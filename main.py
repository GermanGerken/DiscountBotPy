import math

from bs4 import BeautifulSoup
import requests
import json
import lxml

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'bx-ajax': 'true'
}


def get_page():
    s = requests.Session()
    all_items = []
    for i in range(0, 901, 100):
        url = f'https://usa.tommy.com/ProductListingView?includeLowStockIndicator=true&catalogId=10551&isHomeDepartment=false&pageSize=100&disableProductCompare=true&langId=-1&storeId=10151&categoryId=3074457345617719268&currentCategoryIdentifier=W_ALL_HID&imageBadgeIgnoreCategoryCodeParam=W_ALL_HID&beginIndex={i}&minFacetCount=1&facet=ads_f15527_ntk_cs%3A%22Women%22&colorfacetselected=false'
        response = s.get(url=url, headers=headers)
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        with open('index.html', 'r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        for item in soup.find_all('div', class_='productCell'):
            try:
                discount = item.find('div', class_='promoMessage discount').find('span').text
                discount = discount.replace("\n", "")
                discount = discount.replace("\t", "")
                title = item.find('div', class_='productName').find('a').text
                link = item.find('div', class_='productName').find('a').get('href')
                price = item.find('span', class_='price offerPrice').text
                all_items.append({
                               "title": title,
                               "link": link,
                               "price_base": price,
                               "discount_info": discount
                           })

            except:
                pass
    with open('result_data2.json', 'w', encoding="utf-8") as file:
        json.dump(all_items, file, indent=4, ensure_ascii=False)



def get_json(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def collect_data():
    s = requests.Session()
    response = s.get(url='https://www.michaelkors.com/server/data/guidedSearch?stateIdentifier=_/N-28zn&No=0&Nrpp=42', headers=headers)

    data = response.json()
    #pagination_count = math.ceil(data.get('totalProducts') / 42)
    count = 0
    result_data=[]
    items_urls = []
    print(data)
    #for page_count in range(1, pagination_count + 1):
    #    url = f'https://www.michaelkors.com/server/data/guidedSearch?stateIdentifier=_/N-28zn&No={count}&Nrpp=42'
    #    count += 42
    #    r = s.get(url=url, headers=headers)
#
    #    data = r.json()
    #    products = data.get('productList')

        #for product in products:
        #    product_colors = product.get('colors')
        #    for pc in product_colors:
        #        discount_percent = pc.get('price').get('discountPercent')
        #        if discount_percent != 0 and pc.get("link") not in items_urls:
        #            items_urls.append(pc.get("link"))
        #            result_data.append(
        #                {
        #                    'title': pc.get('title'),
        #                    'category': pc.get('category'),
        #                    'link': f'https://salomon.ru{pc.get("link")}',
        #                    'price_base': pc.get('price').get('base'),
        #                    'price_sale': pc.get('price').get('sale'),
        #                    'discount_percent': discount_percent
        #                }
        #            )
        #print(f'{page_count}/{pagination_count}')
    #with open('result_data.json', 'w', encoding="utf-8") as file:
    #    json.dump(result_data, file, indent=4, ensure_ascii=False)

def main():
    get_page()
    #get_json('https://www.michaelkors.com/server/data/guidedSearch?stateIdentifier=_/N-28zn&No=0&Nrpp=42')
    #collect_data()


main()
