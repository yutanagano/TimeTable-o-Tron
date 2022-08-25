from pathlib import Path
from turtle import st
import pytest
from source import utils
import subprocess


@pytest.fixture
def tmp_xlsx_file(tmp_path) -> str:
    tmp_xlsx = tmp_path / 'foo.xlsx'
    subprocess.run(['touch', tmp_xlsx])

    return str(tmp_xlsx.resolve())


@pytest.fixture
def tmp_file(tmp_path):
    tmp = tmp_path / 'foo'
    subprocess.run(['touch', tmp])

    return str(tmp.resolve())


class TestResolvePathToNewTimetable:
    def test_resolve(self, tmp_xlsx_file):
        result = utils.resolve_path_to_new_timetable(str_path=tmp_xlsx_file)
        expected = Path(tmp_xlsx_file).resolve()

        assert result == expected

    
    def test_error_if_not_xlsx(self, tmp_file):
        with pytest.raises(RuntimeError):
            utils.resolve_path_to_new_timetable(str_path=tmp_file)


    def test_error_if_nonexistent(self):
        with pytest.raises(RuntimeError):
            utils.resolve_path_to_new_timetable(str_path='foo/bar/baz')


class TestResolvePathToOldTimetables:
    def test_resolve(self, tmp_path):
        result = utils.resolve_path_to_old_timetables(str_path=str(tmp_path))
        expected = tmp_path.resolve()

        assert result == expected


    def test_error_if_not_directory(self, tmp_file):
        with pytest.raises(RuntimeError):
            utils.resolve_path_to_old_timetables(str_path=tmp_file)


    def test_error_if_nonexistent(self):
        with pytest.raises(RuntimeError):
            utils.resolve_path_to_old_timetables(str_path='foo/bar/baz')