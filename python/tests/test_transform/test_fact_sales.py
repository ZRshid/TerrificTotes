import pytest
import pandas as pd
from src.transform.fact_sales import sales_facts

@pytest.fixture()
def dummy_sales_order():
    data = {"from_time": "2022-01-02 23:30:00.00", 
            "to_time": "2025-06-02 23:59:59.00", 
            "sales_order": [
                {"sales_order_id": 2, 
                "created_at": "2022-11-03 14:20:52.186000", 
                "last_updated": "2022-11-03 14:20:52.186000", 
                "design_id": 3, 
                "staff_id": 19, 
                "counterparty_id": 8, 
                "units_sold": 42972, 
                "unit_price": "3.94", 
                "currency_id": 2, 
                "agreed_delivery_date": "2022-11-07", 
                "agreed_payment_date": "2022-11-08", 
                "agreed_delivery_location_id": 8}, 
                {"sales_order_id": 3, 
                "created_at": "2022-11-03 14:20:52.188000", 
                "last_updated": "2022-11-03 14:20:52.188000", 
                "design_id": 4, 
                "staff_id": 10, 
                "counterparty_id": 4, 
                "units_sold": 65839, 
                "unit_price": "2.91", 
                "currency_id": 3, 
                "agreed_delivery_date": "2022-11-06", 
                "agreed_payment_date": "2022-11-07", 
                "agreed_delivery_location_id": 19}, 
                {"sales_order_id": 4, 
                "created_at": "2022-11-03 14:20:52.188000", 
                "last_updated": "2022-11-03 14:20:52.188000", 
                "design_id": 4, 
                "staff_id": 10, 
                "counterparty_id": 16, 
                "units_sold": 32069, 
                "unit_price": "3.89", 
                "currency_id": 2, 
                "agreed_delivery_date": "2022-11-05", 
                "agreed_payment_date": "2022-11-07", 
                "agreed_delivery_location_id": 15}, 
                {"sales_order_id": 5, 
                "created_at": "2022-11-03 14:20:52.186000", 
                "last_updated": "2022-11-03 14:20:52.186000", 
                "design_id": 7, 
                "staff_id": 18, 
                "counterparty_id": 4, 
                "units_sold": 49659, 
                "unit_price": "2.41", 
                "currency_id": 3, 
                "agreed_delivery_date": "2022-11-05", 
                "agreed_payment_date": "2022-11-08", 
                "agreed_delivery_location_id": 25}
            ]}
    sales_data = data.get("sales_order", [])
    columns = ["sales_order_id", "created_at", "last_updated", "design_id", "staff_id", 
                "counterparty_id", "units_sold", "unit_price", "currency_id", 
                "agreed_delivery_date", "agreed_payment_date", "agreed_delivery_location_id"]
    df_sales_order = pd.DataFrame(sales_data, columns=columns)
    return df_sales_order

@pytest.fixture()
def dummy_dim_currency():
        data = [{"currency_name": "Afghani", 
                 "currency_code": "AFN", 
                 "currency_id": 0}, 
                {"currency_name": "Euro", 
                 "currency_code": "EUR", 
                 "currency_id": 1},
                {"currency_name": "US Dollar", 
                 "currency_code": "USD", 
                 "currency_id": 2}]
        df_dim_currency = pd.DataFrame(data)
        return df_dim_currency

@pytest.fixture()
def dummy_dim_design():
        data = [{"design_id": 8, 
                 "design_name": "Wooden", 
                 "file_location": "/usr",
                 "file_name": "wooden-20220717-npgz.json"}, 
                {"design_id": 51, 
                 "design_name": "Bronze", 
                 "file_location": "/private",
                 "file_name": "bronze-20221024-4dds.json"},
                {"design_id": 8, 
                 "design_name": "Bronze", 
                 "file_location": "/lost+found",
                 "file_name": "bronze-20230102-r904.json"}]
        df_dim_design = pd.DataFrame(data)
        return df_dim_design

@pytest.fixture()
def dummy_dim_date():
        data = [{"date_id": "2022-11-03", 
                 "year": 2022, 
                 "month": 11,
                 "day": 3,
                 "day_of_week": 3, 
                 "day_name": "Thursday",
                 "month_name": "November",
                 "quarter": 4}, 
                {"date_id": "2022-11-08", 
                 "year": 2022, 
                 "month": 11,
                 "day": 8,
                 "day_of_week": 1, 
                 "day_name": "Tuesday",
                 "month_name": "November",
                 "quarter": 4},
                {"date_id": "2022-11-07", 
                 "year": 2022, 
                 "month": 11,
                 "day": 7,
                 "day_of_week": 0, 
                 "day_name": "Monday",
                 "month_name": "November",
                 "quarter": 4},]
        df_dim_date = pd.DataFrame(data)
        return df_dim_date

@pytest.fixture()
def dummy_dim_location():
        data = [{"location_id":1,
               "address_line_1":"6826 Herzog Via",
               "address_line_2":None,
               "district":"Avon",
               "city":"New Patienceburgh",
               "postal_code":"28441",
               "country":"Turkey",
               "phone":"1803 637401"},
               {"location_id":2,
                "address_line_1":"179 Alexie Cliffs",
                "address_line_2":None,
                "district":None,
                "city":"Aliso Viejo",
                "postal_code":"99305-7380",
                "country":"San Marino",
                "phone":"9621 880720"},
                {"location_id":30,
                 "address_line_1":"0336 Ruthe Heights",
                 "address_line_2":None,
                 "district":"Buckinghamshire",
                 "city":"Lake Myrlfurt",
                 "postal_code":"94545-4284",
                 "country":"Falkland Islands (Malvinas)",
                 "phone":"1083 286132"}
                ]

        df_dim_location = pd.DataFrame(data)
        return df_dim_location

@pytest.fixture()
def dummy_dim_counterparty():
        data = [{"counterparty_id":1,
                 "counterparty_legal_name":"Fahey and Sons",
                 "counterparty_legal_address_line_1":"605 Haskell Trafficway",
                 "counterparty_legal_address_line_2":"Axel Freeway",
                 "counterparty_legal_district":None,
                 "counterparty_legal_city":"East Bobbie",
                 "counterparty_legal_postal_code":"88253-4257",
                 "counterparty_legal_country":"Heard Island and McDonald Islands",
                 "counterparty_legal_phone_number":"9687 937447"},
                 {"counterparty_id":2,
                  "counterparty_legal_name":"Leannon, Predovic and Morar",
                  "counterparty_legal_address_line_1":"079 Horacio Landing",
                  "counterparty_legal_address_line_2":None,
                  "counterparty_legal_district":None,
                  "counterparty_legal_city":"Utica",
                  "counterparty_legal_postal_code":"93045",
                  "counterparty_legal_country":"Austria",
                  "counterparty_legal_phone_number":"7772 084705"}
               ]
        
        dummy_dim_counterparty = pd.DataFrame(data)
        return dummy_dim_counterparty

@pytest.fixture()
def dummy_dim_staff():
        data = [{"staff_id":1,
                 "first_name":"Jeremie",
                 "last_name":"Franey",
                 "email_address":"jeremie.franey@terrifictotes.com",
                 "location":"Manchester2",
                 "department_name":"Purchasing"},
                {"staff_id":2,
                 "first_name":"Deron",
                 "last_name":"Beier",
                 "email_address":"deron.beier@terrifictotes.com",
                 "location":"Leeds",
                 "department_name":"distribution"}
               ]
        
        dummy_dim_staff = pd.DataFrame(data)
        return dummy_dim_staff

class TestSales_facts:
    def test_function_returns_a_dataframe(self, dummy_sales_order):
        
        df_sales_facts = sales_facts(dummy_sales_order)
        assert isinstance(df_sales_facts,pd.DataFrame)


    def test_dataframe_has_the_correct_columns(self, dummy_sales_order):
        
        expected_columns = ["sales_record_id", "sales_order_id", "created_date", "created_time", 
                            "last_updated_date", "last_updated_time", "sales_staff_id", "counterparty_id",
                            "units_sold", "unit_price", "currency_id", "design_id", "agreed_payment_date",
                            "agreed_delivery_date", "agreed_delivery_location_id"]
                
        df_sales_facts = sales_facts(dummy_sales_order)

        assert list(df_sales_facts.columns) == expected_columns
    
    def test_dataframe_has_the_correct_number_of_rows(self, dummy_sales_order):
        df_sales_facts = sales_facts(dummy_sales_order)

        assert df_sales_facts.shape[0] == 4

    def test_dataframe_has_the_correct_number_of_columns(self, dummy_sales_order):
        df_sales_facts = sales_facts(dummy_sales_order)
        print(df_sales_facts.columns)
        assert df_sales_facts.shape[1] == 15

    def test_function_returns_an_error_when_table_is_not_generated(self, dummy_sales_order):
        with pytest.raises(Exception):
            sales_facts([dummy_sales_order])
