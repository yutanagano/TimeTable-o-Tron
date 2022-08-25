import argparse
from source import utils
from source import processing


def parse_command_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='TimeTable-o-Tron (TTT)'
    )

    parser.add_argument(
        'new_timetable',
        help='Path to the new (pre-filled) timetable. The script expects an '
            'excel file (xlsx) with the colums: ["Time", "Number", "Name", '
            '"Age", "F2F/TC", "Background", "Reason for Attendance", "Imaging"'
            ', "TMs"] in this order. Based on the existing values in the '
            '"Number" column of this new timetable specified, the script will '
            'attempt to auto-fill missing values for the rest of the columns, '
            'using data from previous dates\' timetables.'
    )
    parser.add_argument(
        'old_timetables_dir',
        help='Path to a directory (i.e. folder) containing previous dates\' '
            'timetables, similarly formatted as above. The script will use '
            'this directory to look for information on patients specified in '
            'the new timetable, to see if it can fill in the patient data for '
            'you.'
    )

    args = parser.parse_args()

    return args


def main(str_path_to_new_timetable: str, str_path_to_old_timetables_dir: str):
    path_to_new_timetable = utils.resolve_path_to_new_timetable(str_path_to_new_timetable)
    path_to_old_timetables = utils.resolve_path_to_old_timetables(str_path_to_old_timetables_dir)

    new_timetable = processing.load_timetable(path_to_new_timetable)

    old_records = processing.load_old_records(path_to_old_timetables)
    old_records_combined = processing.combine_records(old_records)
    patient_dict = processing.create_patient_dictionary(old_records_combined)

    new_timetable = processing.fill_out_timetable(new_timetable, patient_dict)

    new_timetable.to_excel(path_to_new_timetable, index=False)


if __name__ == '__main__':
    args = parse_command_line_arguments()

    main(args.new_timetable, args.old_timetables_dir)