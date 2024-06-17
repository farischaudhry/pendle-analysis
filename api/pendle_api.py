import requests
import pandas as pd
import io
from base_api import BaseAPI

class PendleAPI(BaseAPI):
    base_url = 'https://api-v2.pendle.finance/core/v4'
    headers = {
        'accept': 'application/json'
    }

    @classmethod
    def fetch_and_save_ohlcv_data_daily(cls, token_name: str, token_address: str, chain_id: int):
        super().fetch_and_save_ohlcv_data_daily(cls.base_url, cls.headers, token_name, token_address, chain_id)

    @classmethod
    def fetch_and_save_ohlcv_data_hourly(cls, token_name: str, token_address: str, chain_id: int):
        super().fetch_and_save_ohlcv_data_hourly(cls.base_url, cls.headers, token_name, token_address, chain_id)

