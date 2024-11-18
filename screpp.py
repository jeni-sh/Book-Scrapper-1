# python -m pip install request -->get data fro web (html,json,xml)
#python -m pip install beautisoup4 --> parse html

#git config --global user.name "Jenny Shah"
#git config --global user.email "zennishah555@gmail.com"

import requests
import sqlite3
from bs4 import BeautifulSoup 

URL="https://books.toscrape.com/"

#cretaing a database
def create_database():
    conn = sqlite3.connect("book.sqlite3")
    cursor =conn.cursor()
    cursor.execute(

        """
        CREATE TABLE IF NOT EXISTS books(
        id integer primary key autoincrement,
        title TEXT,
        price REAL,
        currency TEXT
        )
        """
    )
    conn.commit()
    conn.close()

#Function for inserting values into the table

def insert_book(title,price,currency):
    conn =sqlite3.connect("book.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO books(title,price,currency) VALUES(?,?,?)
        """,
        (title,price,currency),
    )    
    conn.commit()
    conn.close()


#function for scrapping

def scrape_books(url):
    response = requests.get(url)
    if response.status_code!=200:
        print(f"Failed to fetch the page ,status code:{response.status_code}")
        return
    
    #set encoding explicitly to handle special characters

    response.encoding =response.apparent_encoding
    print(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    books =soup.find_all("article",class_="product_pod")
    for book in books:
        title =book.h3.a["title"]
        price_text=book.find("p",class_="price_color").text
    #the first character should be the currency symbol(e.g,$)

        currency =price_text[0]
        price =price_text[1:]

        insert_book(title,price,currency)

create_database()
scrape_books(URL)