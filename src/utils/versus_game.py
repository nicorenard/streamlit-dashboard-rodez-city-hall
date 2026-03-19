import pandas as pd
from typing import Dict

from .data_calculation import find_name_query


def find_better_name_game(dataset: pd.DataFrame, name1: str, name2: str) -> Dict[str, str]:
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
        "winner": winner,
    }
