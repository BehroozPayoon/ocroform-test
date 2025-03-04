import re
import os
from datetime import datetime

import PyPDF2
import pandas as pd


class DailyBalanceFetcher:

    def __init__(self, file_name: str = None):
        self.file_name = file_name
        self.pdf_directory = './pdf_files'

    def extract_daily_balances(self, pdf_path):
        """
        Extract daily balances from a single PDF file

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            list or DataFrame of daily balances
        """
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                daily_balances = []

                for page in reader.pages:
                    text = page.extract_text()
                    balance_pattern = r'(\d{2}/\d{2}/\d{4})\s*([-]?\$?[\d,]+\.\d{2})'
                    matches = re.findall(balance_pattern, text)
                    daily_balances.extend(matches)

            return daily_balances
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []

    def batch_extract_daily_balances(self):
        all_balances = []

        for file_name in os.listdir(self.pdf_directory):
            if file_name.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, file_name)
                balances = self.extract_daily_balances(pdf_path)
                enriched_balances = [
                    (*balance, file_name) for balance in balances
                ]
                all_balances.extend(enriched_balances)

        return self._format_result(all_balances)

    def operate(self):
        if self.file_name:
            pdf_path = os.path.join(self.pdf_directory, self.file_name)
            balances = self.extract_daily_balances(pdf_path)
            result = [
                (*balance, self.file_name) for balance in balances
            ]
            return self._format_result(result)
        else:
            return self.batch_extract_daily_balances()

    def _format_result(self, balances):
        df = pd.DataFrame(
            balances,
            columns=['Date', 'Balance', 'Source File']
        )
        df.to_csv(f'results/{datetime.now()}.csv', index=False)
        return df
