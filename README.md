# mooscrap_binance

This program allows to synchronise the Binance crypto account with Moocharoo crypto portfolio. It opens a web explorer, authentificates on moocharoo.ninja, goes to Master portfolio, and grabs all the values of the portfolio (for the 50 cryptos).
It then send BUY/SELL order to Binance to have about the same amount of coins in your the Binance portfolio.

What you need :
Master account $$ to moocharoo.ninja to access moocharoo Master portfolio
Binance account $$
Python install
Some python knowledge

Configuration :
Copy the template into moocharoo_config.py and put your ID/pass/keys
You will need to install modules imported by scrap_crypto.py and manage_binance.py
Configure the Web explorer you use in driver = webdriver.Chrome(ChromeDriverManager().install()). If you use Chrome, no need to change this line.

Finally :
Run scrap_crypto.py

Liability :
I will not be taken accountable or responsible for any damage or consequences on your computer or Binance account.

Satisfaction :
It works well for me. But it was developped for my own needs.
Consequently, do not hesitate to improve it and to share.

Donation:
Feel free to donate by Paypal at francoispina@free.fr if you are happy with all the spared time !!!!!!!

Go Further with this tool:
Make an executable with pyinstaller using -c and --onefile options
Then make it run in a VPS or your computer as a Scheduled Task every hour ;)