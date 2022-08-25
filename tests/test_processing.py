import pandas as pd
from pathlib import Path
import pytest
from source import processing


class TestLoadTimetable:
    def test_load(self):
        path_to_example_timetable = Path('tests/resources/example_data.xlsx')
        result = processing.load_timetable(path_to_example_timetable)
        expected = pd.read_excel(path_to_example_timetable)

        assert result.equals(expected)


    def test_error_if_wrong_columns(self):
        path_to_example_timetable = Path('tests/resources/bad_columns_data.xlsx')
        with pytest.raises(RuntimeError):
            processing.load_timetable(path_to_example_timetable)


class TestLoadOldRecords:
    def test_load(self):
        path_to_example_records = Path('tests/resources/old_records')
        result = processing.load_old_records(path_to_example_records)
        expected = [
            pd.read_excel(path_to_example_records / '20XX0104.xlsx'),
            pd.read_excel(path_to_example_records / '20XX0103.xlsx'),
            pd.read_excel(path_to_example_records / '20XX0102.xlsx'),
            pd.read_excel(path_to_example_records / '20XX0101.xlsx')
        ]

        for i, expected_df in enumerate(expected):
            assert expected_df.equals(result[i])


class TestCombineRecords:
    def test_combine(self):
        old_records = [
            pd.read_excel('tests/resources/old_records/20XX0102.xlsx'),
            pd.read_excel('tests/resources/old_records/20XX0101.xlsx')
        ]
        result = processing.combine_records(old_records)
        expected = pd.DataFrame(
            columns=['Name','Age','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['D',50,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum'],
                ['E',50,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum'],
                ['F',50,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum'],
                ['A',50,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum'],
                ['B',50,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum'],
                ['C',50,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum']
            ],
            index=pd.Index(['yoink','boink','zoink','foo','bar','baz'], name='Number')
        )

        for column in expected:
            assert result[column].equals(expected[column])
    

    def test_drop_duplicates(self):
        old_records = [
            pd.read_excel('tests/resources/old_records/20XX0103.xlsx'),
            pd.read_excel('tests/resources/old_records/20XX0101.xlsx')
        ]
        result = processing.combine_records(old_records)
        expected = pd.DataFrame(
            columns=['Name','Age','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['A',50,'New','New','New','New'],
                ['B',50,'New','New','New','New'],
                ['C',50,'New','New','New','New']
            ],
            index=pd.Index(['foo','bar','baz'], name='Number')
        )

        for column in expected:
            assert result[column].equals(expected[column])


    def test_dropna(self):
        old_records = [
            pd.read_excel('tests/resources/old_records/20XX0104.xlsx'),
            pd.read_excel('tests/resources/old_records/20XX0101.xlsx')
        ]
        result = processing.combine_records(old_records)
        expected = pd.DataFrame(
            columns=['Name','Age','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['A',50,'Newest','Newest','Newest','Newest'],
                ['B',50,'Newest','Newest','Newest','Newest'],
                ['C',50,'Loren ipsum','Loren ipsum','Loren ipsum','Loren ipsum']
            ],
            index=pd.Index(['foo','bar','baz'], name='Number')
        )

        assert result.equals(expected)


class TestCreatePatientDictionary:
    def test_create(self):
        patient_df = pd.DataFrame(
            columns=['Name','Age','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['A',50,'background_a','rfa_a','imaging_a','tms_a'],
                ['B',50,'background_b','rfa_b','imaging_b','tms_b'],
                ['C',50,'background_c','rfa_c','imaging_c','tms_c']
            ],
            index=pd.Index(['foo','bar','baz'], name='Number')
        )
        result = processing.create_patient_dictionary(patient_df)
        expected = {
            'foo': {
                'Name': 'A',
                'Age': 50,
                'Background': 'background_a',
                'Reason for Attendance': 'rfa_a',
                'Imaging': 'imaging_a',
                'TMs': 'tms_a'
            },
            'bar': {
                'Name': 'B',
                'Age': 50,
                'Background': 'background_b',
                'Reason for Attendance': 'rfa_b',
                'Imaging': 'imaging_b',
                'TMs': 'tms_b'
            },
            'baz': {
                'Name': 'C',
                'Age': 50,
                'Background': 'background_c',
                'Reason for Attendance': 'rfa_c',
                'Imaging': 'imaging_c',
                'TMs': 'tms_c'
            }
        }

        assert result == expected


    def test_error_on_non_unique_index(self):
        patient_df = pd.DataFrame(
            columns=['Name','Age','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['A',50,'background_a','rfa_a','imaging_a','tms_a'],
                ['B',50,'background_b','rfa_b','imaging_b','tms_b'],
                ['C',50,'background_c','rfa_c','imaging_c','tms_c']
            ],
            index=pd.Index(['foo','foo','baz'], name='Number')
        )

        with pytest.raises(AssertionError):
            processing.create_patient_dictionary(patient_df)


    def test_error_on_na_index(self):
        patient_df = pd.DataFrame(
            columns=['Name','Age','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['A',50,'background_a','rfa_a','imaging_a','tms_a'],
                ['B',50,'background_b','rfa_b','imaging_b','tms_b'],
                ['C',50,'background_c','rfa_c','imaging_c','tms_c']
            ],
            index=pd.Index(['foo','bar',None], name='Number')
        )

        with pytest.raises(AssertionError):
            processing.create_patient_dictionary(patient_df)


class TestFillOutTimetable:
    def test_fill_out(self):
        timetable = pd.DataFrame(
            columns=['Time','Number','Name','Age','F2F/TC','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['00:00','foo',None,None,None,None,None,None,None],
                ['00:00','bar',None,None,None,None,None,None,None],
                ['00:00','baz',None,None,None,None,None,None,None]
            ]
        )
        patient_dict = {
            'foo': {
                'Name': 'A',
                'Age': 50,
                'Background': 'background_a',
                'Reason for Attendance': 'rfa_a',
                'Imaging': 'imaging_a',
                'TMs': 'tms_a'
            },
            'bar': {
                'Name': 'B',
                'Age': 50,
                'Background': 'background_b',
                'Reason for Attendance': 'rfa_b',
                'Imaging': 'imaging_b',
                'TMs': 'tms_b'
            },
            'baz': {
                'Name': 'C',
                'Age': 50,
                'Background': 'background_c',
                'Reason for Attendance': 'rfa_c',
                'Imaging': 'imaging_c',
                'TMs': 'tms_c'
            }
        }

        result = processing.fill_out_timetable(
            timetable=timetable,
            patient_dict=patient_dict
        )
        expected = pd.DataFrame(
            columns=['Time','Number','Name','Age','F2F/TC','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['00:00','foo','A',50,None,'background_a','rfa_a','imaging_a','tms_a'],
                ['00:00','bar','B',50,None,'background_b','rfa_b','imaging_b','tms_b'],
                ['00:00','baz','C',50,None,'background_c','rfa_c','imaging_c','tms_c']
            ]
        ).astype(object)

        assert result.equals(expected)

    
    def test_give_up_if_no_previous_data(self):
        timetable = pd.DataFrame(
            columns=['Time','Number','Name','Age','F2F/TC','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['00:00','foo',None,None,None,None,None,None,None],
                ['00:00','bar',None,None,None,None,None,None,None],
                ['00:00','baz',None,None,None,None,None,None,None]
            ]
        )
        patient_dict = {
            'foo': {
                'Name': 'A',
                'Age': 50,
                'Background': 'background_a',
                'Reason for Attendance': 'rfa_a',
                'Imaging': 'imaging_a',
                'TMs': 'tms_a'
            },
            'bar': {
                'Name': 'B',
                'Age': 50,
                'Background': 'background_b',
                'Reason for Attendance': 'rfa_b',
                'Imaging': 'imaging_b',
                'TMs': 'tms_b'
            }
        }

        result = processing.fill_out_timetable(
            timetable=timetable,
            patient_dict=patient_dict
        )
        expected = pd.DataFrame(
            columns=['Time','Number','Name','Age','F2F/TC','Background','Reason for Attendance','Imaging','TMs'],
            data=[
                ['00:00','foo','A',50,None,'background_a','rfa_a','imaging_a','tms_a'],
                ['00:00','bar','B',50,None,'background_b','rfa_b','imaging_b','tms_b'],
                ['00:00','baz',None,None,None,None,None,None,None]
            ]
        ).astype(object)

        assert result.equals(expected)