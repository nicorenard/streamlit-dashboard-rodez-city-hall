from pathlib import Path
import pandas
import tempfile
from unittest import TestCase



from src.utils.data_loader import  dataset_load, _load_with_unknown_delimiter, is_csv, is_lower


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
        file_path = Path("data/error_dataset.txt").resolve()
        result = is_csv(file_path)
        assert not result

    def test_should_load_a_valid_dataset_csv_extension(self) -> None:
        file_path = Path("data/liste_des_mariages.csv").resolve()
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
        csv_file = self._create_csv_file("filename;size\nrapport.pdf;1234\nphoto.JPG;5678")
        df = _load_with_unknown_delimiter(csv_file)
        self.assertEqual(list(df.columns), ["filename", "size"])
        self.assertEqual(df.shape, (2, 2))

    def test_should_find_dataset_delimiter_is_comma(self):
        csv_file = self._create_csv_file("filename,size\nrapport.pdf,1234\nphoto.JPG,5678")
        df = _load_with_unknown_delimiter(csv_file)
        self.assertEqual(list(df.columns), ["filename", "size"])
        self.assertEqual(df.shape, (2, 2))

    def test_should_raise_error_when_delimiter_not_found(self):
        csv_file = self._create_csv_file("filename/size\nrapport.pdf/1234\nphoto.JPG/5678")
        with self.assertRaises(ValueError):
            _load_with_unknown_delimiter(csv_file)
