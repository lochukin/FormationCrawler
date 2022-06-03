#!/usr/bin/python

import psycopg2
from config import config


def create_tables():
    commands = (
        """ CREATE TABLE product (
                product_code VARCHAR(255) PRIMARY KEY,
                lower_level_name VARCHAR(255),
                brand_name VARCHAR(255),
                display_name VARCHAR(255),
                price VARCHAR(255),
                description text,
                color VARCHAR[],
                size VARCHAR[],
                product_url VARCHAR(255),
                image_links VARCHAR[],
                fabric_care text,
                sustanability text,
                scrapped_date date
                )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()