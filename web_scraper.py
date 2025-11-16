import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

CATALOGUE_BASE_URL = 'http://books.toscrape.com/catalogue/'
PAGE_URL_TEMPLATE = CATALOGUE_BASE_URL + 'page-{}.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_book_data(soup):
    """Scrapes all book data from a single catalogue page."""
    books = []
    
    for book in soup.select('article.product_pod'):
# 1. Scrape data from the main list page ---
        title = book.h3.a['title']
        price = book.select_one('p.price_color').text.replace('£', '')
        rating = book.p['class'][1]  
        
        
        detail_page_relative_url = book.h3.a['href']
        
        detail_page_url = CATALOGUE_BASE_URL + detail_page_relative_url.replace('../', '')
        
        
        image_url = 'http://books.toscrape.com/' + book.img['src'].replace('../', '')
#  2. Scrape extra data from the detail page ---
        description = "N/A"
        upc = "N/A"
        availability_count = "N/A"
        
        try:
            
            detail_response = requests.get(detail_page_url, headers=HEADERS, timeout=10)
            if detail_response.status_code == 200:
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                
                
                article = detail_soup.find('article', class_='product_page')
                
                
                desc_p = article.select_one('#product_description + p')
                if desc_p:
                    description = desc_p.text
                
                
                for row in article.select('table.table-striped tr'):
                    th_text = row.find('th').text
                    if th_text == 'UPC':
                        upc = row.find('td').text
                    if th_text == 'Availability':
                        
                        availability_count = row.find('td').text.strip().split('(')[-1].replace(' available)', '')
            
            else:
                print(f"  > Failed to get details for: {title}")

        except requests.exceptions.RequestException as e:
            print(f"  > Error getting details for {title}: {e}")

# 3. Append all data (basic + detailed) ---
        books.append({
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Stock_Count': availability_count, 
            'UPC': upc,
            'Description': description,
            'Image_URL': image_url,
            'Detail_Page_URL': detail_page_url
        })
    return books

def scrape_all_books():
    all_books = []
    
    for page_num in range(1, 51):
        url = PAGE_URL_TEMPLATE.format(page_num)
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code != 200:
                print(f'Failed to retrieve page {page_num}. Status: {response.status_code}')
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            books_on_page = get_book_data(soup)
            
            if not books_on_page:
                break  
                
            all_books.extend(books_on_page)
            print(f'Scraped page {page_num}, found {len(books_on_page)} books.')
            
            time.sleep(1) 

        except requests.exceptions.Timeout:
            print(f"Connection to page {page_num} timed out. Skipping page.")
            continue
        except requests.exceptions.RequestException as e:
            print(f"An error occurred on page {page_num}: {e}")
            break
            
    return all_books

if __name__ == '__main__':
    print("Starting professional scrape...")
    books = scrape_all_books()
    df = pd.DataFrame(books)
    df.to_csv('books_professional.csv', index=False)
    print(f'Scraped {len(books)} books in total. Saved to books_professional.csv.')