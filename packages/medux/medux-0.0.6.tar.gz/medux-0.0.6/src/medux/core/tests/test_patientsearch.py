import pytest

from django.utils.timezone import datetime
from medux.utils import parse_date_string


# TODO test other localizations after implementing them - MMDDYY etc.
def test_parse_date_string_ddmmyyyy():
    assert parse_date_string("12111978") == datetime(1978, 11, 12).date()


def test_parse_date_string_ddmmyyyy_with_dots():
    assert parse_date_string("12.11.1978") == datetime(1978, 11, 12).date()


def test_parse_date_string_ddmmyy():
    assert parse_date_string("121178") == datetime(1978, 11, 12).date()


def test_parse_date_string_ddmmyy_with_dots():
    assert parse_date_string("12.11.78") == datetime(1978, 11, 12).date()


def test_parse_date_string_svnr():
    assert parse_date_string("1234150456") == datetime(1956, 4, 15).date()


def test_parse_date_string_wrong_format():
    assert parse_date_string("123456") == None
