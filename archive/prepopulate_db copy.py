import os
import pandas as pd
from sql_server.sql_utils import (
    create_schema, 
    df_to_sql, 
    get_identity_tables, 
    set_identity_insert_on, 
    set_identity_insert_off, 
    table_exists, 
    dispose_engine
    )

# initialize the database <> <> <> <> this needs change to makes sure database is not emptied by accident
create_schema()

# open the ordered list of tables
with open('database/sql_server/ordered_tables_list.txt', 'r') as f:
    ordered_tables_list = f.read().splitlines()

# identify the tables with identity constraint
identity_tables = get_identity_tables()

# prepopulate tables with existing data
for table in ordered_tables_list:

    table = os.path.join('database/initial_csv_data',table)
    table_name = os.path.basename(table)[:-4]

    print(f"\n populating {table_name} ...")

    # load csv data into a dataframe
    try:
        df = pd.read_csv(table)
    except FileNotFoundError:
        print("{table_name} File wasn't found")
    except Exception as err:
        print("problem reading {table_name}: ", err)

    # set identity insert on
    if table_name in identity_tables:
            set_identity_insert_on(table_name)
 
   # check if the table is already populated
    if table_exists(table_name) == True: 
        continue

    # clean the dataframe / transform
    df = df.replace([r'\N'],'')
   
    # append to sql table
    try:
        print(df.dtypes)
        # df.to_sql(table_name, engine, if_exists='append', index=False)
        df_to_sql(df, table_name)
        print(f"{table_name} was successfuly populated")
    except Exception as err:
        print(f"{table_name} wasn't populated with the folloing error: \n", err ,'\n')
        raise Exception
    
    # set identity_insert OFF for safety
    if table_name in identity_tables:
        set_identity_insert_off(table_name)

dispose_engine()
