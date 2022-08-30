# Crypto_news_price_api:
With the use of BeautifulSoup4 and api calling, this app makes calls from CoinGecko to check desired cryptocurrency (by full name only) then cross references that coin to a crypto news website https://cryptopotato.com/market-updates/ to check for any trending news on that particular coin. 

If any news articles available about the chosen coin, then app will save data into a customized csv, then after inserting your own email details, will send email to desired email address. (Note, Python SMTP is implimented, so smtp address will need to be altered to your email preference. Also Email needs to allow app access depending on email type.(Change security settings from email to allow app connection.))  
