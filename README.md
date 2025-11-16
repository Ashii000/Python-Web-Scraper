**Python Book Website Scraper (books.toscrape.com)**  
This project is a sample Python script designed to scrape data from books.toscrape.com, a fictional book website used for scraping practice.  
This script demonstrates a professional web scraping process, which includes:  

1. Scraping basic data from main catalogue pages.
2. Following links to detail pages for each book.
3. Scraping more detailed information (like UPC, Description, and Stock Count) from the detail pages.
4. Saving all the data into a clean CSV file.


**Features**

. Scrapes Title, Price, and Star Rating from main pages.
. Scrapes UPC, Description, and exact Stock Count from detail pages.
. Polite scraping with a time.sleep(1) delay.
. Includes a User-Agent header.
. Saves all data into a single books_professional.csv file.


**Libraries Used**

. **requests **(for making HTTP requests)
. **beautifulsoup4** (for parsing HTML)
.** pandas** (for saving data to CSV)


**How to Run**

1. Make sure you have Python installed.
2.  Install the required libraries:
     **pip install requests beautifulsoup4 pandas**  
3.Run the script:  
      **python web_scraper.py**  

4. The script will print its progress and create a file named **books_professional.csv** in the same folder.

   
