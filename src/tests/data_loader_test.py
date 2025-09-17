from pathlib import Path
import pandas
import tempfile
from unittest import TestCase

import pandas as pd

from src.utils import aggregate_by_year
from src.utils.data_loader import dataset_load, counter_data_total, _load_with_unknown_delimiter, \
    multiple_aggregate_by_year, aggregate_by_gender
from src.utils.data_loader_rules import is_csv, is_lower



class DataLoader(TestCase):

    # on va chercher la liste des naissances et on charge un dataframe
    def test_should_return_birth_data_dataframe(self) -> None:
        result = dataset_load("liste_des_naissances.csv")
        assert isinstance(result, pandas.DataFrame)

    def test_should_return_death_data_dataframe(self) -> None:
        result = dataset_load("liste_des_deces.csv")
        assert isinstance(result, pandas.DataFrame)

    def test_should_return_wedding_data_dataframe(self) -> None:
        result = dataset_load("liste_des_mariages.csv")
        assert isinstance(result, pandas.DataFrame)


    def test_should_load_a_valid_dataset_txt_extension(self) -> None:
        file_path = Path(f"data/error_dataset.txt").resolve()
        result = is_csv(file_path)
        assert not result

    def test_should_load_a_valid_dataset_csv_extension(self) -> None:
        file_path = Path(f"data/liste_des_mariages.csv").resolve()
        result = is_csv(file_path)
        assert result

    def test_should_dataset_filename_be_lower_case_with_lowercase_file(self) -> None:
        result = is_lower("liste_des_mariages.csv")
        assert result

    def test_should_dataset_filename_be_lower_case_with_uppercase_file(self) -> None:
        result = is_lower("Liste_des_DC.csv")
        assert not result

    def _create_csv_file(self, content: str, suffix=".csv") -> Path:
        """Helper pour créer un fichier temporaire CSV"""
        tmpdir = tempfile.TemporaryDirectory()
        path = Path(tmpdir.name) / f"test{suffix}"
        path.write_text(content)
        # on garde une référence à tmpdir pour éviter qu'il soit détruit trop tôt
        self.addCleanup(tmpdir.cleanup)
        return path
    def test_should_find_dataset_delimiter_is_semicolon(self):
        csv_file = self._create_csv_file(
            "filename;size\nrapport.pdf;1234\nphoto.JPG;5678"
        )
        df = _load_with_unknown_delimiter(csv_file)
        self.assertEqual(list(df.columns), ["filename", "size"])
        self.assertEqual(df.shape, (2, 2))

    def test_should_find_dataset_delimiter_is_comma(self):
        csv_file = self._create_csv_file(
            "filename,size\nrapport.pdf,1234\nphoto.JPG,5678"
        )
        df = _load_with_unknown_delimiter(csv_file)
        self.assertEqual(list(df.columns), ["filename", "size"])
        self.assertEqual(df.shape, (2, 2))

    def test_should_raise_error_when_delimiter_not_found(self):
        csv_file = self._create_csv_file(
            "filename/size\nrapport.pdf/1234\nphoto.JPG/5678"
        )
        with self.assertRaises(ValueError):
            _load_with_unknown_delimiter(csv_file)

    def test_should_calculate_total_birth_date(self) -> None:
        df_test = pandas.DataFrame(
            {"birth" : [
            "31/07/1951",
            "25/09/2004",
            "01/12/2010",
            "12/10/1899",
            "35/06/1891"]
            }
        )
        result = counter_data_total(df_test)
        assert result == 5

    def test_should_aggregate_by_year(self) -> None:
        df_test = pd.DataFrame(
            {"annee": ["1951", "1951", "1951", "2004", "2010", "2010", "1899", "1891"]}
        )
        result = aggregate_by_year(df_test)
        expected = pd.Series(
            [3, 1, 2, 1, 1], index=[1951, 2004, 2010, 1899, 1891]
        ).sort_index()
        assert result.sort_index().equals(expected)

    def test_should_aggregate_by_year_with_year_superior_to_0(self) -> None:
        df_test = pd.DataFrame(
            {"annee": ["1951", "1951", "1951", "0", "2010", "2010", "1899", "1891"]}
        )
        result = aggregate_by_year(df_test)
        expected = pd.Series(
            [3, 2, 1, 1], index=[1951, 2010, 1899, 1891]
        ).sort_index()
        assert result.sort_index().equals(expected)

    def test_multiple_aggregate_by_year(self) -> None:

        df_birth = pd.DataFrame({"annee": ["1951", "1951", "2004", "2010", "2010"]})
        df_death = pd.DataFrame({"annee": ["1951", "2004", "2004", "2010"]})
        df_wedding = pd.DataFrame({"annee": ["1951", "2004", "2010", "2010", "2010"]})

        result = multiple_aggregate_by_year(df_birth, df_death, df_wedding)
        expected = pd.DataFrame({
            "annee": [1951, 2004, 2010],
            0: [2, 1, 2],  # naissances
            1: [1, 2, 1],  # décès
            2: [1, 1, 3]  # mariages
        })

        result_sorted = result.sort_values("annee").reset_index(drop=True)
        expected_sorted = expected.sort_values("annee").reset_index(drop=True)

        pd.testing.assert_frame_equal(result_sorted, expected_sorted, check_dtype=False)

    def test_aggregate_by_sex(self):
        data = pd.DataFrame({
            "sexe": ["H", "F", "H", "F", "F"]
        })
        result = aggregate_by_gender(data, "sexe")

        expected = pd.Series([2, 3], index=pd.Index(["H", "F"], name="genre"))
        pd.testing.assert_series_equal(result.sort_index(), expected.sort_index())


    def test_aggregate_by_sex_missing_column(self):
        data = pd.DataFrame({"age": [25, 30, 40]})
        with self.assertRaises(KeyError):
            aggregate_by_gender(data, "sexe")
