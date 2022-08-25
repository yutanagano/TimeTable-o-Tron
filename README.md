# TimeTable-o-Tron

This is a command-line program designed to automate a particular timetabling
process. The program expects two things:

1. A path to an existing timetable, which has patient-numbers filled in but not
necessarily other information.
2. A path to a directory containing timetables from the past, which are already
filled out.

The program then looks through the directory of old timetables, and retreives
the most recent information for all past patients. Then, using this
information, the program figures out if any of the cells in the new, empty
timetable can be filled with past patient data. If so, the program will fill
out the relevant cells. If the patient is not found in any of the past
timetables, the program will leave those patients' rows as is (blank).

## Timetable format

The timetables are all expected to be in Microsoft Excel format, specifically
`.xlsx`.

Furthermore the timetables, both old and new, are expected to have table
headers which *strictly* follow the below format:

|Time|Number|Name|Age|F2F/TC|Background|Reason for Attendance|Imaging|TMs|
|-|-|-|-|-|-|-|-|-|
|00:00|###|Josephine Smith|50|Loren ipsum|Loren ipsum|Reason|Loren ipsum|Loren ipsum|

> The table contents do not have to be in a particular format. Only the headers
> have to follow the above format.

## More on program behaviour

The program will use the values in the "Number" column to attempt to uniquely
identify patients. This meanst that for a row to be filled out, its "Number"
cell must contain the relevant and correct patient number.

The program will attempt to fill in patient data for the following columns,
based on what it can find from the patient's most recent records.

- Name
- Age
- Background
- Reason for attendance
- Imaging
- TMs

> This means that the "Time" and "F2F/TC" columns will never be filled.

### ***IMPORTANT***: How the program decides what information is "recent"

When reading through the old patient records, the program will decide which
data is most recent based on the name of the timetable. That is, the program
will sort the contents of the old records directory alphabetically, and assume
that the files that end up at the bottom are the most recent. This is because,
given a YYYY-MM-DD or similar naming format for the old timetables, the file
names corresponding to the latest dates will be sorted to the bottom. So, to
preserve the behaviour of the program retreiving the most recent information,
please make sure that the old record timetables are named in this way.

## Installation

1. Install python 3 onto your system, if not available already.
2. Git clone this repository onto your local system, at whatever desired
location.
3. Install the required python module dependencies. This can be done by simply
executing the following command from within this project directory:

```
$ python3 -m pip install -r requirements.txt
```

Or to do the same manually:

```
$ python3 -m pip install pandas openpyxl
```

> It may be useful to install these python dependencies in a python virtual 
> environment, so as not to pollute the main system python.

4. Done! Now, the program can be run via the command line from the project
directory using the command:

```
$ python3 ttt.py
```

> To see the command line help menu, try `python3 ttt.py --help`.

## Command line help menu
```
$ python3 ttt.py -h
usage: ttt.py [-h] new_timetable old_timetables_dir

TimeTable-o-Tron (TTT)

positional arguments:
  new_timetable         Path to the new (pre-filled) timetable. The script
                        expects an excel file (xlsx) with the colums: ["Time",
                        "Number", "Name", "Age", "F2F/TC", "Background",
                        "Reason for Attendance", "Imaging", "TMs"] in this
                        order. Based on the existing values in the "Number"
                        column of this new timetable specified, the script will
                        attempt to auto-fill missing values for the rest of the
                        columns, using data from previous dates' timetables.
  old_timetables_dir    Path to a directory (i.e. folder) containing previous
                        dates' timetables, similarly formatted as above. The
                        script will use this directory to look for information
                        on patients specified in the new timetable, to see if
                        it can fill in the patient data for you.

options:
  -h, --help            show this help message and exit
```