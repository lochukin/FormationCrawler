import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime


class FormationBot:
    def __init__(self):
        self.brand_name = 'Formation'
        self.main_url = 'https://www.thereformation.com'
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36'
        # }
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.options,
                                        executable_path='/Users/luzhujian/.wdm/drivers/chromedriver/mac64/102.0.5005.61/chromedriver')

    def get_lower_level_links(self) -> dict:
        self.browser.get(self.main_url)
        time.sleep(5)
        page = self.browser.page_source
        soup = bs4.BeautifulSoup(page, "html.parser")

        # only look for 'clothing'
        clothing = soup.select('li.header-flyout__item.level-1')[1]

        # create a dict to store lower_level and its corresponding url
        low_level_dict = dict()

        # flyout is the elements that in the clothing expand nav
        flyout = clothing.select('li.header-flyout__item.level-2.header-flyout__column-start')

        # exclude the first column of expand nav in clothing and the first element (all clothing) in the second column
        for j in range(1, len(flyout)):
            for low_level in flyout[j].select('a.header-flyout__anchor.header-flyout__anchor--list-title'):
                if low_level['id'] == 'flyout-all-clothing':
                    continue
                # some href do not have http as a starter
                href = low_level['href']
                low_level_dict[low_level.getText().replace('\n', '')] = href if href.startswith(
                    "https") else 'https://www.thereformation.com' + href
        return low_level_dict

    def get_product_links(self, url: str, page_amount: int) -> dict:
        url = url + '?page=' + str(page_amount)
        self.browser.get(url)
        time.sleep(10)
        page = self.browser.page_source
        soup = bs4.BeautifulSoup(page, "html.parser")

        product_links = dict()
        for product in soup.select('div.product-tile.product-tile--default'):
            # each div of product have duplicate href, we only need to take the first one
            a = product.find('a', attrs={'class': 'product-tile__anchor', 'data-product-url': 'productShow'})
            href = a['href']

            # the default href has default color information, we can delete them
            # and use the code as the key
            product_links[href.split('?')[0].split('/')[-1].split('.')[0]] = (
                    'https://www.thereformation.com' + href.split('?')[0])
        return product_links

    def find_info_with_link(self, product_url: str, product_code: str, lower_level: str) -> dict:
        # some info like image cannot be easily extracted by original html, therefore we need selenium and chromedriver
        # url = 'https://www.thereformation.com/products/jeune-dress/1310804ZSE.html'
        self.browser.get(product_url)
        time.sleep(5)
        page = self.browser.page_source
        soup = bs4.BeautifulSoup(page, "html.parser")

        product_dict = dict()
        product_dict['product_code'] = product_code
        product_dict['lower_level_name'] = lower_level
        product_dict['brand_name'] = self.brand_name

        # get product display name and remove /n
        product_dict['display_name'] = soup.select_one('h1.pdp__name').getText().replace('\n', '')

        # get price(str) with symbol and remove /n
        product_dict['price'] = soup.select_one('span.price--reduced').getText().replace('\n', '')

        # get product description and remove /n
        product_dict['description'] = soup.select_one('div.cms-generic-copy').getText().replace('\n', '')

        # note: for color and size, not care for selectable or not for now
        # if want to add storage info, can use css selector with class: selectable unselectable to find

        # multiple color use color_list to store
        color_list = []
        for color in soup.select('button.product-attribute__swatch.swatch--color.swatch--color-large'):
            color_list.append(color['title'])
        product_dict['color'] = color_list

        # multiple sizes use size_list to store
        size_list = []
        for size in soup.select('button.product-attribute__anchor.anchor--size'):
            size_list.append(size.getText().replace('/n', ''))
        product_dict['size'] = size_list

        # add product url
        product_dict['product_url'] = product_url

        # get image_links
        image_list = []
        # there are two images carousel inner wrapper, css-8ymejj and css-1l154bu, the first one gets the uncut image
        for image in soup.find('div', attrs={'data-test': 'carousel-inner-wrapper'}).find_all('img'):
            image_list.append(image['src'])
        product_dict['image_links'] = image_list

        # fabric and care
        product_dict['fabric_care'] = soup.select_one('div.pdp__accordion-content.js-pdp-care').getText().replace('\n',
                                                                                                                  ' ')
        # sustanability
        product_dict['sustanability'] = soup.select_one('div.pdp__accordion-content.js-pdp-sustain').getText().replace(
            '\n', ' ')

        product_dict['scrapped_date'] = datetime.date.today()

        print('product {0} collected'.format(product_code))
        return product_dict

    def run(self, low_level_dict=None) -> list[dict]:
        product_info = []
        if not low_level_dict:
            low_level_dict = self.get_lower_level_links()
        for lower_level, lower_level_url in low_level_dict.items():
            # crawl one page for testing
            product_links = self.get_product_links(lower_level_url, 1)
            for product_code, product_url in product_links.items():
                product_info.append(self.find_info_with_link(product_url, product_code, lower_level))
            break
        self.browser.quit()
        return product_info
