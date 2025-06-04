from src.transform.load_json import load_json
import pytest
from unittest.mock import patch
import pandas as pd
import awswrangler as wr

class TestLoadJson:
    @patch("src.transform.load_json.wr")
    def test_returns_dataframe(self, wr):
        expected = pd.DataFrame({'key': [1, 2], 'key2': [2, 3]})
        wr.s3.read_json.return_value=expected
        result = load_json('bucket', 'key')
        assert isinstance(result, pd.DataFrame)