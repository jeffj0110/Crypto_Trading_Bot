
import sys, getopt, os
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time
import pytz
import logging
import m_logger
import pandas as pd



def summary_file(symbol_list, file_name_date_string, logger):

    #Create Summary File
    logger.info("Creating Summary File")
    Summary_df = pd.DataFrame()
    summary_ticker_list = []
    summary_bot_returns = []
    summary_buyhold_returns = []
    summary_transaction_counts = []

    for sym in symbol_list:
        file_name = sym + '_' + file_name_date_string
        if os.path.exists(file_name):
            sym_results = pd.read_csv(file_name)
        else :
            logger.info("File {fn} Not Found For Summary File Generation".format(fn=file_name))
        summary_ticker_list.append(sym_results['symbol'].iloc[0])
        summary_bot_returns.append(sym_results['Strategy_Return'].iloc[0])
        summary_buyhold_returns.append(sym_results['Buy_Hold_Return'].iloc[0])
        buys_sells = len(sym_results[sym_results['buy_sell_condition'].notna()])
        summary_transaction_counts.append(buys_sells)

    Summary_df['Ticker'] = pd.Series(summary_ticker_list).values
    Summary_df["Bot_Algo_Returns"] = pd.Series(summary_bot_returns).values
    Summary_df['Buy_Hold_Returns'] = pd.Series(summary_buyhold_returns).values
    Summary_df['Bot Transaction Count'] = pd.Series(summary_transaction_counts).values

    Output_Summary_File_Name = 'Summary_' + file_name_date_string
    logger.info("Writing Summary File : {fn}".format(fn=Output_Summary_File_Name))
    Summary_df.to_csv(Output_Summary_File_Name)

    return