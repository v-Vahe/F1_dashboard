#! /usr/bin/venv python

import os
import pandas as pd
from sql_server.sql_utils import (
    create_schema, 
    df_to_sql,
    drop_tables, 
    get_identity_tables, 
    set_identity_insert_on, 
    set_identity_insert_off, 
    table_exists, 
    dispose_engine
    )


def table_list():
    """
    put ordered tables into a list
    """
    with open('database/sql_server/ordered_tables_list.txt', 'r') as f:
        ordered_tables_list = f.read().splitlines()
    return ordered_tables_list

def read_table(table):
    """
    put csv files into a dataframe
    """
    try:
        df = pd.read_csv(table)
    except FileNotFoundError:
        print("{table_name} File wasn't found")
    except Exception as err:
        print("problem reading {table_name}: ", err)
    return df 


def main():

    ordered_tables_list = table_list()
    identity_tables = get_identity_tables()
    
    for table in ordered_tables_list:
        
        table = os.path.join('database/initial_csv_data',table)
        table_name = os.path.basename(table)[:-4]

        # check if the table is already populated
        if table_exists(table_name): 
            print('Database already populated \n')
            response = input(
                "Do you want to drop the tables and repopulate? [Y]/[N]"
                )
            print(response)
            if response.upper() == 'N':
                exit()
            if response.upper() == 'Y':
                drop_tables()
                create_schema()
            else:
                print('invalid response')

        if table_name in identity_tables:
                set_identity_insert_on(table_name)

        # load csv data into a dataframe
        df = read_table(table)
        
        # clean the dataframe / transform
        df = df.replace([r'\N'],'')
    
        # append to sql table
        df_to_sql(df, table_name)
        
        if table_name in identity_tables:
            set_identity_insert_off(table_name)
    
    dispose_engine()
    
if __name__ == '__main__':
    main()