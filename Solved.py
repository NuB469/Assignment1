import requests
import csv
from bs4 import BeautifulSoup
import os

url= 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
# Scrape product listing pages
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
            product_data['URL'] = url


        # Extract product name
        name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        if name:
            product_data['Name'] = name.text.strip()

        # Extract product price
        price = product.find('span', {'class': 'a-offscreen'})
        if price:
            product_data['Price'] = price.text.strip()

        # Extract rating
        rating = product.find('span', {'class': 'a-icon-alt'})
        if rating:
            product_data['Rating'] = rating.text.split()[0]

        # Extract number of reviews
        reviews = product.find('span', {'class': 'a-size-base'})
        if reviews:
            product_data['Reviews'] = reviews.text.strip()

        products.append(product_data)

    return products


# Scrape individual product pages
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_details = {}

    # Extract description
    description = soup.find('div', {'id': 'productDescription'})
    if description:
        product_details['Description'] = description.text.strip()

    # Extract ASIN
    asin = soup.find('th', text='ASIN')
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

    return product_details


def export_to_csv(data, filename):
    keys = data[0].keys()
    filepath = os.path.join("C:/Users/gandh/Downloads", filename)
    print("Data to be exported:", data)  # Print data to check its content
    print("CSV file path:", filepath)  # Print file path to verify it is correct
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(data)



if __name__ == '__main__':
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
    num_pages = 20  # Number of pages
    #print(os.getcwd())

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
