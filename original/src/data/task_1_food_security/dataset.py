import pandas as pd
from pathlib import Path
from difflib import SequenceMatcher
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from datetime import datetime as dt
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import geopandas as gpd

ROOT_FOLDER = Path.cwd().parent.parent.parent
UNITS = [
    "Bakel",
    "Bambey",
    "Bignona",
    "Birkelane",
    "Bounkiling",
    "Dagana",
    "Dakar",
    "Diourbel",
    "Fatick",
    "Foundiougne",
    "Gossas",
    "Goudiry",
    "Goudomp",
    "Guediawaye",
    "Guinguineo",
    "Kaffrine",
    "Kanel",
    "Kaolack",
    "Kebemer",
    "Kedougou",
    "Kolda",
    "Koumpentoum",
    "Koungheul",
    "Linguere",
    "Louga",
    "Malem Hodar",
    "Matam",
    "Mbacke",
    "Mbour",
    "Medina Yoro Foulah",
    "Nioro Du Rip",
    "Oussouye",
    "Pikine",
    "Podor",
    "Ranerou",
    "Rufisque",
    "Saint Louis",
    "Salemata",
    "Saraya",
    "Sedhiou",
    "Tambacounda",
    "Thies",
    "Tivaouane",
    "Velingara",
    "Ziguinchor",
]

class Dataset(object):
    def __init__(
        self,
        location="adm2_name",
        root_folder=ROOT_FOLDER,
        year_start=2013,
        year_end=2019,
        scaler=MinMaxScaler(feature_range=(-1, 1)),
        seed=42,
        weight=2.5
    ):
        self.location = location
        self.root_folder = root_folder
        self.data_folder = Path(self.root_folder).joinpath("data", "external")
        self.ground = None
        self.interpolate = True
        self.scaler = scaler
        self.year_start = year_start
        self.year_end = year_end
        self.test_size = 0.3
        self.X = None
        self.X_train_flat = None
        self.X_test_flat = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.df_sample_year_location = None
        self.n_samples = None
        self.n_times = None
        self.n_features = None
        self.y_train_sev = None
        self.y_test_sev = None
        self.y_train_perc = None
        self.y_test_perc = None
        self.idx_train = None
        self.idx_test = None
        self.df_code2unit = None
        self.code2unit()
        self.seed = seed
        self.encoder = None
        self.weight = weight
        self._prepare_encoder()
        self.df_x, self.df_y = self.prepare_dataset_df()

    def _prepare_encoder(self):
        self.encoder = LabelEncoder()
        self.encoder.fit(UNITS)
        return

    def save_predicted(self, array, model_name, year):
        geo_file_path = self.root_folder.joinpath("src/results/task_1_climate-risk/data/geodf_unit.json")
        df = self.df_y.reset_index()[self.idx_test].copy()
        df[f'severity_{model_name}_{year}'] = array
        df.to_csv(self.data_folder.joinpath(f'predictions_{model_name}.csv'))

        df.reset_index(inplace=True)
        df = df[['adm2_name_code', f'severity_{model_name}_{year}']]
        df['adm2_name_code'] = df['adm2_name_code'].astype(int)
        df.set_index('adm2_name_code', inplace=True)
        df_unit = gpd.read_file(filename=geo_file_path)

        df_unit = df_unit.join(df)
        df_unit.to_file(filename=geo_file_path, driver='GeoJSON')
        return df_unit

    def train_test_split(self):
        """
        indices = list(range(self.n_samples))
        xtr, xts, ytr, yts, itr, its = train_test_split(
            self.X, self.y, indices, test_size=self.test_size, random_state=self.seed
        )
        self.idx_train = itr
        self.idx_test = its"""
        idx_test = self.df_y.reset_index()['season'] == 2019
        idx_train = ~idx_test
        
        xtr = self.X[idx_train]
        ytr = self.y[idx_train]
        xts = self.X[idx_test]
        yts = self.y[idx_test]
        self.idx_train = idx_train
        self.idx_test = idx_test
        
        return xtr, xts, ytr, yts

    def prepare_dataset_array(self, split=True):
        self._prepare_dataset_array()
        n_samples = self.X.shape[0]
        if self.interpolate:
            self.mean = Dataset.get_mean_arr(self.X)
            for i in range(n_samples):
                self.X[i] = self.interpolate_sample(self.X[i])
        if split:
            self.X_train, self.X_test, self.y_train, self.y_test = self.train_test_split()
            self.y_train_sev = self.y_train[:, 0]
            self.y_test_sev = self.y_test[:, 0]
            self.y_train_perc = self.y_train[:, 1:]
            self.y_test_perc = self.y_test[:, 1:]
        if self.scaler is not None:
            self._scale()

        self.X_train_flat = self._flatten(self.X_train, keep="sample", samples=self.X_train.shape[0])
        self.X_test_flat = self._flatten(self.X_test, keep="sample", samples=self.X_test.shape[0])
        return

    def _flatten(self, input, keep="features", samples=None):
        arr = input.copy()
        if keep == "features":
            arr = arr.swapaxes(0, 2)
            if samples is not None:
                return arr.reshape(self.n_features, samples * self.n_times)
            return arr.reshape(self.n_features, self.n_samples * self.n_times)
        elif keep == "sample":
            if samples is not None:
                return arr.reshape(samples, self.n_times * self.n_features)
            return arr.reshape(self.n_samples, self.n_times * self.n_features)
        else:
            raise KeyError("to be implemented")

    def _unflatten(self, input, keep="features", samples=None):
        arr = input.copy()
        if keep == "features":
            if samples is not None:
                arr = arr.reshape(self.n_times, samples, self.n_features)
                return arr.swapaxes(0, 1)
            arr = arr.reshape(self.n_times, self.n_samples, self.n_features)
            return arr.swapaxes(0, 1)
        elif keep == "sample":
            if samples is not None:
                return arr.reshape(samples, self.n_times, self.n_features)
            return arr.reshape(self.n_samples, self.n_times, self.n_features)
        else:
            raise KeyError("to be implemented")

    def _scale(self):
        x_train = self._flatten(self.X_train, samples=self.X_train.shape[0])
        x_train = x_train.swapaxes(0, 1)
        x_train = self.scaler.fit_transform(x_train)
        x_train = x_train.swapaxes(0, 1)
        self.X_train = self._unflatten(x_train, samples=self.X_train.shape[0])

        x_test = self._flatten(self.X_test, samples=self.X_test.shape[0])
        x_test = x_test.swapaxes(0, 1)
        x_test = self.scaler.transform(x_test)
        x_test = x_test.swapaxes(0, 1)
        self.X_test = self._unflatten(x_test, samples=self.X_test.shape[0])

    @staticmethod
    def get_mean_arr(arr):
        means = np.nanmean(arr, axis=0)
        for i in range(means.shape[1]):
            means[:, i] = Dataset._interpolate_line(means[:, i])
        return means

    @staticmethod
    def _interpolate_line(line):
        return np.interp(np.arange(36), np.argwhere(~np.isnan(line)).flatten(), line[~np.isnan(line)])

    def interpolate_sample(self, arr):
        n_features = arr.shape[1]
        output = np.empty_like(arr)
        for i in range(n_features):
            line = arr[:, i]
            idx_notnull = np.argwhere(~np.isnan(line)).flatten()
            if len(idx_notnull) == 0:
                # replace by mean feature value across all samples
                line2 = self.mean[:, i]
            else:
                line2 = Dataset._interpolate_line(line)
            output[:, i] = line2
        return output

    @staticmethod
    def _filter_feature(df, feature_name):
        if isinstance(feature_name, str):
            df = df[df["variable"] != feature_name]
        else:
            for f in feature_name:
                df = df[df["variable"] != f]
        return df

    def _prepare_dataset_array(self):
        df = self.df_x.copy()
        # y = self.df_y.copy()

        df = df[(df["season"] >= self.year_start) & (df["season"] <= self.year_end)]
        df.set_index(["season", "adm2_name_code"], inplace=True)
        df.reset_index(inplace=True)
        sorting = df[["season", "adm2_name_code", "variable"]]
        df_temp = df.drop(["season", "adm2_name_code", "variable"], axis=1)
        df_temp = df_temp.pivot(columns="season_day", values="value")

        cols = [
            0,
            10,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            100,
            110,
            120,
            130,
            140,
            150,
            160,
            170,
            180,
            190,
            200,
            210,
            220,
            230,
            240,
            250,
            260,
            270,
            280,
            290,
            300,
            310,
            320,
            330,
            340,
            350,
        ]

        df_temp = sorting.join(df_temp, rsuffix="1")
        from numpy import nanmean

        df_res = df_temp[["season", "adm2_name_code", "variable"]].copy()
        df_res.drop_duplicates(inplace=True)
        df_res.reset_index(drop=True, inplace=True)
        for d in cols:
            series = df_temp.groupby(["season", "adm2_name_code", "variable"]).agg({d: nanmean}).reset_index(drop=True)
            series.reset_index(drop=True, inplace=True)
            df_res = pd.concat([df_res, series], axis=1)

        df_res.set_index(["season", "adm2_name_code", "variable"], inplace=True)
        df_res.sort_index(inplace=True)

        years = df_res.index.get_level_values(level="season")
        units = df_res.index.get_level_values(level="adm2_name_code")
        idx = pd.DataFrame([years, units]).T
        idx.drop_duplicates(inplace=True)

        vars = df["variable"].unique()
        vars.sort()
        years_un = np.unique(years.to_numpy())
        years_un.sort()
        units_un = np.unique(units.to_numpy())
        units_un.sort()
        from itertools import product

        iter = product(years_un, units_un, vars)
        iter = list(iter)
        iter = [list(i) for i in iter]
        df1 = pd.DataFrame(iter)
        df2 = pd.DataFrame(0, index=df1.index, columns=df_res.columns)
        df_base = df1.join(df2, rsuffix="1")
        cols = ["season", "adm2_name_code", "variable", 0]
        cols.extend(list(df_base.columns)[4:])
        df_base.columns = cols
        df_base.set_index(["season", "adm2_name_code", "variable"], inplace=True)

        x = None
        for i in range(len(idx)):
            temp = df_res.xs((idx.iloc[i, 0], idx.iloc[i, 1]))
            base = df_base.xs((idx.iloc[i, 0], idx.iloc[i, 1]))
            temp = base + temp
            temp = temp.T
            temp = temp.values
            temp = temp[np.newaxis, :]
            if x is None:
                x = temp
            else:
                x = np.vstack([x, temp])
        self.X = x
        self.df_sample_year_location = df_res.reset_index()[["season", "adm2_name_code"]].copy()
        self.df_sample_year_location.drop_duplicates(inplace=True)
        self.df_sample_year_location.reset_index(inplace=True, drop=True)
        self.df_sample_year_location.reset_index(inplace=True)
        self.df_sample_year_location.columns = ["sample", "season", "adm2_name_code"]

        # get ground truth
        df_y = self.df_y.copy()
        df_y["adm2_name_code"] = df_y["adm2_name"].astype(int)
        # df_y.drop('adm2_name', axis=1, inplace=True)

        df_y.set_index(["season", "adm2_name_code"], inplace=True)
        df_right = self.df_sample_year_location.set_index(["season", "adm2_name_code"])

        self.df_y = df_y.join(df_right)

        samples = self.df_y["sample"].values
        # filter only what we have
        self.X = self.X[samples]
        self.y = self.df_y[["severity"] + [f"phase{i}" for i in range(1, 6)]].values
        self.y_severity = self.y[:, 0]
        self.y_percentage = self.y[:, 1:]
        self.n_samples, self.n_times, self.n_features = self.X.shape
        return

        # index = x["season_day"].unique()
        # index.sort()
        #
        # df = pd.DataFrame(
        #     0,
        #     columns=cols,
        #     index=index,
        # )
        # indices = np.unique(x.index.values)
        # n_samples = len(indices)
        # x_mat = np.empty((n_samples, 36, len(cols)))
        # z_mat = np.empty((n_samples, 2))
        # x_single = np.empty((n_samples, 2, 1))
        # i = 0
        # for id in tqdm(indices):
        #     x_sample = x.xs(id).copy()
        #     # vector for vector values per year
        #     x_vector = x_sample[x_sample["variable"] != "urbanization"].copy()
        #     # single values for single entries per year
        #     x_s = x_sample[x_sample["variable"] == "urbanization"].copy()
        #     x_vector.reset_index(inplace=True, drop=True)
        #     sum(x_vector.duplicated(subset=["variable", "season_day"]))
        #     # x1['season_day'] = x1['season_day'].apply(lambda var: var/10)
        #
        #     x_vector = x_vector.groupby(["variable", "season_day"]).mean()
        #     x_vector.reset_index(inplace=True)
        #     x_vector = x_vector.pivot("season_day", "variable", "value")
        #     x_vector = df + x_vector
        #     # x1 = minmax_scale(x1)
        #     x_mat[i, :, :] = x_vector
        #     z_mat[i, :] = id
        #     if len(x_s["value"]) > 0:
        #         x_single[i, 0] = x_s["value"].values  # urbanisation
        #     else:
        #         x_single[i, 0] = np.nan
        #     x_single[i, 1] = id[1]  # region
        #     i += 1
        # # with open(str(np.save(Path(data_folder).joinpath('x_mat.npy'))), 'wb') as f:
        # #     np.save(f, x_mat)
        # # with open(str(np.save(Path(data_folder).joinpath('y_mat.npy'))), 'wb') as f:
        # #     np.save(f, y_mat)
        # return x_mat, x_single, z_mat

    def code2unit(self):
        self.df_code2unit = pd.read_csv(Path(self.data_folder).joinpath("adm1-adm2_name.csv"), index_col=0)
        return self.df_code2unit

    def rename_location(self, df, rename_col="adm2_name"):
        """
        Rename misspelled location in df['adm2_name']
        """
        if "adm2_name_code" in df.columns:
            return df

        u2r = pd.read_csv(Path(self.data_folder).joinpath("adm1-adm2_name.csv"), index_col=0)
        locations = u2r[self.location].unique()
        if rename_col == "adm1_name":
            u2r.drop("adm2_name", axis=1, inplace=True)
            u2r.set_index("adm1_name", inplace=True)
        elif rename_col == "adm2_name":
            u2r.drop("adm1_name", axis=1, inplace=True)
            u2r.set_index("adm2_name", inplace=True)
        else:
            raise KeyError("Wrong col_name.")
        cols = df.columns[1:]
        df2 = pd.DataFrame(columns=["adm2_name_code"].extend(cols))
        df = df.set_index(rename_col)
        regs = np.unique(df.index.values)
        for r in regs:
            temp = df.loc[r].copy()

            try:
                units = u2r.loc[r].values
            except KeyError:
                r = self.match_unit(r, locations)
                units = u2r.loc[r].values

            temp.reset_index(inplace=True, drop=True)
            if type(temp) == pd.Series:
                temp = pd.DataFrame(temp)
            for i in units:
                if type(i) == np.int64:
                    temp1 = temp.assign(adm2_name_code=i)
                else:
                    temp1 = temp.assign(adm2_name_code=i[0])
                df2 = df2.append(temp1)
        return df2

    def get_rainfall(self):
        file_path = Path(self.data_folder).joinpath("asap", "region", "rainfall.csv")
        return pd.read_csv(file_path)

    def get_asap_data(self, start_season_day=100, inplace=False):
        """
        For IPC prediction
        """

        if self.location == "adm1_name":
            print("This dataset is not preprocessed.")
            file_path = Path(self.data_folder).joinpath("asap", "region", "SEN_asap_region.csv")
        elif self.location == "adm2_name":
            file_path = Path(self.data_folder).joinpath("asap", "unit", "asap_data_crop_gaul2.csv")
        else:
            raise ValueError("Incorrect resolution.")

        df_asap = pd.read_csv(file_path)
        # drop rainfall, its loaded separately
        df_asap = df_asap[df_asap["variable"] != "Rainfall"]

        if "Unnamed: 0" in df_asap.columns:
            df_asap.set_index("Unnamed: 0", inplace=True)
        df_asap = df_asap[(df_asap["season_year"] >= self.year_start) & (df_asap["season_year"] <= self.year_end)]

        if "dec_day" not in df_asap.columns:
            df_asap["dec_day"] = df_asap["yearday"].apply(lambda x: (x // 10) * 10)
        if "season_dec_day" not in df_asap.columns:
            for i, row in df_asap.iterrows():
                y = int(row["year"])
                d = row["dec_day"]
                df_asap.loc[i, "season_year"] = y if d > start_season_day else y - 1
                df_asap.loc[i, "season_dec_day"] = d - 100 if d > start_season_day else 360 - start_season_day + d

        if inplace:

            df_asap.to_csv(file_path, index=False)

        return df_asap

    def load_asap_data(self, resolution="unit"):
        if resolution == "unit":
            df_asap = pd.read_csv(Path(self.data_folder).joinpath("asap_data_crop_gaul2.csv"))

        else:
            raise KeyError("Choose unit resolution")

        return df_asap

    def get_ipc_data(self, semester=0, resolution="unit"):
        df_ipc = pd.read_csv(Path(self.data_folder).joinpath("ipc_current.csv"))
        df_ipc["severity"] = (
            df_ipc["phase1"]
            + df_ipc["phase2"] * self.weight
            + df_ipc["phase3"] * np.power(self.weight, 2)
            + df_ipc["phase4"] * np.power(self.weight, 3)
            + df_ipc["phase5"] * np.power(self.weight, 4)
        ) / df_ipc["population"]

        # if resolution == "unit":
        #     if "adm1_name" not in df_ipc.columns:
        #         cols = list(df_ipc.columns)
        #         cols[0] = "adm1_name"
        #         df_ipc.columns = cols
        # else:
        #     return print("Needs to be implemented")
        if semester == 0:
            # spring
            df_ipc = df_ipc[df_ipc["datetime"].apply(lambda x: x[5:7] == "01")].copy()
            df_ipc["season"] = df_ipc["datetime"].apply(lambda x: int(x.split("-")[0]) - 1)
        elif semester == 1:
            # autumn
            df_ipc = df_ipc[df_ipc["datetime"].apply(lambda x: x[5:7] == "09")].copy()
            df_ipc["season"] = df_ipc["datetime"].apply(lambda x: int(x.split("-")[0]))
        else:
            raise ValueError("Select semester to be 0 or 1.")
        return df_ipc

    def encode_location(self, df, col_name):
        u2r = pd.read_csv(Path(self.data_folder).joinpath("adm1-adm2_name.csv"), index_col=0)
        u2r.drop("adm1_name", axis=1, inplace=True)
        u2r.set_index("adm2_name", inplace=True)
        df.reset_index(inplace=True)
        df[col_name + "_old"] = df[col_name]
        for i, item in df[col_name].iteritems():
            code = u2r.loc[item].values
            if type(code) == np.int64:
                df.loc[i, col_name] = str(code)
            else:
                df.loc[i, col_name] = str(code[0])
        df[col_name].astype(int)
        return df

    def prepare_dataset_df(self):
        # ground truth
        df_ipc = self.get_ipc_data()
        df_ipc.set_index("season", inplace=True)
        phase_cols = [f"phase{i}" for i in range(1, 6)]
        df_ipc["population"] = 0
        for p in phase_cols:
            df_ipc["population"] += df_ipc[p]
        for p in phase_cols:
            df_ipc[p] = df_ipc[p] / df_ipc["population"]
        ipc_cols = ["adm2_name", "severity"]
        ipc_cols.extend(phase_cols)
        df_ipc = df_ipc[ipc_cols]
        # df_ipc = df_ipc[["severity", "season", "adm2_name"]]
        df_ipc = self.encode_location(df_ipc, col_name="adm2_name")

        # x variable
        df_asap = self.get_asap_data()
        df_asap = self.rename_location(df_asap, rename_col="adm2_name")

        # rainfall
        df_rain = self.get_rainfall()
        df_rain = self.rename_location(df_rain, rename_col="adm1_name")

        df_urban = self.get_urbanization()
        df_urban = self.rename_location(df_urban, rename_col="adm1_name")
        df_urban["variable"] = "urbanization"
        # df_urban.reset_index(inplace=True)
        # df_urban.columns = ['adm2_name', 'year', 'value', 'variable']

        df_food_price = self.get_food_price()
        df_food_price = self.rename_location(df_food_price, rename_col="adm1_name")

        # encoder = LabelEncoder()
        # encoder.fit(known_locations)
        #
        # df_ipc['adm2_name_code'] = encoder.transform(df_ipc['adm2_name'])
        # # df_ipc.drop('adm2_name', axis=1, inplace=False)
        # df_asap['adm2_name_code'] = encoder.transform(df_asap['adm2_name'])
        # # df_asap.drop('adm2_name', axis=1, inplace=False)

        x = pd.DataFrame(columns=["adm2_name_code", "variable", "year", "dec_day", "value"])

        # append asap
        temp = df_asap[["adm2_name_code", "variable", "year", "dec_day", "value"]].copy()
        x = x.append(temp)

        # append asap
        temp = df_urban[["adm2_name_code", "variable", "year", "value"]].copy()
        temp["dec_day"] = 0
        x = x.append(temp)

        # append rainfall
        temp = df_rain[["adm2_name_code", "variable", "year", "dec_day", "value"]].copy()
        x = x.append(temp)

        # append asap
        temp = df_food_price[["adm2_name_code", "variable", "year", "dec_day", "value"]].copy()
        x = x.append(temp)

        x["season"] = x["year"]
        x.loc[x["dec_day"] < 100, "season"] = x.loc[x["dec_day"] < 100, "season"].apply(lambda x: x - 1)
        x["season_day"] = x["dec_day"].apply(lambda x: x - 100 if x >= 100 else x + 360 - 100)
        x.drop(["year", "dec_day"], axis=1, inplace=True)
        x = x[(x["season"] >= self.year_start) & (x["season"] <= self.year_end)]

        # df_ipc = df_ipc[["season", "adm2_name", "variable", "severity"]]
        # df_ipc.columns = ["season", "adm2_name_code", "variable", "value"]
        y = df_ipc  # [["adm2_name_code", "variable", "season", "value"]]
        return x, y

    def get_urbanization(self):
        df = pd.read_csv(Path(self.data_folder).joinpath("SEN_urbanisation_prediction.csv"), index_col=0)
        return df

    def get_food_price(self):
        """
        Load already aggregated data, see notebook: 'SEN_food_prices_preprocess.ipynb'
        @param root_folder:
        @return: df
        """
        df = pd.read_csv(Path(self.data_folder).joinpath("SEN_market_data_aggreg.csv"), index_col=0)

        # filter
        df = Dataset._filter_feature(df, ["Sorghum", "Groundnuts"])

        # add yearday and year to data
        df = Dataset.datetime2col(df, datetime_col="datetime", target_format="dec_day")
        df = Dataset.datetime2col(df, datetime_col="datetime", target_format="year")
        return df

    @staticmethod
    def datetime2col(df, datetime_col=None, datetime_format="%Y-%m-%d", target_format=None):
        """
        @param df: dataframe
        @param datetime_format: format of datetime column in df
        @type datetime_col: str
        @param target_format: from {'yearday', 'year', 'month', 'day', 'dec_day'}

        'dec_day' is yearday rounded to 10 for better alignment
        """

        if datetime_col is None:
            datetime_col = "datetime"

        if datetime_col not in df.columns:
            raise ValueError("No datetime column")

        code = {"yearday": "%j", "year": "%Y", "month": "%m", "day": "%d"}

        if target_format == "dec_day":
            target_format_code = code["yearday"]
            df[target_format] = df[datetime_col].apply(
                lambda x: int(dt.strptime(x, datetime_format).strftime(target_format_code))
            )
            df[target_format] = df[target_format].apply(lambda x: (x // 10) * 10)
        else:
            if target_format not in code.keys():
                raise KeyError("Wrong target format")
            target_format_code = code[target_format]
            df[target_format] = df[datetime_col].apply(
                lambda x: int(dt.strptime(x, datetime_format).strftime(target_format_code))
            )
        return df

    @staticmethod
    def match_unit(unit, units):
        sim = [SequenceMatcher(None, unit, u).ratio() for u in units]
        sim = np.array(sim)
        id = np.argsort(-sim)[0]
        return units[id]


if __name__ == "__main__":
    # df = get_asap_data(resolution='unit', inplace=True)
    # print(df.head())
    # df_ipc = get_ipc_data()
    # print(df_ipc)
    #
    # print(encode_location(df_ipc, 'adm2_name').head())
    ds = Dataset()
    ds.prepare_dataset_array()
