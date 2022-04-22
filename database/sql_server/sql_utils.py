import sqlalchemy as sa
import sqlparse
import sqlalchemy as sa
import configparser
print('I am here')
_config = configparser.ConfigParser()
_config.read('database/db.cfg')

engine = sa.create_engine('mssql+pyodbc://{3}:{4}@{1}/{2}?driver={0}'.format(*_config['SQL_DB'].values()))


def create_schema():
    """
    create tables and realationships in SQLServer database
    """
    sql_queries = file_query_reader(
        "./database/sql_server/create_tables.sql"
        )
    with engine.connect() as conn:
        for query in sql_queries:
            result = conn.execute(sa.text(query))
            print(f"{result.rowcount} rows have been updated/selected.")

def drop_tables():
    """
    create tables and realationships in SQLServer database
    """
    with open("./database/sql_server/drop_tables.sql") as sql_file:
        sql_raw = sql_file.read()
        sql_queries = sqlparse.split(
            sqlparse.format(sql_raw, strip_comments=True)
        )
    with engine.connect() as conn:
        for query in sql_queries:
            result = conn.execute(sa.text(query))
            print(f"{result.rowcount} rows have been updated/selected.")

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
            print(row)
            if row != (0,):
                exists = True     
    if not exists:
        print(f'{table_name} is already populated') 
    return exists
    
def df_to_sql(df, table_name):
    try:
        print(f"\n populating {table_name} ...")
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"{table_name} was successfuly populated")
    except Exception as err:
        print(f"{table_name} wasn't populated with the folloing error: \n", err ,'\n')
        raise Exception

def set_identity_insert_on(table_name):
    assert table_name in get_identity_tables()
    query = f"SET IDENTITY_INSERT {table_name} ON"
    with engine.connect() as conn:
        conn.execute(query)

def set_identity_insert_off(table_name):
    assert table_name in get_identity_tables()
    query = f"SET IDENTITY_INSERT {table_name} OFF"
    with engine.connect() as conn:
        conn.execute(query)

def file_query_reader(filepath):
    with open(filepath) as sql_file:
            sql_raw = sql_file.read()
            sql_queries = sqlparse.split(
                sqlparse.format(sql_raw, strip_comments=True)
            )
    return sql_queries

def dispose_engine():
    engine.dispose()


