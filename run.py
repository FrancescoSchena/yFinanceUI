import yfinance as yf
import datetime as dt
import requests

#   ___SETTINGS___
datechoice = True           # Defaults to 2000 -> 2019
intervals_choice = True     # Defaults to 1d
stocks_choice = True        # Defaults to defaultstocks
defaultstocks = "^NDX AAPL AMZN MSFT FB GOOGL TSLA GOOG NVDA ADBE NFLX INTC PYPL CMCSA PEP CSCO COST " \
                "AVGO TMUS AMGN QCOM TXN CHTR SBUX AMD INTU ZM ISRG MDLZ GILD BKNG JD VRTX FISV" \
                " ADP REGN ATVI CSX MELI AMAT MU LRCX ADSK ILMN BIIB ADI LULU MNST DOCU WDAY CTSH " \
                "EXC KHC XEL NXPI DXCM EBAY EA BIDU CTAS ROST ORLY IDXX SNPS SPLK MAR KLAC WBA" \
                " NTES PCAR CDNS VRSK PAYX ASML MRNA ANSS MCHP ALXN CPRT FAST XLNX SIRI ALGN" \
                " SWKS VRSN CERN DLTR PDD INCY MXIM TTWO CDW CHKP TCOM CTXS BMRN ULTA EXPE WDC FOXA LBTYK FOX LBTYA"\
    .split(" ")


#   ___FUNCTIONS___
# Returns False if date is incorrect, else True
def date_check(date):
    try:
        date_int = [int(i) for i in date.split("-")]
        if not len(date) == 10:
            return False
        elif not 1900 <= date_int[0] <= 2020:
            return False
        elif not 0 < date_int[1] <= 12:
            return False
        elif not 0 < date_int[2] <= 31:
            return False
        else:
            return True
    except Exception:
        return False

# Returns list of Tickers for a specific query
def stock_info(name):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(name)
    return requests.get(url).json()['ResultSet']['Result']
    '''
    {"ResultSet":
        {"Query":"msft",
            "Result":[
                {"symbol":"MSFT",
                "name":"Microsoft Corporation",
                "exch":"NMS",
                "type":"S",
                "exchDisp":"NASDAQ",
                "typeDisp":"Equity"},

                {"symbol":"^NY2LMSFT",
                "name":"ICE Leveraged 2x MSFT Index",
                "exch":"NYS","type":"I",
                "exchDisp":"NYSE",
                "typeDisp":"Index"},

                {"symbol":"MSFT.BA",
                "name":"Microsoft Corporation",
                and going on...
                }]
        }
    }
    '''


# Asking for inputs:
#   Date
if datechoice:
    # ____ Parsing and correcting the inputs ____
    # Start Date
    while True:
        usr = input(
            "Starting date as YYYY-MM-DD\nIf blank defaults to 2000-01-01\n>>")
        if usr == "":
            starting_date = [2000, 1, 1]
            break
        elif date_check(usr):
            starting_date = [int(i) for i in usr.split("-")]
            break
        else:
            print("\nSorry your date wasn't correct\n")
    start = dt.datetime(starting_date[0], starting_date[1], starting_date[2])
    # End Date
    while True:
        today = dt.datetime.today()
        usr = input(
            f"Ending date as YYYY-MM-DD\nIf blank defaults to today ({today})\n>>")
        if usr == "":
            end = today
            break
        elif date_check(usr):
            ending_date = [int(i) for i in usr.split("-")]
            end = dt.datetime(ending_date[0], ending_date[1], ending_date[2], 23, 59)
            break
        else:
            print("\nSorry your date wasn't correct\n")
else:
    # Fallback in case of datechoice = False
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2020, 1, 1)
# Interval
intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
if intervals_choice:
    # Acceptables intervals to input
    while True:
        usr_interval = input(
            "Interval (1d, 5d, 1wk, 1mo, 3mo)\nIf blank defaults to \'1d\'\n>>")
        if usr_interval == "":
            usr_interval = "1d"
            break
        elif usr_interval in intervals:
            break
        elif usr_interval not in intervals:
            print("\nSorry your interval wasn't correct\n")
else:
    usr_interval = "1d"


#   Stock
if stocks_choice:
    stocks = []
    while True:
        stocksnum = len(stocks)
        print('\n\nTicker in lista: {}'.format(stocksnum))
        msg = "Aggiungi delle azioni digitando il ticker o il nome dell'emittente."
        if stocksnum != 0:
            msg += ("\nOppure digita \"go\" per iniziare l'elaborazione o \"list\" per vedere i titoli già presenti")
        print(msg)
        comand = input(">>> ").lower()
        if comand == "":
            stocks = ["AAPL", "MSFT", ]
        elif stocksnum != 0 and comand == "go":
            break
        elif stocksnum != 0 and comand == "list":
            print(stocks)
        else:
            num = 2
            while True:
                stocklist = stock_info(comand)[0:num]
                print("_" * 25)
                for i, stock in enumerate(stocklist):
                    print(i)
                    print(stock)
                    '''for line in stock:    print(line)'''
                    print("_"*25)
                comand1 = input('Digita il numero corrispondente al ticker che interessa.\nOppure \"more\" se non è in lista o \"none\" per uscire\n>>> ').lower()
                if comand1 == 'none':
                    break
                elif comand1 == 'more':
                    num = 6
                else:
                    try:
                        stocks.append(stocklist[int(comand1)]['symbol'])
                        print('\nAggiunto {} alla lista dei ticker'.format(stocks[-1]))
                        break
                    except ValueError as e:
                        print("C'è stato un errore, riprova.")
                    except IndexError as a:
                        print("Il numero non era corretto, riprova.")
else:
    stocks = defaultstocks

print("Inizio download...")

data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers=stocks,

        start=start,
        end=end,
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        # period="ytd",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval=usr_interval,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        # group_by = 'ticker',
        group_by='column',

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads=True,
    )

# Comment the columns you want
del data['Volume']
del data['High']
del data['Low']
del data['Open']
# del data['Close']
# del data['Adj Close']

data.to_excel("Data.xlsx",
              sheet_name="Data")
