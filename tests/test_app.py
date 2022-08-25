from ttt import main
import pandas as pd
import pytest
import subprocess


@pytest.fixture
def tmp_empty_timetable(tmp_path):
    subprocess.run(['cp', 'tests/resources/example_data_empty.xlsx', tmp_path])
    return tmp_path / 'example_data_empty.xlsx'


class TestApp:
    def test_app(self, tmp_empty_timetable):
        main(
            str_path_to_new_timetable=tmp_empty_timetable,
            str_path_to_old_timetables_dir='tests/resources/old_records'
        )

        result = pd.read_excel(tmp_empty_timetable).astype(object)
        expected = pd.DataFrame(
            columns=['Time','Number','Name','Age','F2F/TC','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                [None,'foo','A',50,None,'Newest','Newest','Newest','Newest'],
                [None,'bar','B',50,None,'Newest','Newest','Newest','Newest'],
                [None,'baz','C',50,None,'New','New','New','New'],
                [None,'yoink','D',50,None,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum'],
                [None,'boink','E',50,None,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum'],
                [None,'zoink','F',50,None,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum']
            ]
        ).astype(object)
        
        assert result.equals(expected)