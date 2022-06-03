## Introduction
- FormationCrawler.py: code for webscrapping
- main.py: code for executing
- conncet.py: connecting to localhost postgresql database
- create_table.py: create table in postgresql
- insert_data.py: insert scrapped data in postgresql
- postgres_public_product_examples.md: sample data

## Strategy For Scrapping The Whole Website (www.thereformation.com)
1. Get all the names and links of low level categories on the font page:
   1. For starter, I can get all the high level categories from the upper flyout on the home page.
   2. Only scrap the links under 'Clothing' for now, because the categories under 'Clothing' include most of the other high level categories.
   3. Exclude the first column and the 'All Clothing' in the second column under 'Clothing' since there may be duplicated data.
   4. get all the low level names and links using FormationCrawler.get_lower_level_links(), return a dict with low level name as the key and link as the value.
2. Get product links:
   1. From the low level links, I can get to each category page, and I can get all the product links at one time by adding large-number page attribute to the url. 
   2. Then I collected all the product links
   3. return a dict with product code (extract from product link) as key and product link as value
3. Get product info:
   1. From the product links, I can get to specific product page.
   2. scrap all the information.
4. Store the data in PostGRESQL database:
   1. Create table in database using create_tales.py
   2. Insert data in database using insert_data.py

## Strategy For new data
After building a table of all the products from the website, we can get new product by getting low level categories starting with 'new' to get new products in our database which may be faster but lead to incompleteness.

## Strategy For updating data
There are columns 'scrapped_date' and 'product_link' in the table, by testing if product links is still available, more specifically, if the product is no longer available, the product's website will show no product details and show some error messages.
The strategy should be testing the earliest data and check if they are unavailable, if so, drop them from the table.
