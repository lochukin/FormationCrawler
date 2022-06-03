from FormationCrawler import FormationBot
from insert_data import insert

if __name__ == '__main__':
    reformationRobot = FormationBot()

    lower_level = reformationRobot.get_lower_level_links()
    print(lower_level)
    print('Lower_level data collected!')

    product_info = reformationRobot.run(lower_level)
    print(product_info)
    print('Product_info data collected!')

    print('Begin insert data')

    print('Insert product data')
    insert('product', product_info)
    print('Product data insert successfully!')



