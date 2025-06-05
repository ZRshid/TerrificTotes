import pandas as pd
import pytest
from src.transform.transform_staff import transform_staff_with_department, NullInDataFrameException
EXAMPLE_STAFF = {"staff": [
                    {"staff_id": 1, "first_name": "Jeremie", "last_name": "Franey", "department_id": 2, "email_address": "jeremie.franey@terrifictotes.com", "created_at": "2022-11-03 14:20:51.563000", "last_updated": "2022-11-03 14:20:51.563000"},
                    {"staff_id": 2, "first_name": "Deron", "last_name": "Beier", "department_id": 6, "email_address": "deron.beier@terrifictotes.com", "created_at": "2022-11-03 14:20:51.563000", "last_updated": "2022-11-03 14:20:51.563000"}
                   ]
}

EXAMPLE_DEPT = {"department": [
    {"department_id": 1, "department_name": "Sales", "location": "Manchester", "manager": "Richard Roma", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"},
    {"department_id": 2, "department_name": "Purchasing", "location": "Manchester2", "manager": "Naomi Lapaglia", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"},
    {"department_id": 6, "department_name": "distribution", "location": "Leeds", "manager": "Richard Roma", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"},
    ]
}

@pytest.fixture()
def staff_df(autoapply=True):
    return pd.DataFrame(EXAMPLE_STAFF["staff"])

@pytest.fixture()
def dept_df(autoapply=True):
    return pd.DataFrame(EXAMPLE_DEPT["department"])

class TestTransform_staff_with_department():
    def test_returns_a_dataframe(self,staff_df,dept_df):
        returned_df = transform_staff_with_department(staff_df,dept_df)
        assert isinstance(returned_df,pd.DataFrame)
    def test_returns_a_different_dataframe(self,staff_df,dept_df):
        returned_df = transform_staff_with_department(staff_df,dept_df)
        assert returned_df is not staff_df
        assert returned_df is not dept_df
    def test_returns_correct_columns(self,staff_df,dept_df):
        expected_columns = ["staff_id", "first_name", "last_name", "department_name","location", "email_address",]
        returned_df = transform_staff_with_department(staff_df,dept_df)
        for name in expected_columns:
            assert name in returned_df.columns
    def test_returns_6_colunms_and_2_rows(self,staff_df,dept_df):
        returned_df = transform_staff_with_department(staff_df,dept_df)
        
        assert returned_df.shape == (2,6) #(rows,columns)
    def test_person_at_correct_location(self,staff_df,dept_df):
        expected_location = 'Leeds'
        person = 'Deron'
        
        returned_df = transform_staff_with_department(staff_df,dept_df)
        
        returned_df.set_index('first_name', inplace=True)
        location = returned_df.loc[person]['location']
        
        assert  location == expected_location
    def test_raised_if_department_id_is_missing(self,staff_df,dept_df):
        expected_location = 'Leeds'
        person = 'Deron'
        staff_df.loc[staff_df['first_name'] == person, 'department_id'] = 26
        with pytest.raises(NullInDataFrameException) as exc:
            returned_df = transform_staff_with_department(staff_df,dept_df)
        

