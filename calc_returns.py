import sys, getopt, os
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time
import pytz
import logging
import m_logger
import pandas as pd


def Calc_Returns(stock_info, start_date, end_date, logger):

    column_strategy_return = []
    column_bnh_return = []
    if 'Date' not in stock_info.columns.values.tolist() :
        start_dt = stock_info.index[0]
        end_dt = stock_info.index[-1]
    else :
        start_dt = datetime.strptime(stock_info['Date'].iloc[0], '%Y-%m-%d')
        end_dt = datetime.strptime(stock_info['Date'].iloc[-1], '%Y-%m-%d')
        #start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        #end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    days_between = (end_dt - start_dt).days

    final_pnl_value = stock_info['Running_PnL'].iloc[-1] # Retrieve last element
    starting_closing_price = stock_info['close'].iloc[0] # retrieve initial investment
    start_pnl_value = stock_info['close'].iloc[0]
    mantissa = 1+(final_pnl_value/start_pnl_value)
    if mantissa < 0 :
        annualized_return_on_strategy = -1.0
    else :
        annualized_return_on_strategy = (mantissa ** (365/days_between)) - 1
    end_closing_price = stock_info['close'].iloc[-1]
    annualized_buy_hold_return = ((1+((end_closing_price-starting_closing_price)/starting_closing_price)) ** (365/days_between)) - 1
    column_strategy_return.append(str(round((annualized_return_on_strategy * 100),2)))
    column_bnh_return.append(str(round((annualized_buy_hold_return * 100),2)))
    for i in range(1,len(stock_info)) :
        column_strategy_return.append('')
        column_bnh_return.append('')

    stock_info['Strategy_Return'] = pd.Series(column_strategy_return).values
    stock_info['Buy_Hold_Return'] = pd.Series(column_bnh_return).values

    logger.info('Annualized Strategy Return = {strat_ret}'.format(strat_ret = column_strategy_return[0]))
    logger.info('Annualized Buy and Hold Return = {bnh_ret}'.format(bnh_ret = column_bnh_return[0]))

    return stock_info