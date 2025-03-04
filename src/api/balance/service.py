from datetime import datetime

from src.core.ocr import DailyBalanceFetcher

class BalanceResultService:

    def __init__(self):
        self.daily_fetcher = DailyBalanceFetcher()

    def operate_single_file(self, file_name: str):
        results = self.daily_fetcher.single_extract(file_name=file_name)

    def operate_batch(self):
        results = self.daily_fetcher.batch_extract_daily_balances()