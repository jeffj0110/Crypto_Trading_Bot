import sys, getopt, os
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time
import pytz
import logging
import m_logger
import pandas as pd

from functions import setup_func

from indicator_calcs import Indicators
#from save_sp500_tickers import save_sp500_tickers
from calc_returns import Calc_Returns
from retrieve_prices import retrieve_prices, read_price_file
from summary_file import summary_file


def Run_Model(inputsymbol, start_date, end_date, logger, historical_prices_df, file_name) :

    symbol = inputsymbol

    # Convert data to a Data StockFrame.
    if len(historical_prices_df) == 0 :
        logger.info("No Data Returned")
        sys.exit(-1)

    # Create an indicator Object.
    indicator_client = Indicators(symbol, input_price_data_frame=historical_prices_df, lgfile=logger)

    stock_info_df = indicator_client.refresh(symbol)

    stock_info_df = Calc_Returns(symbol, stock_info_df, start_date, end_date, logger)

    full_path = file_name

    logger.info('Starting to write spreadsheet to {fname}'.format(fname=full_path))

    # Save an excel sheet with the data
    stock_info_df.to_csv(full_path)

    logger.info('Finished writing spreadsheet')

    return stock_info_df




# Check to see if this file is being executed as the "Main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
#
def main(argv):
    inputsymbol = ''
    bar_string = ''
    start_date = ''
    end_date = ''
    input_ticker_file = ''

#    Yahoo_GetOHLC -t ticker -s <start_date> -e <end_date> -b <bar_string>
#    <start_date> : a date in the format of YYYY-MM-DD that historical data should start from
#    <end_date> : a date in the format of YYYY-MM-DD that historical data should end
#    bar string -- possible value-- 1min, 2min, 3min, 5min, 10min, 15min, 30min, 1h, 2h, 3h, 4h, 8h, 1d, 1w, 1m
    try:
       opts, args = getopt.getopt(argv,"ht:s:e:b:i:")
    except getopt.GetoptError:
       print('Yahoo_GetOHLC -i input_ticker_file -t ticker -s <start_date> -e <end_date> -b <bar_string>')
       print('<start_date> : a date in the format of YYYY-MM-DD that historical data should start from')
       print('<end_date> : a date in the format of YYYY-MM-DD that historical data should end')
       print('input_ticker_file : if you do not specify an input_ticker_file then you need to specify a -t ticker')
       print('<bar string> : possible value-- 1min, 2min, 3min, 5min, 10min, 15min, 30min, 1h, 2h, 3h, 4h, 8h, 1d, 1w, 1m')
       print('See Yahoo Finance For Data Limits')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print('Yahoo_GetOHLC -i input_ticker_file -t ticker -s <start_date> -e <end_date> -b <bar_string>')
          print('<start_date> : a date in the format of YYYY-MM-DD that historical data should start from')
          print('<end_date> : a date in the format of YYYY-MM-DD that historical data should end')
          print('input_ticker_file : if you do not specify an input_ticker_file then you need to specify a -t ticker')

          print('<bar string> : possible value-- 1min, 2min, 3min, 5min, 10min, 15min, 30min, 1h, 2h, 3h, 4h, 8h, 1d, 1w, 1m')
          print('See Yahoo Finance For Data Limits')
          sys.exit()
       elif opt in ("-t", "-T"):
           inputsymbol = arg
       elif opt in ("-s"):
           start_date = arg
       elif opt in ("-e"):
           end_date = arg
       elif opt in ("-b") :
           bar_string = arg
       elif opt in ("-i") :
           input_ticker_file = arg

    if input_ticker_file == '' :
        if inputsymbol == '' :
            inputsymbol = "No_Sym_Defined"
    if bar_string == '' :
        bar_string = "No_Bar_Defined"
    if start_date == '' :
        start_date = 'No_Start_Date_defined'
    if end_date == '' :
        end_date = 'No_End_Date_defined'
    # J. Jones
    # Setting up a logging service for the bot to be able to retrieve
    # runtime messages from a log file
    est_tz = pytz.timezone('US/Eastern')
    now = datetime.now(est_tz).strftime("%Y_%m_%d-%H%M%S")
    if input_ticker_file != '' :
        logfilename = "{}_logfile_{}".format('input_file', now)
    else :
        logfilename = "{}_logfile_{}".format(inputsymbol, now)
    logfilename = logfilename + ".txt"
    logger = m_logger.getlogger(logfilename)

    if inputsymbol == "No_Sym_Defined" :
       logger.info("Invalid Command Line Arguments")
       logger.info("Yahoo_GetOHLC -i input_ticker_file -t ticker -p <period_string> -b <bar_string>")
       logger.info('<start_date> : a date in the format of YYYY-MM-DD that historical data should start from')
       logger.info('<end_date> : a date in the format of YYYY-MM-DD that historical data should end')
       logger.info(
           '<bar string> : possible value-- 1min, 2min, 3min, 5min, 10min, 15min, 30min, 1h, 2h, 3h, 4h, 8h, 1d, 1w, 1m')
       logger.info('input_ticker_file : if you do nott specify an input_ticker_file then you need to specify a -t ticker')

       logger.info('Maximum of 2-3 year daily prices')
       exit()
    elif input_ticker_file == '' :
       logger.info('Running With Ticker Symbol : {sym}, Start Date : {sdate}, End Date : {edate}, bar : {bar}'.format(sym=inputsymbol, sdate=start_date, edate=end_date, bar=bar_string))
    else :
        logger.info('Running With Tickers from file {ticker_file} '.format(ticker_file=input_ticker_file))

    Symbol_List = []

    if input_ticker_file != '' :
        if os.path.exists(input_ticker_file) :
            df = pd.read_csv(input_ticker_file)
            Symbol_List = list(df['tickers'])
    else :
        if inputsymbol == 'SP500':
            #check if file of SP Symbols exists in the default directory.  If it does not, then retrieve symbols
            if os.path.exists("SP500_Symbols.csv") :
                df = pd.read_csv("SP500_Symbols.csv")
                Symbol_List = list(df['tickers'])
            else :
                Symbol_List = save_sp500_tickers('')
                df = pd.DataFrame()
                df['tickers'] = pd.Series(Symbol_List).values
                df.to_csv("SP500_Symbols.csv")
        else :
            Symbol_List.append(inputsymbol)

    CWD = os.getcwd()
    file_name_date_string = start_date + '_to_' + end_date + '.csv'
    os.makedirs('OutputFiles', exist_ok=True)
    os.chdir('OutputFiles')

    for sym in Symbol_List :
        file_name = sym + '_' + file_name_date_string
        #if os.path.exists(file_name) :
        #    logger.info("Already Retrieved Data For Ticker {tick}".format(tick=sym))
        #    historical_prices_df = read_price_file(file_name, logger)
        #    Run_Model(sym, start_date, end_date, logger, historical_prices_df, file_name)
        #else :
        # Sets up the robot class, robot's portfolio
        trading_robot = setup_func(logger)
        historical_prices_df, trading_robot = retrieve_prices(trading_robot, sym, start_date, end_date, bar_string, logger)
        Run_Model(sym, start_date, end_date, logger, historical_prices_df, file_name)
        time.sleep(5)

    if len(Symbol_List) > 1 :
        summary_file(Symbol_List, file_name_date_string, logger)


    return True

if __name__ == "__main__":
   main(sys.argv[1:])
