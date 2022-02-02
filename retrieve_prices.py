
import sys, getopt, os
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time
import pytz
import logging
import m_logger
import pandas as pd
from robot import PyRobot


def retrieve_prices(trading_robot, inputsymbol, start_date, end_date, bar_string, logger) :

    historical_prices_df = trading_robot.grab_historical_prices(
        start=start_date,
        end=end_date,
        bar_string=bar_string,
        symbols=[inputsymbol]
        )

    logger.info("Data Retrieval From Yahoo Finance Complete")

    return historical_prices_df, trading_robot

def read_price_file(file_name, logger) :

    try:
        input_df = pd.read_csv(file_name)
        historical_prices_df = input_df[['Date','symbol','open','high', 'low', 'close', 'volume']].copy()
        #print(historical_prices_df.index.name)
        return historical_prices_df

    except BaseException as e:
        logger.info('The exception: {}'.format(e))
        return pd.DataFrame()

    return historical_prices_df


