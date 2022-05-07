""" Testing file """

import json
from unittest.mock import MagicMock
import sqlite3
import pytest

import main
from main import cursor_to_dict, is_date, valid_dates, write_json


def test_is_date():
    """
    Testing is_date function
    """
    assert is_date("1992-02-29") is True
    assert is_date("1993-02-29") is False
    assert is_date("2012-02-01") is True
    assert is_date("02-1992-01") is False
    assert is_date("1992/02/01") is False


@pytest.mark.parametrize(
    "start, end, expected_value",
    [
        ("2013-11-13", "2014-11-13", True),
        ("2013-01-01", "2013-01-13", True),
        ("2013-01-01", "2013-01-01", True),
        ("2013-01-01", "2010-01-01", False),
        ("2020-01-01", "2010-12-31", False),
    ],
)
def test_valid_dates(start, end, expected_value):
    """
    Testing valid_date function
    """
    assert valid_dates(start, end) == expected_value


def test_write_json(tmpdir):
    """
    Testing write_json function
    """
    data = {
        "customer_id": 57,
        "first_name": "Luis",
        "last_name": "Rojas",
        "total_paid": 46.62,
        "invoices": [
            {"date": "2009-04-04 00:00:00", "amount": 1.98},
            {"date": "2009-05-15 00:00:00", "amount": 13.86},
            {"date": "2010-01-13 00:00:00", "amount": 17.91},
            {"date": "2011-08-20 00:00:00", "amount": 1.98},
            {"date": "2011-11-22 00:00:00", "amount": 3.96},
            {"date": "2012-02-24 00:00:00", "amount": 5.94},
            {"date": "2012-10-14 00:00:00", "amount": 0.99},
        ],
    }

    file = tmpdir.join("output_test.json")
    write_json(data, str(file))
    assert json.load(file) == data


def test_cursor_to_dict():
    """
    Testing sqlite3 cursor result to dictionary
    """
    cursor = MagicMock(sqlite3.Cursor)
    cursor.fetchall.return_value = [
        (6, "Helena", "Holý", "49.62", "2009-07-11 00:00:00", 8.91),
        (6, "Helena", "Holý", "49.62", "2011-02-15 00:00:00", 1.98),
        (6, "Helena", "Holý", "49.62", "2011-05-20 00:00:00", 3.96),
        (6, "Helena", "Holý", "49.62", "2011-08-22 00:00:00", 5.94),
        (6, "Helena", "Holý", "49.62", "2012-04-11 00:00:00", 0.99),
        (6, "Helena", "Holý", "49.62", "2013-10-03 00:00:00", 1.98),
        (6, "Helena", "Holý", "49.62", "2013-11-13 00:00:00", 25.86),
    ]
    query_outupt = cursor.fetchall()
    out_dict = cursor_to_dict(query_outupt)

    output_to_be = [
        {
            "customer_id": 6,
            "first_name": "Helena",
            "last_name": "Holý",
            "total_paid": "49.62",
            "invoices": [
                {"date": "2009-07-11 00:00:00", "amount": "8.91"},
                {"date": "2011-02-15 00:00:00", "amount": "1.98"},
                {"date": "2011-05-20 00:00:00", "amount": "3.96"},
                {"date": "2011-08-22 00:00:00", "amount": "5.94"},
                {"date": "2012-04-11 00:00:00", "amount": "0.99"},
                {"date": "2013-10-03 00:00:00", "amount": "1.98"},
                {"date": "2013-11-13 00:00:00", "amount": "25.86"},
            ],
        }
    ]

    assert out_dict == output_to_be


@pytest.mark.parametrize(
    "start, end, exception, error_message",
    [
        (
            "2013",
            "2013-01-01",
            ValueError,
            "Please provide valide dates in the format YYYY-MM-DDDD",
        ),
        (
            "2013-01-01",
            "01-01",
            ValueError,
            "Please provide valide dates in the format YYYY-MM-DDDD",
        ),
        (
            "2013-01-01",
            "2010-01-01",
            ValueError,
            "The end date must be greater than or equal to the start date",
        ),
        (
            "2020-01-01",
            "2010-12-31",
            ValueError,
            "The end date must be greater than or equal to the start date",
        ),
    ],
)
def test_main_exceptions(start, end, exception, error_message):
    """
    Testing main exceptions
    """
    with pytest.raises(exception) as error:
        main.main(start, end)
        assert error.message == error_message
