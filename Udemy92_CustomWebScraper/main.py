# UdemyDay92 : Custom Web Scraper

from bs4 import BeautifulSoup
import requests
import csv

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

SOURCE_URL = "https://sclibrary.bibliocommons.com/list/share/1348734862_sclibrary_youthservices/1570299219_high_school_suggested_reading_list"
FIELD_NAMES = ['url', 'title', 'author', 'rating', 'story']

CSV_FILE = 'book_list.csv'
book_list = []


# scrap book url
def get_book_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    books = soup.find_all('div', class_='list_item_title')
    book_dict = {}

    for book in books:
        data = book.contents[1].get('href').split('/')
        href_end = "S" + data[3][7:] + "C" + data[3][:7]

        book_dict[data[3]] = "https://sclibrary.bibliocommons.com/v2/record/" + href_end
    return book_dict



def book_detail(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    # book info
    get_info = soup.find_all('span', class_='cp-screen-reader-message')

    title = get_info[0].get_text()
    author = get_info[1].get_text()
    rating = get_info[2].get_text()

    # book story
    get_story = soup.find(class_='expandable-html__text')
    story = get_story.get_text()

    book_info = {
        'url': url,
        'title': title,
        'author': author[:-1],
        'rating': rating[12:15],
        'story': story
    }

    book_list.append(book_info)


def save_to_csv(item_list):
    with open(CSV_FILE, 'w',encoding='UTF-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(item_list)




urls = get_book_url(SOURCE_URL)

for book_id, book_url in urls.items():
    book_detail(book_url)

save_to_csv(book_list)
book_list = []