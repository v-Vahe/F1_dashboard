import os
import urllib
import pandas as pd
import sqlalchemy as sa

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=localhost;"
                                 "DATABASE=formula1;"
                                 "UID=sa;"
                                 "PWD=Vahe1996")

engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# with engine.connect(f"SELECT count({df.columns[1]}) FROM {table_name}") as conn:
#     conn.execute()

# print(os.listdir('ergast_db'))

with open('ergast_db/ordered_tables_list.txt', 'r') as f:
    ordered_tables_list = f.read().splitlines()

# identify the tables with identity constraint
with engine.connect() as conn:
    result = conn.execute(
        """
        SELECT DISTINCT TABLE_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE (TABLE_SCHEMA = 'dbo') AND (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
        """
        )
    identity_tables = []
    for row in result:
        identity_tables.append(row[0])
    print(identity_tables)


# prepopulate tables with existing data
for table in ordered_tables_list:
    print(table)
    table_name = 'ergast_db/' + os.path.basename(table)[:-4]
    print(table_name)
    table_exists = False
    print(f"\n populating {table_name} ...")

    # csv into dataframe
    try:
        table_path = 'f1_pipeline/' + table 
        print(table_path)
        df = pd.read_csv(table_path)
    except FileNotFoundError:
        print("{table_name} File wasn't found")
    except Exception as err:
        print("problem reading {table_name}: ", err)
   
    # check if the table is already populated
    with engine.connect() as conn:
        table_name = table_name.split('/')[1]    
        if table_name in identity_tables:
            conn.execute(f"SET IDENTITY_INSERT {table_name} ON")
        result = conn.execute(f"SELECT count({df.columns[1]}) FROM {table_name}")
        for row in result:
            if row != (0,):
                print(row)
                print(f"table {table_name} is already pre-populated \n Skippint {table_name} ...")
                table_exists = True
    
    if table_exists == True: continue

    # clean the dataframe / transform
    df = df.replace([r'\N'],'')

    
    # append to sql table
    try:
        print(df.dtypes)
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"{table_name} was successfuly populated")
    except Exception as err:
        print(f"{table_name} wasn't populated with the folloing error: \n", err ,'\n')
        raise Exception
    
    # set identity_insert OFF for safety
    if table_name in identity_tables:
        with engine.connect() as conn:
            conn.execute(f"SET IDENTITY_INSERT {table_name} OFF")
engine.dispose()