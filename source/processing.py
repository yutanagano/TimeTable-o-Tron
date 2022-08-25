import pandas as pd
from pathlib import Path


def load_timetable(path_to_timetable: Path) -> pd.DataFrame:
    df = pd.read_excel(path_to_timetable)

    if df.columns.tolist() != [
        'Time',
        'Number',
        'Name',
        'Age',
        'F2F/TC',
        'Background',
        'Reason for Attendance',
        'Imaging',
        'TMs'
    ]:
        raise RuntimeError(
            'Columns of timetable spreadsheets must be of form: [\'Time\', '
            '\'Number\', \'Name\', \'Age\', \'F2F/TC\', \'Background\', '
            f'\'Reason for Attendance\', \'Imaging\', \'TMs\']. Got '
            f'{df.columns.tolist()} for {path_to_timetable}'
        )
    
    return df


def load_old_records(path_to_old_timetables_dir: Path) -> list[pd.DataFrame]:
    # Combine all old records into one dataframe starting with most recent
    records = []

    for f in sorted(path_to_old_timetables_dir.iterdir(), reverse=True):
        if f.suffix == '.xlsx':
            records.append(load_timetable(f))
    
    return records


def combine_records(old_records: list[pd.DataFrame]) -> pd.DataFrame:
    # Keep only the most recent record for every patient
    combined = pd.concat(old_records)
    combined = combined.drop(['Time', 'F2F/TC'], axis=1)
    combined = combined[combined['Number'].notna()]
    combined = combined.drop_duplicates(
        subset='Number',
        keep='first',
        ignore_index=True
    )
    combined = combined.set_index('Number')

    return combined


def create_patient_dictionary(
    patient_df: pd.DataFrame
) -> dict[str, dict]:
    assert patient_df.index.is_unique
    assert patient_df.index.notna().all()

    patient_dict = dict()

    for number, row in patient_df.iterrows():
        patient_dict[number] = {
            'Name': row['Name'],
            'Age': row['Age'],
            'Background': row['Background'],
            'Reason for Attendance': row['Reason for Attendance'],
            'Imaging': row['Imaging'],
            'TMs': row['TMs']
        }
    
    return patient_dict


def fill_out_timetable(
    timetable: pd.DataFrame,
    patient_dict: dict[str, dict]
) -> pd.DataFrame:
    timetable = timetable.copy()

    for i, row in timetable.iterrows():
        patient_number = row['Number']
        try:
            patient_data = patient_dict[patient_number]
        except KeyError:
            continue

        timetable.loc[
            i,
            [
                'Name',
                'Age',
                'Background',
                'Reason for Attendance',
                'Imaging',
                'TMs'
            ]
        ] = pd.Series(patient_data)
    
    return timetable