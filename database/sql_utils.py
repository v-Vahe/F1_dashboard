import urllib
import sqlalchemy as sa
import pandas as pd
from sql_queries import do_some


params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=localhost;"
                                 "DATABASE=formula1;"
                                 "UID=sa;"
                                 "PWD=Vahe1996")

engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))



def get_identity_tables():
    """
    return tables with identity constraint
    """
    query = """
        SELECT DISTINCT TABLE_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE (TABLE_SCHEMA = 'dbo') AND (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
        """
    with engine.connect() as conn:
        result = conn.execute(query)
        identity_tables = []
        for row in result:
            identity_tables.append(row[0])
        return identity_tables

def table_exists(table_name):
    """
    return True if table exists, else return False
    """
    query = f"SELECT count(*) FROM {table_name}"
    with engine.connect() as conn:
        try:
            result = conn.execute(query)
        except sa.exc.ProgrammingError as err:
            return False
        exists = False
        for row in result:
            if row != (0,):
                exists = True        
        return table_exists
    
def df_to_sql(df, table_name):
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"{table_name} was successfuly populated")
    except Exception as err:
        print(f"{table_name} wasn't populated with the folloing error: \n", err ,'\n')
        raise Exception

def set_identity_insert_on(table_name):
    query = f"SET IDENTITY_INSERT {table_name} ON"
    with engine.connect() as conn:
        conn.execute(query)

def set_identity_insert_off(table_name):
    assert table_name in get_identity_tables()
    query = f"SET IDENTITY_INSERT {table_name} OFF"
    with engine.connect() as conn:
        conn.execute(query)

def dispose_engine():
    engine.dispose()

if __name__ == '__main__':
    df = pd.read_csv('./database/initial_csv_data/circuits.csv')
    print(table_exists('ss'))
