#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
""" sudo python3.8 -m pip install python-binance """
import binance
from binance.client import Client
from moocharoo_config import config
client = Client(config.apikey,config.secretkey)
MIN_VALUE=0.0001
def get_account_info(portfolio,capital,total_lots,btc_total):
    account=dict()
    for crypto in portfolio.keys():
        balance = client.get_asset_balance(asset=crypto) 
        #balance format example {'asset': 'DASH', 'free': '696.00000000', 'locked': '0.00000000'}
        name=crypto+'BTC'# name of the pair to trade
        if  crypto != 'USDT': #USDT/BTC does not exist in Binance
            avg_price = client.get_avg_price(symbol=name) #Get market price for a pair.
            """ Compute the amount of crypto (normalized) in Moocharoo according to the ratio lots/total_lots, the capital & the market price"""
            """ 
            To have the same LOTs than Moocharoo, the formula to use is 
            asset_nb=portfolio[crypto]
            If you want to use 100% of capital, the formula to use is
            asset_nb=portfolio[crypto]*((capital-capital*0.1)/btc_total)
            """
            asset_nb=portfolio[crypto]*((capital-capital*0.1)/btc_total)
            """ Compute the difference between normalized Moocharoo portfolio and Binance account crypto amount """
            difference=asset_nb-float(balance["free"])
            diff_price_btc = abs(difference)*float(avg_price['price'])
            """ Difference must be higher than minimal Binance allowable transaction ie 0,0001 BTC"""
            if diff_price_btc>MIN_VALUE:
                if difference < 0:
                    buy_sell="SELL"
                    difference = -difference
                else:
                    buy_sell = "BUY"
            else:
                buy_sell="HOLD"
            print(f"{crypto} \t Moocharoo: {asset_nb:.3f} \t Binance: {float(balance['free']):.3f} \t Difference in BTC: {diff_price_btc:.4f}")
            account[crypto]=difference, buy_sell
    return (account)#exemple {'BAT': 211.11893033075296, 'BNB': 2.4469392867754585, 'BCH': 0.16720497379062033}

def update_positions(account):
    current = client.get_account()
    """ Clear all positions that are not in Moocharoo portfolio """
    for coin in current['balances']:
        # example of format : {'asset': 'STPT', 'free': '12.00000000', 'locked': '0.00000000'}
        """ IF crypto in Binance Portfolio, crypto is not BNB, and crypto is not in Moocharoo portfolio, THEN Sell crypto"""
        if int(float(coin['free'])) > 0:
            if coin['asset'] != "BNB":# BNB used for fees
                if coin['asset'] not in account.keys():
                    print(f'SELL {coin["free"]} \t{coin["asset"]} because not listed in MOOCHAROO portfolio')
                    try:
                        qty=round(float(coin['free']),2)
                        order = client.order_market_sell(
                        symbol=(coin["asset"]+'BTC'),
                        quantity=qty)
                        print(f'SELL of {coin["asset"]} {qty} success')
                    except:
                        try:
                            qty=round(float(coin['free']),1)
                            order = client.order_market_sell(
                            symbol=(coin["asset"]+'BTC'),
                            quantity=qty)
                            print(f'SELL of {coin["asset"]} {qty} success')
                        except:
                            try:
                                qty=int(float(coin['free']))
                                order = client.order_market_sell(
                                symbol=(coin["asset"]+'BTC'),
                                quantity=qty)
                                print(f'SELL of {coin["asset"]} {qty} success')
                            except:
                                print(f'{coin["asset"]} SELL failed ERROR 10 qty {coin["free"]}')
    """ SELL first """
    for key_coin in account:
        if account[key_coin][1]=='SELL': #account['ADA'][0] nb d'assets à acheter/vendre, account['ADA'][1] 'BUY' ou 'SELL'
            try:
                qty=round(account[key_coin][0],2)
                order = client.order_market_sell(
                    symbol=(key_coin+'BTC'),
                    quantity=qty)
                print(f'{order["executedQty"]} {order["symbol"]} SELL order {order["orderId"]}')
            except:
                try:
                    qty=round(account[key_coin][0],1)
                    order = client.order_market_sell(
                        symbol=(key_coin+'BTC'),
                        quantity=qty)
                    print(f'{order["executedQty"]} {order["symbol"]} SELL order {order["orderId"]}')
                except:
                    try:
                        qty=int(account[key_coin][0])
                        order = client.order_market_sell(
                            symbol=(key_coin+'BTC'),
                            quantity=qty)
                        print(f'{order["executedQty"]} {order["symbol"]} SELL order {order["orderId"]}')
                    except:
                        print(f'{key_coin} SELL failed ERROR 20 qty {account[key_coin][0]}')
    """ BUY """
    for key_coin in account:
        if account[key_coin][1]=='BUY': #account['ADA'][0] nb d'assets à acheter/vendre, account['ADA'][1] 'BUY' ou 'SELL'
            try:
                qty=round(account[key_coin][0],2)
                order = client.order_market_buy(
                    symbol=(key_coin+'BTC'),
                    quantity=qty)
                print(f'{order["executedQty"]} {order["symbol"]} BUY order {order["orderId"]}')
            except:
                try:
                    qty=round(account[key_coin][0],1)
                    order = client.order_market_buy(
                        symbol=(key_coin+'BTC'),
                        quantity=qty)
                    print(f'{order["executedQty"]} {order["symbol"]} BUY order {order["orderId"]}')
                except:
                    try:
                        qty=int(account[key_coin][0])
                        order = client.order_market_buy(
                            symbol=(key_coin+'BTC'),
                            quantity=qty)
                        print(f'{order["executedQty"]} {order["symbol"]} BUY order {order["orderId"]}')
                    except:
                        print(f'{key_coin} BUY failed ERROR 30 qty {account[key_coin][0]}')
#test={'ZRX': 4, 'BAT': 11, 'BNB': 4, 'BCH': 4, 'ADA': 7, 'LINK': 13, 'DASH': 7}
#result=get_account_info(test, 0.24)
# place a test market buy order, to place an actual order use the create_order function
#order = client.create_test_order(
#    symbol='BNBBTC',
#    side=Client.SIDE_BUY,
#    type=Client.ORDER_TYPE_MARKET,
#    quantity=100)
#order = client.order_limit_buy(
#    symbol='BNBBTC',
#    quantity=100,
#    price='0.00001')
#order = client.order_limit_sell(
#    symbol='BNBBTC',
#    quantity=100,
#    price='0.00001')
#balance = client.get_asset_balance('REN')
#{'asset': 'BNB', 'free': '1.99485710', 'locked': '0.00000000'}
#price=client.get_avg_price(symbol='RENBTC')
