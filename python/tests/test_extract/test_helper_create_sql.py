from python.src.extract.helper_create_sql import create_sql
from datetime import datetime,timedelta,timezone

class TestCreate_sql:
    def test_create_sql_returns_string(self):
        table = 'test'
        columns=['column1']
        from_time = datetime.now(timezone.utc) - timedelta(minutes=15) 
        to_time = datetime.now(timezone.utc)

        returned = create_sql(table,columns,from_time,to_time)

        assert isinstance(returned,str)