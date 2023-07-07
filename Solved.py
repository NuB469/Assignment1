import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from a given URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the page is a valid product page
    if soup.find("span", class_="a-size-medium"):
        # Extract product details
        product_title_element = soup.find("span", class_="a-size-medium")
        product_title = product_title_element.text.strip() if product_title_element else ""

        product_price_element = soup.find("span", class_="a-offscreen")
        product_price = product_price_element.text.strip() if product_price_element else ""

        product_rating_element = soup.find("span", class_="a-icon-alt")
        product_rating = product_rating_element.text.strip() if product_rating_element else ""

        product_reviews_element = soup.find("span", class_="a-size-base")
        product_reviews = product_reviews_element.text.strip() if product_reviews_element else ""

        # Additional scraping within the product page (if required)
        product_description = ""
        product_asin = ""
        product_manufacturer = ""

        return {
            "Title": product_title,
            "Price": product_price,
            "Rating": product_rating,
            "Reviews": product_reviews,
            "Description": product_description,
            "ASIN": product_asin,
            "Product Description": product_description,
            "Manufacturer": product_manufacturer,
        }

    # Return None for non-product pages
    return None

# Base URL for scraping product listing pages
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"

# Number of pages to scrape (at least 20 in this case)
num_pages = 20

# List to store all scraped product details
all_products = []

# Scrape product listing pages
for page in range(1, num_pages + 1):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    products = soup.find_all("div", class_="sg-col-inner")

    # Iterate over products on the current page
    for product in products:
        product_url_element = product.find("a", class_="a-link-normal")
        if product_url_element:
            product_url = "https://www.amazon.in" + product_url_element["href"]
            print("Scraping:", product_url)  # Print the URL being scraped
            product_details = scrape_product_details(product_url)
            if product_details:
                all_products.append(product_details)

        # Limit the number of product URLs to be scraped
        if len(all_products) >= 200:
            break

    # Break the outer loop if the limit of product URLs is reached
    if len(all_products) >= 200:
        break

# Export scraped data to a CSV file
fieldnames = [
    "Title",
    "Price",
    "Rating",
    "Reviews",
    "Description",
    "ASIN",
    "Product Description",
    "Manufacturer",
]

with open("bag_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_products)
