import fetch_data as fd
import pandas as pd
import numpy as np
from datetime import datetime


class dcf_model:
    def __init__(self, symbol):
        self.cash_flow_statement = fd.get_cash_flow_statement(symbol)
        self.balance_sheet = fd.get_balance_sheet(symbol)
        self.income_statement = fd.get_income_statement(symbol)
        self.symbol = symbol

        df_index = [
            'EBIT',
            'Tax',
            'D&A',
            'Change in NWC',
            'Capex',
            'UFCF'
        ]

        #create empty dcf df, then format it to be Q1, Q2, Q3, Q4
        df_columns = self.income_statement['fiscalDateEnding'].tolist()
        df_columns = [dcf_model.convert_to_quarter_format(x) for x in df_columns]
        self.dcf_model_df = pd.DataFrame(index=df_index, columns=df_columns)
        self.populate_df()



    def convert_to_quarter_format(date_str):
        """
        :param: date_str: a string in the format of YYYY-MM-DD
        :return: a string in the format of YYYYQ#
        """
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        year = date_obj.year
        month = date_obj.month
        quarter = (month - 1) // 3 + 1
        return f"{year}Q{quarter}"


    def populate_df(self):
        #populate EBIT column
        self.dcf_model_df.loc['EBIT'] = self.income_statement['ebit'].tolist()
        #populate Tax column
        self.dcf_model_df.loc['Tax'] = self.income_statement['incomeTaxExpense'].tolist()
        #populate D&A column
        self.dcf_model_df.loc['D&A'] = self.income_statement['depreciationAndAmortization'].tolist()
        
        