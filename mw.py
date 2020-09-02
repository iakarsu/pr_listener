from urllib.request import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup   
import threading, os, requests, json

from db import PRTable, session, Mails
from mail import MailClient
from dotenv import load_dotenv


load_dotenv(verbose=True)
mail_list = session.query(Mails).all()

def linker(url):
    print(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        web_byte = urlopen(req).read() 
        webpage = web_byte.decode('utf-8')
        soup = BeautifulSoup(webpage, 'html.parser')
    except HTTPError as e:
        print('HTTPError = ' + str(e.code))
    except URLError as e:
        print('URLError = ' + str(e.reason))
    except Exception:
        import traceback
        print('generic exception: ' + traceback.format_exc())
    
    return soup

def pr_listener():
    url = 'https://www.prnewswire.com/search/news/?keyword=huobi&page=1&pagesize=100'
    soup = linker(url)
    urls = soup.find('div', class_="col-sm-12 card-list")
    rows = urls.findAll('div', class_="row")
    link = 'prnewswire.com' + rows[0].find('a', class_='news-release')['href']
    last = session.query(PRTable).order_by(PRTable.id.desc()).first()
    
    if(last.link == link):
        print("found")
    else:
        print("sending..")
        link = 'prnewswire.com' + rows[0].find('a', class_='news-release')['href']
        title = rows[0].find('a', class_='news-release').text
        date = rows[0].find('small').text
        ins = PRTable(link=link, title=title, date=date)
        session.add(ins)
        session.commit()
        print("{} titled article has been found and, you can check the link here: {}".format(title, link))

        alert(title, link, date)

def alert(title, link, date):
    mail_sender = MailClient(os.getenv("MAIL"), os.getenv("MAIL_PASSWORD")) 
    for r in mail_list:
        mail_sender.sendMail(r.mail, title[1:], link, date)

def bulk_db_inserter():
    obj = []
    url = 'https://www.prnewswire.com/search/news/?keyword=huobi&page=1&pagesize=100'
    soup = linker(url)
    urls = soup.find('div', class_="col-sm-12 card-list")
    rows = urls.findAll('div', class_="row")

    for r in rows:
        link = 'prnewswire.com' + r.find('a', class_='news-release')['href']
        title = r.find('a', class_='news-release').text
        date = r.find('small').text
        ins = PRTable(link=link, title=title, date=date)
        obj.append(ins)

    session.add_all(obj)
    session.commit()

def trial():
    last = session.query(PRTable).order_by(PRTable.id.desc()).first()
    alert(last.title, last.link, last.date)

soup = linker('https://www.bitfinex.com/posts')
print(('Bitfinex Lists Chainlink (LINK)' in soup))