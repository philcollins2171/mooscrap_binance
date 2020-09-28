
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 

version=1.1
import sys
""" Code used with python 3.8.2 run under Visual Studio Code on a Chromebook"""
import time
""" pip install python-binance """
import manage_binance
""" pip install selenium"""
from selenium import webdriver
""" pip install webdriver_manager. Here Chrome imported, but one can choose any other driver (IE, Opera...) """
from webdriver_manager.chrome import ChromeDriverManager
from moocharoo_config import config
import logging

"""
Regular Chrome or any other browser must be installed
Using Chrome to access web
"""
# CSS Pathes on Moocharoo site
xpath_login="/html/body/header[@class='header-section transparent--header header--fixed']/div[@class='header-top']/div[@class='container']/div[@class='row justify-content-between']/div[@class='col-lg-4 col-md-4']/div[@class='header-top-right d-flex align-items-center justify-content-end']/div[@class='header-cart-count']/span"
xpath_user="/html/body[@class='modal-open']/div[@id='signInModal']/div[@class='modal-dialog modal-dialog-centered']/div[@class='modal-content bdr-radius']/div[@class='signin-wrapper']/form[@class='signin-form']/div[@class='form-group'][1]/input[@class='form-control']"
xpath_pass="/html/body[@class='modal-open']/div[@id='signInModal']/div[@class='modal-dialog modal-dialog-centered']/div[@class='modal-content bdr-radius']/div[@class='signin-wrapper']/form[@class='signin-form']/div[@class='form-group'][2]/input[@class='form-control']"
xpath_btnlogin="/html/body[@class='modal-open']/div[@id='signInModal']/div[@class='modal-dialog modal-dialog-centered']/div[@class='modal-content bdr-radius']/div[@class='signin-wrapper']/form[@class='signin-form']/button[@class='btn btn-primary btn-hover']"
xpath_cryptovalue="/html/body[@class='modal-open']/div[@id='setBalance']/div[@class='modal-dialog modal-dialog-centered']/div[@class='modal-content bdr-radius']/div[@class='signin-wrapper']/form[@class='signin-form']/div[@class='form-group'][1]/div[@class='input-group mb-2']/input[@id='bitcoin']"
xpath_submit="/html/body[@class='modal-open']/div[@id='setBalance']/div[@class='modal-dialog modal-dialog-centered']/div[@class='modal-content bdr-radius']/div[@class='signin-wrapper']/form[@class='signin-form']/button[@class='btn btn-primary btn-hover']"
xpath_position="/html/body/section[@class='investment-section pb-120']/div[@class='container']/div[@class='row']/div[@class='col-lg-12']/div[@class='main-area']/div[@class='row mt-4 mb-none-30 investment-item-area list-view']/div[@class='col-lg-6 investment-item crypto'][1]/div[@class='investment-single mb-30']/div[@class='content']/div[@class='right']/div[@class='share-price'][2]/h3[@class='price']"

def site_login():
    driver.get('https://moocharoo.ninja/')
    driver.find_element_by_xpath(xpath_login).click()
    time.sleep(1)
    driver.find_element_by_xpath(xpath_user).send_keys(config.username) # config.username is to be setup in moocharoo_config.py
    driver.find_element_by_xpath(xpath_pass).send_keys(config.password) # config.password is to be setup in moocharoo_config.py
    element=driver.find_element_by_xpath(xpath_btnlogin)
    driver.execute_script("arguments[0].click();", element)

def portfolio_tracker_page(btc_capital):
    driver.get("https://moocharoo.ninja/portfolio-tracker.html")
    time.sleep(1)
    driver.find_element_by_xpath(xpath_cryptovalue).clear()
    driver.find_element_by_xpath(xpath_cryptovalue).send_keys(str(btc_capital)) # config.capital is to be setup in moocharoo_config.py
    driver.find_element_by_xpath(xpath_submit).click()
    cryptos = driver.find_elements_by_css_selector("div.col-lg-6.investment-item.crypto")
    portfolio_lots=dict()#dictionnary of crypto = lot
    total_lots=0 # Used to recompute total number of lots used in the Moocharoo portfolio to recompute further ratios for each crypto
    pos_value_total=0 # Used to copute total BTC equivalence
    for m in cryptos:
        """SCRAP CRYPTO NAME HTML FIELD"""
        name=m.find_element_by_css_selector('h3.investment-title').text #Get crypto name, including descriptive Name and Binance SPOT Name
        last = name.split() 
        crypto_coin=last[-1] #-1 stands for last word corresponding to Binance SPOT Name
        """SCRAP CRYPTO LOTS HTML FIELD"""
        lots=m.find_elements_by_css_selector('h4.amount') #Get crypto field containing : [0]:%, [1]:lots [2]:lot value
        lots_value = int(lots[1].text)
        position=m.find_elements_by_css_selector('h3.price') #Get crypto field containing : [2] 538\nHODLING [3] 0.00520\nPOSITION VALUE (in BTC)
        temp = position[3].text
        temp = temp.split("\n")
        pos_value=float(temp[0])
        temp = position[2].text
        temp = temp.split("\n")
        portfolio_lots[crypto_coin]=float(temp[0].replace(',','')) # Get number of Crypto holding (replace GB ',' thousands for float conversion)
        total_lots=total_lots+lots_value
        pos_value_total = pos_value_total+pos_value
    print(f'Total lots : {total_lots}')
    print(f'Total position : {pos_value_total} BTC')
    return(portfolio_lots,total_lots, pos_value_total)

if __name__ == "__main__":
    """
    print("LOG ACTIVATED")
    logging.basicConfig(filename='scrap_crypto.log',level=logging.DEBUG,\
        format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
    logging.debug('Debug error')
    logging.info('INFO ERROR')
    logging.warning('Warning Error %s: %s', '01234', 'Erreur Oracle')
    logging.error('error message')
    logging.critical('critical error')
    """
    btc_capital = manage_binance.get_btc_capital()
    #driver = webdriver.Chrome(). Any other program can be used. See webdriver doc.
    driver = webdriver.Chrome(ChromeDriverManager().install())

    site_login()
    """ 
    Build portfolio_lots dictionnary. Lots is the number of lots in the Moocharoo portfolio
    for example : {'ZRX': 4, 'BAT': 11, 'BNB': 4, 'BCH': 4, 'ADA': 7, 'LINK': 13, 'DASH': 7}
    total_lots is the total number of lots used in the Moocharoo portfolio
    """
    print(f"\n Mooscrap-binance version {version}\n")
    portfolio_lots,total_lots,btc_total=portfolio_tracker_page(btc_capital) 
    """ 
    Build account dictionnary. Numbre of lots in Binance portfolio, and the direction of trading based on delta between Moocharoo and Binance
    for example : {'BAT': (19, 'BUY'), 'BNB': (0, 'SELL'), 'BCH': (0, 'BUY'), 'BTG': (0, 'BUY'), 'ADA': (489, 'BUY')}
    """
    account=manage_binance.get_account_info(portfolio_lots,float(config.capital),total_lots,btc_total) 
    """ Update of all Binance positions"""
    manage_binance.update_positions(account)
    driver.quit()#kill Chrome#
