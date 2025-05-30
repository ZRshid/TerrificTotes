from python.src.extract.helper_create_sql import create_sql
from python.src.extract.connection import close_db, query_db
from datetime import datetime
import pytest
from unittest import mock
from pg8000.native import InterfaceError, DatabaseError


@pytest.fixture
def mock_db_conn():
    mock_conn = mock.Mock()
    mock_conn.run.return_value = [
        ("2022-11-03 14:20:52", "1"),
        ("2022-11-18 12:27:09", "2"),
    ]
    mock_conn.columns = ["timestamp", "id"]
    return mock_conn


def test_returns_correct_datatype(mock_db_conn):
    table = "sales_order"
    from_time = datetime(2022, 11, 3, 14, 20, 52, 186000)
    to_time = datetime(2022, 11, 18, 12, 27, 9, 924000)
    with mock.patch(
        "python.src.extract.connection.connect_to_db", return_value=mock_db_conn
    ):
        query = create_sql(table, from_time, to_time)
        result = query_db(query, mock_db_conn)
        # formatted_result = format_result(result)
    close_db(mock_db_conn)
    assert isinstance(result, tuple)
    assert isinstance(result[0], list)
    assert isinstance(result[1], list)


def test_database_error_raises(mock_db_conn):
    table = "sales_order"
    from_time = datetime(2022, 11, 3, 14, 20, 52, 186000)
    to_time = datetime(2022, 11, 18, 12, 27, 9, 924000)
    close_db(mock_db_conn)
    with pytest.raises(DatabaseError) as d:
        conn = mock.Mock()
        conn.run.side_effect = DatabaseError()
        query = create_sql(table, from_time, to_time)
        result = query_db(query, conn)
        close_db(conn)


def test_interface_error_raises(mock_db_conn):
    table = "sales_order"
    from_time = datetime(2022, 11, 3, 14, 20, 52, 186000)
    to_time = datetime(2022, 11, 18, 12, 27, 9, 924000)
    close_db(mock_db_conn)
    with pytest.raises(InterfaceError) as i:
        conn = mock.Mock()
        conn.run.side_effect = InterfaceError()
        query = create_sql(table, from_time, to_time)
        result = query_db(query, conn)
        close_db(conn)
