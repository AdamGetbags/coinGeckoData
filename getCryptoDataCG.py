# -*- coding: utf-8 -*-
"""
@author: Adam Getbags
CoinGecko API: Advanced Guide
"""

#pip install pycoingecko

#import modules
import pandas as pd
import datetime as dt
import time as t
import plotly.graph_objects as go
from plotly.offline import plot
from pycoingecko import CoinGeckoAPI

#create a client
cg = CoinGeckoAPI()

#confirm connection
cg.ping()

#get a list of coins, sort df by id
coinList = cg.get_coins_list()
coinDataFrame = pd.DataFrame.from_dict(coinList).sort_values('id'
                                      ).reset_index(drop=True)

#btc/eth/dpx by id
#coinDataFrame[coinDataFrame['id'] == 'bitcoin']
#coinDataFrame[coinDataFrame['id'] == 'ethereum']
#coinDataFrame[coinDataFrame['id'] == 'dopex']
coins = ['bitcoin','ethereum','dopex']

#get list of suppored VS currencies
counterCurrencies = cg.get_supported_vs_currencies()
vsCurrencies = ['usd', 'eur', 'link']

#most simple price request - nested dictionary format
simplePriceRequest = cg.get_price(ids = coins, vs_currencies = 'usd')
print(simplePriceRequest)

complexPriceRequest = cg.get_price(ids = coins, 
                        vs_currencies = vsCurrencies, 
                        include_market_cap = True,
                        include_24hr_vol = True,
                        include_24hr_change = True,
                        include_last_updated_at = True)
print(complexPriceRequest)

#get all asset platforms
assetPlatformsList = cg.get_asset_platforms()
assetPlatforms = pd.DataFrame.from_dict(assetPlatformsList
                   ).sort_values('id').reset_index(drop=True)

#assetPlatforms[assetPlatforms['id'] == 'binance-smart-chain']
#get AVAX token price (using contract address) from BSC (asset platform)
AVAXpriceBSC = cg.get_token_price(id = 'binance-smart-chain', 
                   contract_addresses = '0x1ce0c2827e2ef14d5c4f' +
                                        '29a091d735a204794041',
                   vs_currencies = 'usd')

#get coins categories, privacy-coins, stablecoins, gambling, lp-tokens, etc.
coinCategoriesList = pd.DataFrame(cg.get_coins_categories_list())
#get data on coin categories
coinCategoriesData = pd.DataFrame(cg.get_coins_categories(
                                                order = 'market_cap_desc'))
#dictionary to dataframe
coinCategoriesDataFrame = pd.DataFrame.from_dict(coinCategoriesData
                                ).sort_values('id').reset_index(drop=True)

#get coins market cap, rank, prices, volume, market data, etc.
#by ID using a list
coinsMktDataByIds = cg.get_coins_markets(vs_currency = 'usd',
                                        ids = coins)

#by category see cg.get_coins_categories_list(), in order
coinsMktDataByCategory = cg.get_coins_markets(vs_currency = 'usd',
                                    category = 'stablecoins',
                                    order = 'volume_desc')

#by gecko rank, 250 per page, page number two 
coinsMktDataByPage = cg.get_coins_markets(vs_currency = 'usd',
                                      per_page = 250,
                                      page = 2,
                                      order = 'gecko_desc')

#get coin data by ID, rate of change, sparkline chart data
coinsMktDataById = cg.get_coins_markets(vs_currency = 'usd',
                                      ids = 'bitcoin',
                                      price_change_percentage = '1h,24h,7d',
                                      sparkline = True)
#dictionary to dataframe
coinsMktDataFrame = pd.DataFrame.from_dict(coinsMktDataById).sort_values('id'
                                      ).reset_index(drop=True)

#get list of exchanges
exchgList = cg.get_exchanges_list(per_page = 250, page = 1)
exchgDataFrame = pd.DataFrame.from_dict(exchgList
                              ).sort_values('trade_volume_24h_btc_normalized',
                                            ascending = False
                              ).reset_index(drop=True)
                                            
#get exchanges ids              
exchgIds = cg.get_exchanges_id_name_list()                             
exchgIdsDataFrame = pd.DataFrame.from_dict(exchgIds
                              ).sort_values('id'
                              ).reset_index(drop=True)
                                            
#get exchange data by id // max of 100 results in exchgById['tickers']                                           
exchgById = cg.get_exchanges_by_id(id = 'binance')    
print(exchgById.keys())
exchgDataFrameById = pd.DataFrame(exchgById['tickers'])
print(exchgDataFrameById.columns)                      

#the same as exchgById['tickers'] but can input multiple ids + pages
exchgTickersByID = cg.get_exchanges_tickers_by_id(id = 'binance', 
                                            coin_ids = ['bitcoin','ethereum'],
                                            page = 1, 
                                            depth = True, 
                                            order = 'volume_desc')
                  
#get exchg volume (in BTC?) // days param has a limit, returns 503 errors
exchgVolume = cg.get_exchanges_volume_chart_by_id(id='binance',days=40)

#list to dataframe
exchgVolumeDataFrame = pd.DataFrame(exchgVolume,  columns = ['Date', 'Volume'])

#reformat date
exchgVolumeDataFrame['Date'] = exchgVolumeDataFrame['Date'].apply(
             lambda x: dt.datetime.fromtimestamp(x/1000).strftime('%m-%d-%Y'))
#reformat volume
exchgVolumeDataFrame['Volume'] = pd.to_numeric(exchgVolumeDataFrame['Volume'])

#set index
exchgVolumeDataFrame = exchgVolumeDataFrame.set_index('Date')

#plot
exchgVolumeDataFrame['Volume'].plot()

#get coin ticker by id / limited to 100, by page
mktSpecificData = cg.get_coin_ticker_by_id(id = 'bitcoin',
                                           exchange_id ='aave',
                                           page = 2,
                                           depth = True)
#dictionary to dataframe
mktSpecificDataFrame = pd.DataFrame.from_dict(mktSpecificData['tickers']
                                  ).sort_values('base').reset_index(drop=True)

#get coin history by SINGLE id
coinHistory = cg.get_coin_history_by_id(id = 'bitcoin', 
                              date = dt.datetime.today().strftime('%d-%m-%Y'))

#get daily historical data
dailyHistoricalData = cg.get_coin_market_chart_by_id(id = 'bitcoin', 
                               vs_currency = 'usd',
                               days = 'max')

#get hourly historical data
hourlyHistoricalData = cg.get_coin_market_chart_by_id(id = 'bitcoin', 
                               vs_currency = 'usd',
                               days = 90)

#get 5 minute historical data
fiveMinHistoricalData = cg.get_coin_market_chart_by_id(id = 'bitcoin', 
                               vs_currency = 'usd',
                               days = 1)

#input a range of timestamps to get data for - using predetermined frequency
chartRange = cg.get_coin_market_chart_range_by_id(id = 'bitcoin', 
                                                  vs_currency = 'usd', 
                                                  from_timestamp = 1392577232, 
                                                  to_timestamp = 1422577232)
#list of lists to dataframe 
dailyHistoricalDataFrame = pd.DataFrame(data = dailyHistoricalData['prices'],
                                        columns = ['Date', 'Price'])
#reformat date
dailyHistoricalDataFrame['Date'] = dailyHistoricalDataFrame['Date'].apply(
             lambda x: dt.datetime.fromtimestamp(x/1000).strftime('%m-%d-%Y'))
#set index
dailyHistoricalDataFrame = dailyHistoricalDataFrame.set_index('Date')

#plot
dailyHistoricalDataFrame['Price'].plot()

#get OHLC data for preset range 1/7/14/30/90/180/365/max
#candle body width by date range 
#1 - 2 days: 30 minutes
#3 - 30 days: 4 hours
#31 days and beyond: 4 days
ohlcData = cg.get_coin_ohlc_by_id(id = 'bitcoin', 
                                  vs_currency = 'usd', 
                                  days = '14')
#list to dataframe
ohlcDataFrame = pd.DataFrame(data = ohlcData,
                           columns = ['Date', 'Open', 'High' ,'Low', 'Close'])
#reformat date
ohlcDataFrame['Date'] = ohlcDataFrame['Date'].apply(
                        lambda x: dt.datetime.fromtimestamp(x/1000
                        ).strftime('%m-%d-%Y %H:%M:%S'))
#set index
ohlcDataFrame = ohlcDataFrame.set_index('Date')

#generate plotly figure
fig = go.Figure(data=[go.Candlestick(x=ohlcDataFrame.index,
                open=ohlcDataFrame['Open'],
                high=ohlcDataFrame['High'],
                low=ohlcDataFrame['Low'],
                close=ohlcDataFrame['Close'])])

#open figure in browser
plot(fig, auto_open=True)

#get coin info from contract address
coinInfoByAddress = cg.get_coin_info_from_contract_address_by_id(
                               id = 'binance-smart-chain', 
                               contract_address = '0x1ce0c2827e2ef14d5c4f' +
                                                  '29a091d735a204794041')
#display
print(coinInfoByAddress['market_data'].keys())
print(coinInfoByAddress['tickers'])

#get historical market data - price, mkt cap, and volume / days = 1 to 'max'
#similar data points to .get_coin_market_chart_by_id()
coinChartData = cg.get_coin_market_chart_from_contract_address_by_id(
                            id = 'binance-smart-chain', 
                            contract_address = '0x1ce0c2827e2ef14d5c4f' +
                                               '29a091d735a204794041',
                            vs_currency = 'usd',
                            days = 'max')

coinChartDataRng = cg.get_coin_market_chart_range_from_contract_address_by_id(
                            id = 'binance-smart-chain', 
                            contract_address = '0x1ce0c2827e2ef14d5c4f' +
                                               '29a091d735a204794041',
                            vs_currency = 'usd',
                            from_timestamp = t.time()-100000, 
                            to_timestamp = t.time())

#display
print(coinChartData.keys())

#list of lists to dataframe 
coinChartDataFrame = pd.DataFrame(data = coinChartData['prices'],
                                        columns = ['Date', 'Price'])
#reformat date
coinChartDataFrame['Date'] = coinChartDataFrame['Date'].apply(
             lambda x: dt.datetime.fromtimestamp(x/1000).strftime('%m-%d-%Y'))
#set index
coinChartDataFrame = coinChartDataFrame.set_index('Date')

#plot
coinChartDataFrame['Price'].plot()

#get limited index data // name, id , market, last price
indexData = cg.get_indexes()

#get index ids, names
indexIds = cg.get_indexes_list()
indexIdsDataFrame = pd.DataFrame(indexIds).sort_values('id'
                                                       ).reset_index(drop=True)

#get all derivatives tickers
derivTickers = cg.get_derivatives()

#list to dataframe
derivTickersDataFrame = pd.DataFrame(derivTickers).sort_values('symbol'
                                                ).reset_index(drop=True)

#get derivatives exchanges + data
derivExchg = cg.get_derivatives_exchanges()       
#list to dataframe        
derivExchgDataFrame = pd.DataFrame(derivExchg).sort_values('id'
                                                ).reset_index(drop=True)

#get exchanges ordered by open interest
print(derivExchgDataFrame.sort_values('open_interest_btc',
                                       ascending = False
                                       ).reset_index(drop=True
                                       )[['id','open_interest_btc']].dropna())

#get exchange ids
derivExchgId = cg.get_derivatives_exchanges_list()

#list to dataframe
derivExchgIdDataFrame = pd.DataFrame(derivExchgId).sort_values('id'
                                                 ).reset_index(drop=True)
#display
print(derivExchgIdDataFrame['id'].head(20))

#get single exchange data by id + ticker data
print(cg.get_derivatives_exchanges_by_id(id = 'binance_futures'))
#with tickers
singleExchgData = cg.get_derivatives_exchanges_by_id(id = 'binance_futures',
                                                     include_tickers = 'all')
#ticker data list to dataframe
singleExchgTickerData = pd.DataFrame(singleExchgData['tickers']
                                     ).sort_values('symbol'
                                     ).reset_index(drop=True)

#get exchange rates
exchangeRates = cg.get_exchange_rates()
#list to dataframe
exchangeRatesDataFrame = pd.DataFrame(exchangeRates['rates'])

#get trending search coins 
trendingCoins = cg.get_search_trending()['coins']


#get global cryptcurrency data // not too useful
globalData = cg.get_global()
print(globalData.keys())


#get global defi data 
globalDefiData = cg.get_global_decentralized_finance_defi()

#get public companies bitcoin or ethereum holdings
publicBTC = cg.get_companies_public_treasury_by_coin_id(coin_id = 'bitcoin')
publicETH = cg.get_companies_public_treasury_by_coin_id(coin_id = 'ethereum')
