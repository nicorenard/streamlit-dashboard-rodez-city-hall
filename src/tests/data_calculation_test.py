import pandas as pd

from src.utils.data_calculation import (
    size_dataset,
    multiple_aggregate_by_year,
    aggregate_by_gender,
    aggregate_by_year
)


def test_should_calculate_total_birth_date(self) -> None:
    df_test = pd.DataFrame(
        {
            "birth": [
                "31/07/1951",
                "25/09/2004",
                "01/12/2010",
                "12/10/1899",
                "35/06/1891",
            ]
        }
    )
    result = size_dataset(df_test)
    assert result == 5

def test_should_aggregate_by_year(self) -> None:
    df_test = pd.DataFrame(
        {"annee": ["1951", "1951", "1951", "2004", "2010", "2010", "1899", "1891"]}
    )
    result = aggregate_by_year(df_test)
    expected = pd.Series([3, 1, 2, 1, 1], index=[1951, 2004, 2010, 1899, 1891]).sort_index()
    assert result.sort_index().equals(expected)

def test_should_aggregate_by_year_with_year_superior_to_0(self) -> None:
    df_test = pd.DataFrame(
        {"annee": ["1951", "1951", "1951", "0", "2010", "2010", "1899", "1891"]}
    )
    result = aggregate_by_year(df_test)
    expected = pd.Series([3, 2, 1, 1], index=[1951, 2010, 1899, 1891]).sort_index()
    assert result.sort_index().equals(expected)

def test_multiple_aggregate_by_year(self) -> None:
    df_birth = pd.DataFrame({"annee": ["1951", "1951", "2004", "2010", "2010"]})
    df_death = pd.DataFrame({"annee": ["1951", "2004", "2004", "2010"]})
    df_wedding = pd.DataFrame({"annee": ["1951", "2004", "2010", "2010", "2010"]})

    result = multiple_aggregate_by_year(df_birth, df_death, df_wedding)
    expected = pd.DataFrame(
        {
            "annee": [1951, 2004, 2010],
            0: [2, 1, 2],  # naissances
            1: [1, 2, 1],  # décès
            2: [1, 1, 3],  # mariages
        }
    )

    result_sorted = result.sort_values("annee").reset_index(drop=True)
    expected_sorted = expected.sort_values("annee").reset_index(drop=True)

    pd.testing.assert_frame_equal(result_sorted, expected_sorted, check_dtype=False)

def test_aggregate_by_gender(self):
    data = pd.DataFrame({"genre": ["H", "F", "H", "F", "F"]})
    result = aggregate_by_gender(data, "genre")

    expected = pd.Series([2, 3], index=pd.Index(["H", "F"], name="genre"))
    pd.testing.assert_series_equal(result.sort_index(), expected.sort_index())

def test_aggregate_by_gender_missing_column(self):
    data = pd.DataFrame({"age": [25, 30, 40]})
    with self.assertRaises(KeyError):
        aggregate_by_gender(data, "genre")
