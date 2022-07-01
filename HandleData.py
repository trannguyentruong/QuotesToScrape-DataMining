from pydoc import classname
from bs4 import BeautifulSoup
from urllib import request
import requests
import codecs
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

class Information:
    array = []
    def __init__(self,author, link, birthday,quote):
        self.author = author
        self.link = link
        self.birthday = birthday
        self.quote = quote
    def addAuthor(self,infor):
        self.array.append(infor)
    def printArray(self):
        for obj in self.array:
            print(obj.author)
    def exportCSV(self):
        header = ['Author', 'Link', 'Birthday', "Quote"]
        with open('Quote.csv', 'w+', newline='', encoding='utf-8-sig') as f: 
            write = csv.writer(f)  
            write.writerow(header)
            for obj in self.array:
                write.writerow([obj.author, obj.link, obj.birthday, obj.quote]) 


#1.2 c
def tacgiaLink():
    html = requests.get(url)
    quote_url = 'http://quotes.toscrape.com/'
    soup = BeautifulSoup(html.text, 'html.parser')
    result = soup.find_all('div', {'class': 'quote'})
    for quote in result:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        a = quote.find("a", string="(about)")
        link = quote_url+a['href']
        birthday = crawl_author(link)
        person = Information(author,link, birthday, text)
        print('Tên tác giả: ', author, "\nĐường link tác giả: ", link, "\nNgày tháng năm sinh: ", birthday, "\nCâu nói nổi tiếng: ", text)
        person.addAuthor(person)
    if(soup.find('li', class_='next')):
        next_page = soup.find('li', class_='next').find('a')
        if(next_page):
            next_page_jump(quote_url+next_page['href'])
    else:
        person.exportCSV()

def crawl_author(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    birthday = soup.find('span', class_='author-born-date').text
    return birthday

def next_page_jump(link):
    global url
    url = link
    tacgiaLink()

if __name__ == '__main__':
    global url

    url = 'http://quotes.toscrape.com/'
    html = requests.get(url)

    soup = BeautifulSoup(html.text, 'html.parser')

    #1.1
    with open('kq.txt', "w+", encoding="utf-8") as f:
        f.write(soup.prettify())

    #1.2 a
    result = soup.find_all('div', {'class': 'quote'})
    print(result)

    #1.2 b
    for i in range(len(result)):
        print(result[i].select('small[class="author"]'))

    tacgiaLink()