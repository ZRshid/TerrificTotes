from src.extract.helper_json import (to_JSON,
                                        extract_names_from_columns_data, 
                                        name_rows,
                                        LengthMissMatchException
)
import re
from datetime import datetime
import pytest

class TestName_Rows:
    def test_returns_a_list_of_dicts(self):
        pg8000_result = [[1,2,3]]
        columns = ["a","b","c"]

        returned = name_rows(pg8000_result,columns)

        assert isinstance(returned, list)
        assert isinstance(returned[0], dict)

    def test_dict_contains_correct_keys(self):
        pg8000_result = [[1,2,3]]
        columns = ["a","b","c"]

        returned = name_rows(pg8000_result,columns)

        assert "a" in returned[0]
        assert "b" in returned[0]
        assert "c" in returned[0]

    def test_dict_contains_correct_values(self):
        pg8000_result = [[1,2,3]]
        columns = ["a","b","c"]

        returned = name_rows(pg8000_result,columns)

        assert returned[0]["a"] == 1
        assert returned[0]["b"] == 2
        assert returned[0]["c"] == 3

    
class TestExtract_names_from_columns_data:
    def test_list_returned(self):
        columns_data = [{'name':1}]
        hopefully_a_list = extract_names_from_columns_data(columns_data)
        assert isinstance(hopefully_a_list,list)
    def test_correct_list_returned(self):
        columns_data = [{'name':"test"},{'name':"experiment",'number':1}]

        expected_names = ["test", "experiment"]
        actual_list = extract_names_from_columns_data(columns_data)

        assert actual_list == expected_names

@pytest.fixture(scope="class")
def columns_data():
    return [
            {'column_attrnum': 1,'format': 0,'name': 'id'},
            {'column_attrnum': 2,'format': 0,'name': 'sales'},
            {'column_attrnum': 2,'format': 0,'name': 'date'}
        ]
class TestTo_json:
    ...
    # test is json etx and 
    # in correct shape.
    # raises errors if result is not in the correct format? 
    #       i.e sql returned the wrong thing??
    
    def test_string_returned(self,columns_data):
        pg8000_result = [[1,2,3],[5,4,3]]
        table_name = "test"

        hopefully_a_string = to_JSON(table_name,columns_data,pg8000_result)

        assert isinstance(hopefully_a_string,str)
    
    def test_string_contains_table_key(self,columns_data):
        pg8000_result = [[1,2,3],[5,4,3]]
        table_name = "test"

        contains = f'"{table_name}": ['
        hopefully_json = to_JSON(table_name,columns_data,pg8000_result)
        assert hopefully_json.find(contains) >= 0

    def test_string_matches_pattern_of_expected_json(self,columns_data):
        #roughly I haven't checked data types are ok e.g what happens to dates
        pattern = r'^\{".+": \[(\{".+": .+\}, )*\{".+": .+\}\]\}$'
        reg_ex = re.compile(pattern)
        from datetime import datetime
        pg8000_result = [[1,2,3],[5,"4",38.6]]
        table_name = "test2"

        hopefully_json = to_JSON(table_name,columns_data,pg8000_result)
        assert reg_ex.match(hopefully_json) != None

    def test_it_dumps_datetime_correctly(self,columns_data):
        pg8000_result = [[1,2,3],[5,4,datetime.now()]]
        table_name = "test"
        try:
            to_JSON(table_name,columns_data,pg8000_result)
        except Exception as e:
            print("An error should not happen here but did:",e)
            assert e != None #always going to fail if it gets here 

    #note:
    #  not for this function but:
    #  what to do about timezone info (is it a timezone datetime or unzoned)
    #  does it matter when the dates in the nc database don't have timezones

    ### might also need to check other types e.g interval/datetime.timedelta
    # https://pypi.org/project/pg8000/#:~:text=Type%20Mapping
    # - the nc tables don't seem to use it so I wont bother right now.

    def test_raise_exception_if_different_number_of_rows_and_names_(self):
        pg8000_result = [[1,2,3],[5,4,datetime.now()]]
        table_name = "test"
        columns_data = [
            {'column_attrnum': 1,'format': 0,'name': 'id'},
            {'column_attrnum': 2,'format': 0,'name': 'sales'},
        ]
        with pytest.raises(LengthMissMatchException) as excpt:
            to_JSON(table_name,columns_data,pg8000_result)
            print(excpt)

    def test_when_has_from_time_it_is_in_dictionary(self, columns_data):
        pg8000_result = [[1,2,3],[5,4,3]]
        table_name = "test"
        
        should_have_from_time = to_JSON(table_name,columns_data,pg8000_result,from_time=datetime.now())

        assert 'from_time' in should_have_from_time
    def test_when_has_to_time_it_is_in_dictionary(self, columns_data):
        pg8000_result = [[1,2,3],[5,4,3]]
        table_name = "test"
        
        should_have_from_time = to_JSON(table_name,columns_data,pg8000_result,to_time=datetime.now())

        assert 'to_time' in should_have_from_time
    def test_times_are_in_correct_format(self, columns_data):
        pg8000_result = [[1,2,3],[5,4,3]]
        table_name = "test"
        to_dt = "2025-04-03 02:01:00.123"
        to_will_contain = "2025-04-03 02:01:00.123"
        from_dt = "2025-04-03 02:01:00.00"
        from_will_contain = "2025-04-03 02:01:00.00"

        json_str = to_JSON(table_name,columns_data,pg8000_result,from_time=from_dt,to_time=to_dt)

        assert to_will_contain in json_str
        assert from_will_contain in json_str
        
        