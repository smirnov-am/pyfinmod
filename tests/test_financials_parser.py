import os
import json
from json import JSONDecodeError
from datetime import date
import pandas as pd
import pytest
from pyfinmod.financials import Financials, ParserError

raw_data_dir = os.path.join(os.path.dirname(__file__), 'raw_data')


def test_date_parser():
    assert Financials._date_parse("2018-9-29") == date(2018, 9, 29)


def test_json_to_df():
    with open(os.path.join(raw_data_dir, "aapl_balance_sheet.json"), "r") as f:
        json_data = json.load(f)

    results = Financials._json_to_df(json_data)
    expected = pd.read_hdf(os.path.join(raw_data_dir, "aapl_balance_sheet.hdf"), key="aapl_balance_sheet")
    assert results.equals(expected)


def test_fetch_json():
    parser = Financials("AAPL")
    parser.datatypes["balance_sheet_statement"] = "NotaValidURL"
    parser.datatypes["cash_flow_statement"] = "https://www.google.com"
 
    # Wrong url should raise ParseError
    with pytest.raises(ParserError):
        parser._fetch_json("balance_sheet_statement")
    with pytest.raises(JSONDecodeError):
        parser._fetch_json("cash_flow_statement")


def test_get_balance_sheet():
    parser = Financials("AAPL")
    with open(os.path.join(raw_data_dir, "aapl_balance_sheet.json"), "r") as f:
        json_data = json.load(f)

    parser._fetch_json = lambda x: {"financials": json_data}

    results = parser.balance_sheet_statement
    assert not results.empty

    expected = pd.read_hdf(os.path.join(raw_data_dir, "aapl_balance_sheet.hdf"), key="aapl_balance_sheet")
    assert results.equals(expected)

    # test cached value
    parser._fetch_json = None
    results = parser.balance_sheet_statement
    assert results.equals(expected)


def test_get_income_statement():
    parser = Financials("AAPL")
    with open(os.path.join(raw_data_dir, "aapl_income_statement.json"), "r") as f:
        json_data = json.load(f)
    parser._fetch_json = lambda x: json_data

    results = parser.income_statement
    assert not results.empty

    expected = pd.read_hdf(os.path.join(raw_data_dir, "aapl_income_statement.hdf"), key="aapl_income_statement")
    assert results.equals(expected)

    # test cached value
    parser._fetch_json = None
    results = parser.income_statement
    assert results.equals(expected)


def test_get_cash_flow():
    parser = Financials("AAPL")
    with open(os.path.join(raw_data_dir, "aapl_cash_flow.json"), "r") as f:
        json_data = json.load(f)
    parser._fetch_json = lambda x: json_data

    results = parser.cash_flow_statement
    assert not results.empty

    expected = pd.read_hdf(os.path.join(raw_data_dir, "aapl_cash_flow.hdf"), key="aapl_cash_flow")
    assert results.equals(expected)

    # test cached value
    parser._fetch_json = None
    results = parser.cash_flow_statement
    assert results.equals(expected)


def test_get_market_cap():
    parser = Financials("AAPL")
    with open(os.path.join(raw_data_dir, "aapl_summary.json"), "r") as f:
        json_data = json.load(f)
    parser._fetch_json = lambda x: json_data
    results = parser.mktCap
    assert results == float(1230468047640.00)

    # test cached value
    parser._fetch_json = None
    results = parser.mktCap
    assert results == float(1230468047640.00)
