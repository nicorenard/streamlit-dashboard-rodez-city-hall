from typing import Dict
import pandas as pd
from pathlib import Path

from pandas import DataFrame

from .data_loader_rules import is_lower, is_csv

def _load_with_unknown_delimiter(filepath: Path, delimiters=(",", ";", "\t", "|")):
    for sep in delimiters:
        try:
            df = pd.read_csv(filepath,sep=sep,encoding="utf-8",engine="pyarrow",on_bad_lines="skip")
            # Nettoyage vectorisé
            df = df.replace("�", "_", regex=True)
            if df.shape[1] > 1 and not df.empty:
                return df
        except Exception as e:
            print(f"Erreur avec le séparateur '{sep}': {e}")
    raise ValueError("Aucun délimiteur approprié trouvé!")

def dataset_load(file_name : str) -> pd.DataFrame:
    if not is_lower(file_name):
        raise ValueError("Dataset name is not valid : file name should be lower case.")
    file_path = Path(f"src/data/{file_name}").resolve()
    if not is_csv(file_path):
        raise ValueError("Dataset name is not valid dataset : file extension should be a csv.")
    df = _load_with_unknown_delimiter(file_path)
    return df


def size_dataset(dataset : pd.DataFrame) -> int:
    return dataset.shape[0]


def aggregate_by_year(dataset: pd.DataFrame) -> pd.Series:
    dataset["annee"] = pd.to_numeric(dataset["annee"], errors="coerce")
    dataset_valid = dataset[dataset["annee"] > 0]
    return dataset_valid.groupby("annee").size()

def multiple_aggregate_by_year(df1 : pd.DataFrame, df2: pd.DataFrame,df3: pd.DataFrame) -> DataFrame:
    birth = aggregate_by_year(df1).fillna(0).astype(int) # for NaN value -> will be 0
    death = aggregate_by_year(df2).fillna(0).astype(int)
    wedding = aggregate_by_year(df3).fillna(0).astype(int)
    final = pd.concat([birth,death,wedding], axis=1).reset_index()
    final["annee"] = pd.to_numeric(final["annee"], downcast='integer')
    return final


def aggregate_by_gender(dataset: pd.DataFrame, column_name : str) -> pd.Series:
    if column_name not in dataset.columns:
        raise KeyError(f"Column '{column_name}' doesn't exist")
    df = dataset.rename(columns={
        column_name:"genre"
    })
    return df.groupby("genre").size()

def _aggregate_by_name(dataset: pd.DataFrame, column_name : str) -> pd.Series:
    return dataset.groupby(column_name).size()

def top_name(dataset : pd.DataFrame, column_name : str, limiter : int) -> pd.Series:
    df = _aggregate_by_name(dataset, column_name)
    return df.sort_values(ascending=False).head(limiter)

def top_name_by_genre(dataset: pd.DataFrame) -> Dict[str, int | str]:
    """
    Returns a dict of metrics:
    - highest and lowest name by gender
    """
    df = dataset.groupby(["genre", "pr1"]).size().reset_index(name="count")
    pivot = df.pivot(index="pr1", columns="genre",values="count").rename(columns={"F_minin": "Féminin","Ind_termin_": "Indéterminé"}).fillna(0)

    return {
        "male" : pivot["Masculin"].idxmax(),
        "female" : pivot ["Féminin"].idxmax()
    }

def top_name_by_year_and_gender(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a pivot of count by year, gender and name
    """

    dataset = dataset[dataset["genre"].isin(["Masculin", "F_minin"])].copy()
    dataset["pr1"] = dataset["pr1"].str.replace("_", "e")
    df = dataset.groupby(["annee", "genre", "pr1"]).size().reset_index(name="count")
    top_df = df.sort_values(["annee", "genre", "count"], ascending=[True, True, False])
    top_df = top_df.groupby(["annee", "genre"]).first().reset_index()
    result = top_df.pivot(index="annee", columns="genre", values="pr1")
    result = result.rename(columns={
        "F_minin": "Féminin"
    })
    return result

def _reshape_names_by_gender_and_year(dataset: pd.DataFrame) -> pd.DataFrame:
    df = pd.melt(
        dataset,
        id_vars=["annee", "genre"],  # keep
        value_vars=["pr1", "pr2", "pr3", "pr4"],  # fusion of all names
        value_name="prenom", #new column name
        var_name="position"
    )
    df["prenom"] = df["prenom"].str.replace("_", "e", regex=False)
    df = df.dropna(subset=["prenom"]) # drop NaN in new column prenom
    df = df[df["prenom"].str.strip() != ""] # strip empty value
    return df

def find_name_query(dataset : pd.DataFrame, name : str) -> Dict[str, int | pd.Series]:
    df = _reshape_names_by_gender_and_year(dataset)
    df_name = df[df["prenom"].str.lower() == name.lower()] # filter on name
    total_name = len(df_name)
    occurrence_in_year = df_name.groupby("annee").size()
    return {
        "total_occurence" : total_name,
        "occurence_by_time" : occurrence_in_year

    }

def name_vs_name(dataset: pd.DataFrame, name1:str, name2: str) -> Dict[str, str]:
    result_name1 = find_name_query(dataset, name1)
    result_name2 = find_name_query(dataset, name2)

    if result_name1["total_occurence"] > result_name2["total_occurence"]:
        winner = name1
    elif result_name1["total_occurence"] == result_name2["total_occurence"]:
        winner = "Exæquo"
    else:
        winner = name2


    return {
        name1: result_name1["total_occurence"],
        name2: result_name2["total_occurence"],
        "winner": winner
    }

def aggregate_by_gender_and_by_year(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset["annee"] = pd.to_numeric(dataset["annee"], errors="coerce", downcast='integer')
    dataset_valid = dataset[dataset["annee"] > 0]
    df = dataset_valid.groupby(["annee", "genre"]).size().reset_index(name="count")
    df_pivot = df.pivot(index="annee", columns="genre", values="count").rename(columns={"F_minin": "Féminin","Ind_termin_": "Indéterminé"}).fillna(0)
    return df_pivot.astype(int)

def top_or_down_birth(dataset: pd.DataFrame) -> Dict[str, Dict]:
    """
    Returns a dict of metrics:
    - highest and lowest year (all genders combined)
    - highest and lowest year by gender
    """
    df = aggregate_by_gender_and_by_year(dataset)
    df["total"] = df.sum(axis=1)

    highest_year = df["total"].idxmax()
    lowest_year = df["total"].idxmin()

    highest_female = df["Féminin"].idxmax()
    lowest_female = df["Féminin"].idxmin()

    highest_male = df["Masculin"].idxmax()
    lowest_male = df["Masculin"].idxmin()

    return {
        "all": {
            "highest_year": {"year": int(highest_year), "value": int(df.loc[highest_year, "total"])},
            "lowest_year": {"year": int(lowest_year), "value": int(df.loc[lowest_year, "total"])}
        },
        "female": {
            "highest_year": {"year": int(highest_female), "value": int(df.loc[highest_female, "Féminin"])},
            "lowest_year": {"year": int(lowest_female), "value": int(df.loc[lowest_female, "Féminin"])}
        },
        "male": {
            "highest_year": {"year": int(highest_male), "value": int(df.loc[highest_male, "Masculin"])},
            "lowest_year": {"year": int(lowest_male), "value": int(df.loc[lowest_male, "Masculin"])}
        }
    }


def top_and_down_death_year(dataset: pd.DataFrame) -> Dict:
    series = aggregate_by_year(dataset)

    highest_year = series.idxmax()
    lowest_year = series.idxmin()

    return {
        "highest_year": {"year": int(highest_year), "value": int(series.loc[highest_year])},
        "lowest_year": {"year": int(lowest_year), "value": int(series.loc[lowest_year])}
        }


def _age_of_death(dt : pd.DataFrame) -> pd.DataFrame:
    dataset = dt.copy()
    dataset["date_naissance"] = pd.to_datetime(dataset["date_naissance"],  errors="coerce", dayfirst=True)
    dataset["date_deces"] = pd.to_datetime(dataset["date_deces"],  errors="coerce", dayfirst=True)
    dataset["age_deces"] = (dataset["date_deces"] - dataset["date_naissance"]).dt.days // 365
    dataset = dataset[dataset["age_deces"].notna()] # filter on NaN
    dataset = dataset[dataset["age_deces"] >= 0]
    dataset["date_naissance"] = dataset["date_naissance"].dt.date
    dataset["date_deces"] = dataset["date_deces"].dt.date
    return dataset.reset_index(drop=True)

def average_death_age_by_year(dt : pd.DataFrame) -> pd.Series:
    dataset = _age_of_death(dt)
    df = dataset[["annee", "age_deces"]].copy()
    return df.groupby("annee")["age_deces"].mean()


def death_age_histogram(dt: pd.DataFrame, bins: int= 20, year_range = None) -> pd.Series:
    dataset = _age_of_death(dt)
    if year_range:
        dataset = dataset[(dataset["annee"] >= year_range[0]) & (dataset["annee"] <= year_range[1])]

    histogram = pd.cut(dataset["age_deces"], bins=bins).value_counts().sort_index()
    histogram.index = [
        f"{int(interval.left)}-{int(interval.right)}"
        for interval in histogram.index
    ] # value are not float bug fix
    return histogram

def average_death_age_by_year_and_genre(dt : pd.DataFrame) -> pd.DataFrame:
    raw_df = _age_of_death(dt)
    raw_df["genre"] = raw_df["genre"].str.replace("_", "e")
    df = raw_df[["annee", "age_deces", "genre"]].copy()
    return df.groupby(["annee", "genre"])["age_deces"].mean().reset_index()

def death_by_month(dt: pd.DataFrame) ->pd.DataFrame:
    df = dt.copy()
    df["date_deces"] = pd.to_datetime(df["date_deces"], errors="coerce")
    df["mois"] = df["date_deces"].dt.month
    return df


def death_by_month_chart(dt: pd.DataFrame) -> pd.Series:
    df = death_by_month(dt)

    # S'assurer qu'on a bien des datetime
    df["date_deces"] = pd.to_datetime(df["date_deces"], errors="coerce")
    df["mois_num"] = df["date_deces"].dt.month

    # Compter et forcer l'ordre 1 → 12
    counts = df.groupby("mois_num").size().reindex(range(1, 13), fill_value=0)

    # Mapping en français
    mois_map = {
        1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
        5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
        9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
    }
    counts.index = [mois_map[m] for m in counts.index]

    return counts



def death_by_season_month(dt: pd.DataFrame) ->pd.Series:
    df = death_by_month(dt)
    df["saison"] = df["mois"].map({
        12:"Hiver",
        1:"Hiver",
        2:"Hiver",
        3:"Printemps",
        4:"Printemps",
        5:"Printemps",
        6:"Ete",
        7: "Ete",
        8: "Ete",
        9: "Automne",
        10: "Automne",
        11: "Automne",
    })
    seasons = ["Hiver","Printemps","Ete","Automne"]
    df_season = df.groupby("saison").size().reindex(seasons, fill_value=0)
    return df_season


def death_by_day(dt: pd.DataFrame) -> pd.Series:
    df = dt.copy()
    df["date_deces"] = pd.to_datetime(df["date_deces"], errors="coerce")
    df["jour_num"] = df["date_deces"].dt.dayofweek
    jours_map = {
        0: "Lundi", 1: "Mardi", 2: "Mercredi",
        3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"
    }
    death_d_df = (
        df.groupby("jour_num").size()
        .reindex(range(7), fill_value=0)
    )
    death_d_df.index = [jours_map[j] for j in death_d_df.index]

    return death_d_df