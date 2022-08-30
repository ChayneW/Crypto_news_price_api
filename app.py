import requests
from bs4 import BeautifulSoup
import time
import pandas
import datetime as dt
import smtplib

from email.message import EmailMessage


TODAY = dt.datetime.now().date()
gecko_endpoint = 'https://api.coingecko.com/api/v3/simple/price'
cryptopotato_endpoint = 'https://cryptopotato.com/crypto-news/'


''' API funct that makes api calls and saves data into a list. '''
def api_requests(coin_data):
    try:
        coin_id = coin_data['ids']
        g_request = requests.get(url=gecko_endpoint, params=coin_data)
        g_request.raise_for_status()
        g_coin_data = (g_request.json())
        print(g_coin_data)
        rounded_coin_data =float("{:.2f}".format(g_coin_data[coin_id]['usd_24h_change']))
        print(f"{coin_id} is at a change of: {(rounded_coin_data)}%")
    
        news_request = requests.get(url=cryptopotato_endpoint)
        time.sleep(2)
        news_request.raise_for_status()
        news_page = news_request.text

        soup = BeautifulSoup(news_page, 'html.parser')

        links = soup.find_all('h3', class_='rpwe-title')
        print(f"There are {len(links)} total articles trending.")

        for l in links:
            l_text = l.getText()
            
            if coin_id.lower() in l_text or coin_id.title() in l_text:
                print("\n")
                print(l_text)

                l_link = l.find('a').get('href')
                print(l_link)
                print("\n")
                related_links.append(l_link)
        save_csv()
    
    except KeyError:
        print('Please check spelling. Looping again.')
        return


'''Funct that takes list from api_requests() and automatically saves data into csv for use.'''
def save_csv():
    print('tapping into save_csv')
    print(f"tapping into related_links: {related_links}")
    if len(related_links) > 0:
        print(f"There are {len(related_links)} articles from 'Crypto Potato' news source saved about {coin}.\n")
        print('saving to CSV...')
        links_df = pandas.DataFrame(related_links, columns=[f'articles: {TODAY}'])
        links_df.to_csv(f'./{coin}_articles.csv', index=False)
    else:
        print(f'Looks like there are no articles trending on "CryptoPotato" on "{coin.upper()}" trending today.')
        return


'''Email Funct that requires your email address to send CSV.
    - Email credentials need to be provided.
    - Depending on email services, SMTP will need to be altered, and email service will need to allow app access.'''

MY_EMAIL = "YOUR EMAIL"
PASSWORD = "YOUR PASSWORD"

TARGET_EMAIL = "TARGET EMAIL"

def send_email():
    email = input(f"What's your email? (press 'n' for no email.) ").lower()

    if email == 'n':
        return

    elif '@' in email:
        email_confirm = input(f"'Y' to confirm: '{email}' is the right email? (can't end process once confirmed.) ").lower()

        if email_confirm == 'y':
            msg_text = f"Here's your list of articles for {coin} on {TODAY}"

            msg = EmailMessage()
            msg['Subject'] = msg_text
            msg['From'] = MY_EMAIL
            msg['To'] = email
            msg.set_content(f'Attached below is the files for {coin} that you requested.')
            
            with open(f'{coin}_articles.csv', 'rb') as file:
                file_data = file.read()
                file_type = str(type(file.name)) 
                file_name = file.name
                print(file_type, file_name)
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name )

            # Alter smtp to your email preference:
            with smtplib.SMTP('smtp.mail.yahoo.com', port=587) as connection:
                connection.starttls()
                print('connecting and sending email...')
                connection.set_debuglevel(1)
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.send_message(msg)
                print(f'{file_name} Sent to {email}')
        else:
            return      
    else:
        print('Please follow email format. Looping again.')
        return


'''MAIN CODE STARTS HERE!'''
keep_searching = False

while keep_searching != True:
    related_links = []
    coin = input('What coin do you want to check? (Please spell out coin. (CoinGeckoAPI only accepts fullname spelling. EX: "bitcoin" rather than "BTC".)) ')
    print(f'{coin} {type(coin)}')

    coin_parameters = {
        'ids': coin, 
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
    }

    api_requests(coin_parameters)

    articles_saved = len(related_links)

    if articles_saved > 0:
        choice_email = input('Send CSV to email? ("Y" or "N") ').lower()
        if choice_email == 'y':
            send_email()
    else:
        pass

    more_searches = input("Any more Crypto searches? 'Y' or 'N'. ").lower()
    if more_searches == 'n':
        keep_searching = True
    elif more_searches != 'y':
        print("Please only choose 'N' or 'Y'. Looping again.")
        pass