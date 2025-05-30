from python.src.extract.helper_create_sql import create_sql, add_where_clause
from datetime import datetime, timedelta, timezone
import pytest


@pytest.fixture(scope="module")
def from_time(to_time):
    return to_time - timedelta(minutes=15)


@pytest.fixture(scope="module")
def to_time():
    return datetime(2025, 5, 29, 12, 30, 00, 1000)


class TestCreate_sql:
    def test_create_sql_returns_string(self, from_time, to_time):
        table = "test"
        returned = create_sql(table, from_time, to_time)
        assert isinstance(returned, str)

    def test_string_begins_with_select_all_from(self, from_time, to_time):
        table = "test"
        start = f"SELECT * FROM {table}"
        returned = create_sql(table, from_time, to_time)
        assert returned.startswith(start)

    def test_protect_table_name_from_injection(self, from_time, to_time):
        table = "test;"
        start = f'SELECT * FROM "{table}"'
        returned = create_sql(table, from_time, to_time)
        assert returned.startswith(start)

    def test_query_ends_with_semicolon(self, from_time, to_time):
        table = "test;"
        returned = create_sql(table, from_time, to_time)
        assert returned.endswith(";")

    def test_query_contains_where_clause(self, from_time, to_time):
        table = "test;"
        returned = create_sql(table, from_time, to_time)
        assert "WHERE" in returned

    def test_query_has_where_clause(self, from_time, to_time):
        # arrage - combined select and where clause
        table = "test"
        start = f"SELECT * FROM {table} "
        add_where = add_where_clause(from_time, to_time)
        expected = start + add_where + ";"
        # act
        returned = create_sql(table, from_time, to_time)
        # assert
        assert returned == expected


class TestAddWhereClause:
    def test_add_where_clause(self, from_time, to_time):
        returned = add_where_clause(from_time, to_time)
        print(from_time, to_time, "test")
        # 2025-05-29 12:30:00.001
        assert isinstance(returned, str)

    def test_where_clause_correct(self, from_time, to_time):
        returned = add_where_clause(from_time, to_time)
        expected = "WHERE last_updated BETWEEN '2025-05-29 12:15:00.001' and '2025-05-29 12:30:00.001'"
        assert returned == expected
