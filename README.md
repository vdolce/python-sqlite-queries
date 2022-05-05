# python-sqlite-queries

This Python program uses this [database](https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql) to get customer invoice payments data and writes it to a JSON file.
The DB was filled using the `db/Chinook_Sqlite.sql` script.

Invoices payments can be filtered for a specific time periods and they are sorted by `total_paid` amount in descending order. The JSON filename includes the timestamp of when the script was executed in the format `invoice_payments_YYYYMMDD_hh_mm_ss.json`.

The JSON output will be the following format:

```json
[
    {
        "customer_id": 57,
        "first_name": "Luis",
        "last_name": "Rojas",
        "total_paid": 46.62,
        "individual_payments": [
            {
                "date": "2009-04-04 00:00:00",
                "amount": 1.98
            },
            {
                "date": "2009-05-15 00:00:00",
                "amount": 13.86
            },
            {
                "date": "2010-01-13 00:00:00",
                "amount": 17.91
            },
            {
                "date": "2011-08-20 00:00:00",
                "amount": 1.98
            },
            {
                "date": "2011-11-22 00:00:00",
                "amount": 3.96
            },
            {
                "date": "2012-02-24 00:00:00",
                "amount": 5.94
            },
            {
                "date": "2012-10-14 00:00:00",
                "amount": 0.99
            }
        ]
    },
    ...
]
```

## Installation

Make sure to have Python 3.9 installed in your computer. For this project, the Python version used is 3.9.7.

Start creating a virtual environment with the command

```bash
python -m venv venv
```

Then activate the virtual environment

```bash
 source venv/bin/activate
```

When you need to deactivate the venv, just run `deactivate`

All the Python packages used for the project are saved in the `requirements.txt` file. To install them, run the following command:

```
pip install -r requirements.txt
```

## How to run

```bash
python main.py [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```

`start` and `end` parameters are optional: you can pass both of them, one of them or neither.

## Packages

The following built-in packages were used:

- `json` to dump a json file
- `sqlite3` to connect to the sqlite database and run queries
- `os` to access the operating system and manage files

The following external packages were used in the project:

- `python-dateutil` to work easily with dates
- `pytest` to run code tests
- `black` to format the code
- `mypy` for type and syntax checking
- `pylint` to avoid bugs, code smells. it helps to code in a standard way.

## Structure

- `main.py` contains all the logic and functionalities
- `queries.py` contains the queries strings
- `test.py` contains the tests for some of the functions of the main file
- `/db` contains the sqlite database
- `/dumps` contains the dumped json files (if it does not exist, it will be created)

The program uses the built-in sqlite3 to open a DB connection and run a query using the function `open_db_connection()`, `execute_query()` and `close_db_connection()`. Using python to inject the query, the execute_query function returns a `sqlite3.Cursor`, which is an iterable of tuples.
The injected query is called `FILTERED_INVOICES_QUERY` and it's used for all the cases.

The Cursor will be processed by the function `cursor_to_dict()` that will create a list of dictionaries that follow the required json structure.

Finally, the function `write_json()` will dump the previous list of dictionaries into a JSON file: the filename will contain the current datetime, following the format `invoice_payments_YYYYMMDD_hh_mm_ss.json`.

The program validates the input dates using the function `is_date()` and `valid_dates()`: if the dates are not valid, an exception is raised.
Both dates need to be passed valid or neither of them.
