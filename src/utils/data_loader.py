from pathlib import Path
import streamlit as st
import pandas as pd


def _load_with_unknown_delimiter(filepath: Path, delimiters=(",", ";", "\t", "|")):
    for sep in delimiters:
        try:
            df = pd.read_csv(
                filepath,
                sep=sep,
                encoding="utf-8",
                engine="pyarrow",
                on_bad_lines="skip",
            )
            # Nettoyage vectorisé
            df = df.replace("�", "_", regex=True)
            if df.shape[1] > 1 and not df.empty:
                return df
        except Exception as e:
            print(f"Erreur avec le séparateur '{sep}': {e}")
    raise ValueError("Aucun délimiteur approprié trouvé!")

@st.cache_data
def dataset_load(file_name: str) -> pd.DataFrame:
    if not is_lower(file_name):
        raise ValueError("Dataset name is not valid : file name should be lower case.")
    file_path = Path(f"src/data/{file_name}").resolve()
    if not is_csv(file_path):
        raise ValueError("Dataset name is not valid dataset : file extension should be a csv.")
    df = _load_with_unknown_delimiter(file_path)
    return df


def is_csv(file_path: Path) -> bool:
    file_extension = file_path.suffix
    return bool(file_extension == ".csv")


def is_lower(file_name: str) -> bool:
    return file_name.islower()
