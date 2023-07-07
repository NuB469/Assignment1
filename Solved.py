import requests
import csv
from bs4 import BeautifulSoup


# import os

def scrape_product_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

    products = []
    for product in product_list:
        product_data = {}

        # Extract product URL
        link = product.find('a', {'class': 'a-link-normal s-no-outline'})
        if link:
            product_data['URL'] = 'https://www.amazon.in' + link['href']

        # Extract product name
        name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        if name:
            product_data['Name'] = name.text.strip()

        # Extract product price
        price = product.find('span', {'class': 'a-price-whole'})
        if price:
            product_data['Price'] = price.text.strip()

        # Extract rating
        rating = product.find('span', {'class': 'a-icon a-icon-star-small a-star-small-4 aok-align-bottom'})
        if rating:
            product_data['Rating'] = rating.text.split()[0]

        # Extract number of reviews
        reviews = product.find('span', {'class': 'a-size-base s-underline-text'})
        if reviews:
            product_data['Reviews'] = reviews.text.strip()

        products.append(product_data)
        print(product_data)

    return products


def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_details = {}

    # Extract description
    description = soup.find('div', {'id': 'productDescription'})
    if description:
        product_details['Description'] = description.text.strip()

    # Extract ASIN
    asin = soup.find('th', string='ASIN')
    if asin:
        product_details['ASIN'] = asin.find_next('td').text.strip()

    # Extract product description
    prod_description = soup.find('div', {'id': 'feature-bullets'})
    if prod_description:
        desc_list = prod_description.find_all('span', {'class': 'a-list-item'})
        product_details['Product Description'] = '\n'.join([desc.text.strip() for desc in desc_list])

    # Extract manufacturer
    manufacturer = soup.find('a', {'id': 'bylineInfo'})
    if manufacturer:
        product_details['Manufacturer'] = manufacturer.text.strip()

    print(product_details)
    return product_details


def fetch_product_details(product_url):
    # Code to fetch and extract product details from the provided URL
    # Implement your logic here to extract the necessary information
    # Return a dictionary containing the fetched details

    # Example implementation:
    product_details = {
        'Product URL': product_url,
        'Product Name': 'Sample Product Name',
        'Product Price': 'Sample Price',
        'Rating': 'Sample Rating',
        'Number of Reviews': 'Sample Number of Reviews'
    }
    return product_details


def export_to_csv(data, filename):
    fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating',
                  'Number of Reviews']  # Adjust the fieldnames as needed

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product_url in data:
            product_details = fetch_product_details(product_url)
            writer.writerow(product_details)
            print(product_details)


if __name__ == '__main__':
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
    num_pages = 20  # Number of pages

    all_products = []
    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        print(f"Scraping products from page {page}...")
        products = scrape_product_listings(url)
        all_products.extend(products)

    print("Scraping complete.")
    print(f"Total products scraped: {len(all_products)}")

    scraped_product_details = []
    for product in all_products:
        product_url = product['URL']
        print(f"Fetching details for product: {product['Name']}")
        details = scrape_product_details(product_url)
        scraped_product_details.append(details)

    print("Fetching details complete.")

    export_to_csv(scraped_product_details, 'output.csv')
    print("Data exported to CSV file.")
