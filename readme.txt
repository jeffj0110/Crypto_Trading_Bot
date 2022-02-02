# Setup to run this code
- You don't need any logins for Yahoo or Yahoo Finance
- Access to their market data is free, but it will be delayed
- please review the libraries required in 'requirements.txt' to 
      understand the python libraries which will need to be 
      installed (ie. pip install 'libraries')

# The code will take as input a ticker of the crypto currency(ie. BTC-USD), the start and end dates of the
# market data and the type of data to process with the algorithmic strategy.  
# The command line parameter examples -

cd <the directory where python code resides>
python Yahoo_GetOHLC.py -t BTC-USD -s 2019-01-21 -e 2022-01-21 -b 1d

python Yahoo_GetOHLC -i <input_ticker_file> -t <tickersymbol> -s <start_date> -e <end_date> -b <bar_string>
     <input_ticker_file> : A CSV file with input tickers to process.  See the example provided (Input_Crypto_Symbols.csv).
     <tickersymbol> : An input ticker symbol is required if you don't specify an input_ticker_file.
     <start_date> : a date in the format of YYYY-MM-DD that historical data should start from
     <end_date> : a date in the format of YYYY-MM-DD that historical data should end
     <bar string> : possible value-- 1min, 2min, 3min, 5min, 10min, 15min, 30min, 1h, 2h, 3h, 4h, 8h, 1d, 1w, 1m

This will generate at least two files in the directory for each ticker -
    <tickersymbol>_logfile_YYYY_MM_DD-HHMMSS.txt     : This is a timestamped log file in the default directory
    <tickersymbol>_run_YYYY_MM_DD_HHMMSS.csv         : A comma delimited file market data and results will go in the 'OutputFiles' subdirectory.

It will also generate a summary file which will contain the annualized returns and number of trades generated 
for each ticker in the input_ticker_file.
