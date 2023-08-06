from typing import Tuple, Optional, Dict
from abc import ABC, abstractmethod
import os
import math

import pandas as pd
import numpy as np
import traceback
from loguru import logger
from numpy.random import seed, choice
from pathos.multiprocessing import ProcessingPool
import dill
import pickle

from syngen.ml.vae import *
from syngen.ml.reporters import Report
from syngen.ml.data_loaders import DataLoader


class AbstractHandler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, data: pd.DataFrame, **kwargs):
        pass


class BaseHandler(AbstractHandler):
    def __init__(self, metadata: dict, paths: dict, table_name: str):
        self.metadata = metadata
        self.paths = paths
        self.table_name = table_name
        if self.table_name is None:
            raise KeyError("No table name was provided.")

    _next_handler: AbstractHandler = None

    def set_next(self, handler: AbstractHandler) -> AbstractHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, data: pd.DataFrame, **kwargs):

        if self._next_handler:
            return self._next_handler.handle(data, **kwargs)

        return None

    @staticmethod
    def create_wrapper(cls_name, data: pd.DataFrame, schema: Optional[Dict], **kwargs):
        return globals()[cls_name](
            data, schema, kwargs["metadata"], kwargs["table_name"], kwargs["paths"]
        )


class RootHandler(BaseHandler):
    def __init__(self, metadata: dict, paths: dict, table_name: str):
        super().__init__(metadata, paths, table_name)

    def _prepare_dirs(self):
        os.makedirs(self.paths["model_artifacts_path"], exist_ok=True)
        tmp_store_path = self.paths["tmp_store_path"]
        os.makedirs(tmp_store_path, exist_ok=True)

    @staticmethod
    def _set_options(data, options):
        if options["drop_null"]:
            if not data.dropna().empty:
                data = data.dropna()
            else:
                logger.warning("The specified 'drop_null' argument results in the empty dataframe, "
                               "so it will be ignored")

        if options["row_subset"]:
            data = data.sample(n=min(options["row_subset"], len(data)))
            if len(data) < 100:
                logger.warning("The input table is too small to provide any meaningful results. "
                               "Please consider 1) disable drop_null argument, 2) provide bigger table")
            elif len(data) < 500:
                logger.warning(
                    f"The amount of data is {len(data)} rows. It seems that it isn't enough to supply "
                    f"high-quality results. To improve the quality of generated data please consider any of the steps: "
                    f"1) provide a bigger table, 2) disable drop_null argument")
        return data

    def set_options(self, data, options):
        return self._set_options(data, options)

    def prepare_data(self, data, options):
        data = self.set_options(data, options)

        data_columns = set(data.columns)
        dropped_cols = set(data.columns) - data_columns
        if len(dropped_cols) > 0:
            logger.info(f"Empty columns {dropped_cols} were removed")
        return data

    def handle(self, data: pd.DataFrame, **kwargs):
        self._prepare_dirs()
        data = self.prepare_data(data, kwargs)
        data.to_csv(self.paths["input_data_path"], index=False)
        return super().handle(data, **kwargs)


class VaeTrainHandler(BaseHandler):
    def __init__(
            self, metadata: dict, paths: dict, table_name: str, schema: Optional[Dict], wrapper_name: str
    ):
        super().__init__(metadata, paths, table_name)
        self.wrapper_name = wrapper_name
        self.schema = schema
        self.state_path = self.paths["state_path"]

    def __fit_model(
            self, data: pd.DataFrame, epochs: int, batch_size: int
    ):
        os.makedirs(self.state_path, exist_ok=True)
        logger.info("Start VAE training")
        if data is None:
            logger.error("For mode = 'train' path must be provided")
            raise ValueError("Can't read data from path or path is None")

        self.model = self.create_wrapper(
            self.wrapper_name,
            data,
            self.schema,
            metadata=self.metadata,
            table_name=self.table_name,
            paths=self.paths,
        )

        self.model.batch_size = min(batch_size, len(data))
        self.model.fit_on_df(
            data,
            epochs=epochs,
        )

        self.model.save_state(self.state_path)
        logger.info("Finished VAE training")

    def handle(self, data: pd.DataFrame, **kwargs):
        self.__fit_model(
            data,
            kwargs["epochs"],
            kwargs["batch_size"]
        )
        return super().handle(data, **kwargs)


class VaeInferHandler(BaseHandler):
    def __init__(
            self,
            metadata: dict,
            paths: dict,
            table_name: str,
            wrapper_name: str,
            random_seed: int = None,
    ):
        super().__init__(metadata, paths, table_name)
        self.random_seed = random_seed
        self.random_seeds_list = []
        if random_seed:
            seed(random_seed)
        self.vae = None
        self.wrapper_name = wrapper_name
        self.vae_state_path = self.paths["state_path"]
        self.path_to_merged_infer = self.paths["path_to_merged_infer"]
        self.fk_kde_path = self.paths["fk_kde_path"]

    def _prepare_dir(self):
        tmp_store_path = self.paths["tmp_store_path"]
        os.makedirs(tmp_store_path, exist_ok=True)

    def _is_pk(self):
        is_pk = self.table_name.endswith("_pk")
        return is_pk

    def _concat_slices_with_unique_pk(self, df_slices: list):
        if self.metadata and self.table_name in self.metadata:
            config_of_keys = self.metadata.get(self.table_name).get("keys", {})
            for key in config_of_keys.keys():
                column = config_of_keys.get(key).get("columns")[0]
                if config_of_keys.get(key).get("type") == "PK" and not isinstance(df_slices[0][column][0], str):
                    cumm_len = 0
                    for i, frame in enumerate(df_slices):
                        frame[column] = frame[column].map(lambda pk_val: pk_val + cumm_len)
                        cumm_len += len(frame)
        return pd.concat(df_slices, ignore_index=True)

    def run_separate(self, params: Tuple):
        i, size = params

        if self.random_seed:
            seed(self.random_seeds_list[i])

        data, schema = DataLoader(self.paths["input_data_path"]).load_data()
        self.vae = self.create_wrapper(
            self.wrapper_name,
            data,
            schema,
            metadata={"table_name": self.table_name},
            table_name=self.table_name,
            paths=self.paths,
        )
        self.vae.load_state(self.vae_state_path)
        synthetic_infer = self.vae.predict_sampled_df(size)
        return synthetic_infer

    @staticmethod
    def split_by_batches(size, nodes):
        quote = int(size / nodes)
        data = [quote] * nodes
        data.append((size - nodes * quote) + data.pop())
        return data

    def run(self, size: int, run_parallel: bool = True):
        logger.info("Start data synthesis")
        if run_parallel:
            pool = ProcessingPool()
            if self.random_seed:
                self.random_seeds_list = choice(
                    range(0, max(100, pool.nodes)), pool.nodes, replace=False
                )

            frames = pool.map(
                self.run_separate, enumerate(self.split_by_batches(size, pool.nodes))
            )
            generated = self._concat_slices_with_unique_pk(frames)
        else:
            if self.random_seed:
                self.random_seeds_list = [self.random_seed]
            generated = self.run_separate((0, size))
        return generated

    def kde_gen(self, pk_table, pk_column_label, size, fk_label):
        pk = pk_table[pk_column_label]

        try:
            with open(f"{self.fk_kde_path}{fk_label}.pkl", "rb") as file:
                kde = dill.load(file)
            pk = pk.dropna()
            numeric_pk = np.arange(len(pk)) if pk.dtype == "object" else pk
            fk_pdf = np.maximum(kde.evaluate(numeric_pk), 1e-12)
            synth_fk = np.random.choice(pk, size=size, p=fk_pdf / sum(fk_pdf), replace=True)
            synth_fk = pd.DataFrame({fk_label: synth_fk}).reset_index(drop=True)

        except FileNotFoundError:
            logger.warning(f"The mapper for the {fk_label} text key is not found. Making simple sampling")
            synth_fk = pk.sample(size, replace=True).reset_index(drop=True)
            synth_fk.rename(fk_label, inplace=True)

        return synth_fk

    def generate_keys(self, generated, size, metadata, table_name):
        metadata_of_table = metadata.get(table_name)
        if "keys" not in metadata_of_table:
            return None
        config_of_keys = metadata_of_table.get("keys")
        for key in config_of_keys.keys():
            if config_of_keys.get(key).get("type") == "FK":
                pk_table = config_of_keys.get(key).get("references").get("table")
                pk_path = f"model_artifacts/tmp_store/{pk_table}/merged_infer_{pk_table}.csv"
                if not os.path.exists(pk_path):
                    raise FileNotFoundError(
                        "The table with a primary key specified in the metadata file does not "
                        "exist or is not trained. Ensure that the metadata contains the "
                        "name of referenced table with a primary key in the foreign key declaration section."
                    )
                pk_table_data, pk_table_schema = DataLoader(pk_path).load_data()
                pk_column_label = config_of_keys.get(key).get("references").get("columns")[0]
                logger.info(f"The {pk_column_label} assigned as a foreign_key feature")

                synth_fk = self.kde_gen(pk_table_data, pk_column_label, size, config_of_keys.get(key).get("columns")[0])
                generated = generated.reset_index(drop=True)

                null_column_name = f"{key}_null"
                if null_column_name in generated.columns:
                    not_null_column_mask = generated[null_column_name].astype("float64") <= 0.5
                    synth_fk = synth_fk.where(not_null_column_mask, np.nan)
                    generated = generated.drop(null_column_name, axis=1)

                generated = pd.concat([generated, synth_fk], axis=1)
        return generated

    def handle(
            self,
            size: int,
            run_parallel: bool = True,
            batch_size: int = None,
            print_report: bool = False,
            metadata_path: str = None,
    ):
        self._prepare_dir()
        try:
            if not batch_size:
                batch_size = size
            batch_num = math.ceil(size / batch_size)
            logger.info(f"Total of {batch_num} batch(es)")
            batches = self.split_by_batches(size, batch_num)
            prepared_batches = [self.run(batch, run_parallel) for batch in batches]
            prepared_data = self._concat_slices_with_unique_pk(prepared_batches) if len(prepared_batches) > 0 else pd.DataFrame()

            is_pk = self._is_pk()
            if metadata_path is not None:
                if not is_pk:
                    generated_data = self.generate_keys(prepared_data, size, self.metadata, self.table_name)
                    if generated_data is None:
                        prepared_data.to_csv(self.path_to_merged_infer, index=False)
                    else:
                        generated_data.to_csv(self.path_to_merged_infer, index=False)
                else:
                    prepared_data.to_csv(self.path_to_merged_infer, index=False)
            if metadata_path is None:
                prepared_data.to_csv(self.path_to_merged_infer, index=False)
            if print_report:
                Report().generate_report()
                Report().clear_report()
            logger.info(
                f"Synthesis of the table - {self.table_name} was completed. "
                f"Synthetic data saved in {self.path_to_merged_infer}"
            )
        except Exception as e:
            logger.info(f"Generation of the table - {self.table_name} failed on running stage.")
            logger.error(e)
            logger.error(traceback.format_exc())
            raise
