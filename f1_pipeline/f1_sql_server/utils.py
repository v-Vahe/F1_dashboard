# import sqlalchemy as sa
# from sqlite3 import ProgrammingError
# from distutils.log import error
# from inspect import trace
# from numpy import roll
# from unittest import result
# from pendulum import now
# from requests import Session
from debugpy import connect
from sqlalchemy import create_engine, text
import sqlparse
import configparser
import sys
import os
import pandas as pd

sys.path.insert(0, './f1_pipeline')
from logs import logger


class F1Database:

    def __init__(self, config_file = 'f1_pipeline/db.cfg', config_name = 'SQL_DB'):
        self.engine = self.engine_create(config_file,config_name)
        self.session = Session(self.engine)
        self.constraints = pd.read_csv(
            'f1_pipeline/f1_sql_server/db_constraints.csv')
        self.connection = self.engine.connect()
        # self.transaction = self.connection.begin()
        self.ordered_tables = self.fetch_ordered_tables()

    def fetch_identiry_tables(self):
        query = """
        SELECT DISTINCT(TABLE_NAME)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE (TABLE_SCHEMA = 'dbo') AND 
            (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
        """
        return self.session.fetch(query)

    def fetch_table_names(self):
        query = """
        SELECT DISTINCT(TABLE_NAME)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE (TABLE_SCHEMA = 'dbo') 
        """
        return self.session.fetch(query)


    def fetch_fk_constraints(self, to_table_name):
        fk_df = self.constraints[
            (self.constraints['CONSTRAINT_NAME'].str.contains(to_table_name)) &
            (self.constraints['CONSTRAINT_TYPE']=='FOREIGN KEY')
        ]
        return fk_df

    def fetch_ordered_tables(self):
        return ['circuits',
                'races',
                'drivers',
                'constructors',
                'qualifying',
                'lap_times',
                'pit_stops',
                'seasons',
                'status',
                'constructor_results',
                'constructor_standings',
                'driver_standings',
                'results']


    def create_schema(self, create_queries = "./f1_pipeline/f1_sql_server/create_tables.sql"):
        """
        create tables and realationships in SQLServer database
        """
        logger.info('Transaction begins ...')
        try:
            self.session.execute(create_queries, self.connection)
            logger.info('Transactions completed succesfully !')
        except Exception as err:
            logger.error('Transaction Feiled !' + err)
            raise


    def drop_tables(self, drop_queries = "./f1_pipeline/f1_sql_server/drop_tables.sql"):
        """
        drop all database tables
        """
        logger.info('Transaction begins ...')
        try:
            self.session.execute(drop_queries, self.connection)
            logger.info('Transactions completed succesfully !')
        except Exception as err:
            logger.error('Transaction Feiled !')
            print(err)
            raise


    def drop_fk_constraints(self, table_name):
        fk_df = self.fetch_fk_constraints(table_name)
        print(fk_df)
        try:
            for row in fk_df.itertuples():
                print(row)
                query = f""" 
                ALTER TABLE {row.TABLE_NAME}
                DROP CONSTRAINT {row.CONSTRAINT_NAME};
                """
                print(query)
                self.session.execute(query)
        except Exception as err:
            logger.error('Transaction failed!' +
            f'\n {err}')
            pass
        
    def add_fk_constraints(self, table_name):
        fk_df = self.fetch_fk_constraints(table_name)
        try:
            for row in fk_df.itertuples():
                query = f""" 
                ALTER TABLE {row.TABLE_NAME}
                ADD CONSTRAINT {row.CONSTRAINT_NAME}
                FOREIGN KEY ({row.CONSTRAINT_NAME.split('_')[1]})
                REFERENCES {row.CONSTRAINT_NAME.split('_')[2]}({row.CONSTRAINT_NAME.split('_')[1]});
                """
                self.session.execute(query)
        except Exception as err:
            logger.error('Transaction failed!' +
            f'\n {err}')
            pass

    def engine_create(self, config_file, config_name):
        _config = configparser.ConfigParser()
        _config.read(config_file)
        _config_string = 'mssql+pyodbc://{3}:{4}@{1}/{2}?driver={0}&Mars_Connection=YES'
        url = _config_string.format(*_config[config_name].values())
        return create_engine(url)

    def set_identity_insert_on(self, table_name):
        assert table_name in self.fetch_identiry_tables()
        query = f"SET IDENTITY_INSERT {table_name} ON"
        with self.engine.connect() as conn:
            conn.execute(query)

    def set_identity_insert_off(self, table_name):
        assert table_name in self.fetch_identiry_tables()
        query = f"SET IDENTITY_INSERT {table_name} OFF"
        with self.engine.connect() as conn:
            conn.execute(query)


class Session:

    def __init__(self, engine):
        self.engine = engine
        self.conn = self.engine.connect()


    def execute(self, query, connection = None):
        if connection == None:
            connection = self.conn 
        query = self._query_parser(query)      
        for q in query:
            connection.execute(q)


    def query_table(self, query):
        query = self._query_parser(query)
        return pd.read_sql(query, self.engine) 


    def fetch(self, query):
        query = self._query_parser(query)
        results = []
        for q in query:
            result = self.conn.execute(q)
            if len(query) > 1:
                results.append([row[0] for row in result])
            else:
                results = [row[0] for row in result]       
        return results       
    
    
    def _query_parser(self,query):
        if query[-4:] == '.sql':
            with open(query) as sql_file:
                query = sql_file.read()
        
        query = sqlparse.split(
                    sqlparse.format(
                        query, strip_comments=True
                    )
                )
        return query


if __name__=='__main__':
    f1_db = F1Database()
    # f1_db.create_schema()
    # f1_db.drop_tables()
    # f1_db.transaction.commit()
    # trans1 = f1_db.session1.transaction
    # trans2 = f1_db.session2.transaction
    # print(id(trans1))
    # print(id(trans2))
    f1_db.set_identity_insert_on('circuits')
    # f1_db.set_identity_insert_off('circuits')
    
    # f1_db.drop_fk_constraints('circuits')
    # f1_db.add_fk_constraints('circuits')
    
    
    
    


        # def query_all_constraints(self):
        # query = f"""
        # SELECT * 
        # FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS;
        # """
        # return self.session.query_table(query)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    









# circuits.csv
# races.csv
# drivers.csv
# constructors.csv
# qualifying.csv
# lap_times.csv
# pit_stops.csv
# seasons.csv
# status.csv
# constructor_results.csv
# constructor_standings.csv
# driver_standings.csv
# results.csv






#--------------------------------------------------------------------------------------

# from sqlalchemy import create_engine, text
# import sqlparse
# import configparser
# import sys
# import os
# import pandas as pd

# sys.path.insert(0, './f1_pipeline')
# from logs import logger

# # What do I have now ?
# # query_execute()
# # if given a connection it will use the connection so that rollback can be used inside many executions

# class F1Database:

#     def __init__(self, config_file = 'f1_pipeline/db.cfg', config_name = 'SQL_DB'):
#         self.engine = self.engine_create(config_file,config_name)
#         self.session = Session(self.engine)

#     def upsert(self, update_df, insert_df, table_name, rollback = True):
#         assert table_name in self.fetch_table_names(), \
#             f"{table_name} is doesn't exist in the database"
#         print('hello')
        
#         print('hello')

#     def fetch_last(self, table_name):
#         query = f"""
#         SELECT TOP 1 *
#         FROM {table_name}
#         ORDER BY date_added desc
#         """
#         return self.session.query_table(query)


#     def fetch_identiry_tables(self):
#         query = """
#         SELECT DISTINCT(TABLE_NAME)
#         FROM INFORMATION_SCHEMA.COLUMNS
#         WHERE (TABLE_SCHEMA = 'dbo') AND 
#             (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
#         """
#         return self.session.fetch(query)

#     def fetch_table_names(self):
#         query = """
#         SELECT DISTINCT(TABLE_NAME)
#         FROM INFORMATION_SCHEMA.TABLES
#         WHERE (TABLE_SCHEMA = 'dbo') 
#         """
#         return self.session.fetch(query)

#     def fetch_fk_constraints(self, table_name):
#         query = f"""
#         SELECT * --TABLE_NAME, CONSTRAINT_TYPE,CONSTRAINT_NAME
#         FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
#         WHERE CONSTRAINT_TYPE = 'FOREIGN KEY'
#             and CONSTRAINT_NAME like '%{table_name}%';
#         """
#         return self.session.query_table(query)

#     def fetch_primary_keys_of():
#         pass

#     def create_schema(self, create_queries = "./f1_pipeline/f1_sql_server/create_tables.sql"):
#         """
#         create tables and realationships in SQLServer database
#         """
#         logger.info('Transaction begins ...')
#         try:
#             self.session.execute(create_queries, rollback= False)
#             logger.info('Transactions completed succesfully !')
#         except Exception as err:
#             logger.error('Transaction Feiled !')
#             print(err)
#             raise


#     def drop_tables(self, drop_queries = "./f1_pipeline/f1_sql_server/drop_tables.sql"):
#         """
#         drop all database tables
#         """
#         logger.info('Transaction begins ...')
#         try:
#             self.session.execute(drop_queries)
#             logger.info('Transactions completed succesfully !')
#         except Exception as err:
#             logger.error('Transaction Feiled !')
#             print(err)
#             raise
    
#     def drop_foreign_constraint(self, table_name):
#         fk_df = self.fetch_fk_constraints(table_name)
#         for fk_constraint in fk_df['constraint_name']:
#             query = f""" 
#             ALTER TABLE Persons
#             DROP CONSTRAINT {fk_constraint};
#             """
#             self.sessin.execute(query)

#     def engine_create(self, config_file, config_name):
#         _config = configparser.ConfigParser()
#         _config.read(config_file)
#         _config_string = 'mssql+pyodbc://{3}:{4}@{1}/{2}?driver={0}&Mars_Connection=YES'
#         url = _config_string.format(*_config[config_name].values())
#         return create_engine(url)

#     def set_identity_insert_on(self, table_name):
#         assert table_name in self.fetch_identiry_tables()
#         query = f"SET IDENTITY_INSERT {table_name} ON"
#         with self.engine.connect() as conn:
#             conn.execute(query)

#     def set_identity_insert_off(self, table_name):
#         assert table_name in self.fetch_identiry_tables()
#         query = f"SET IDENTITY_INSERT {table_name} OFF"
#         with self.engine.connect() as conn:
#             conn.execute(query)


# class Session:

#     def __init__(self, engine):
#         self.engine = engine
#         self.conn = self.engine.connect()


#     def execute(self, query, rollback = True):
#         query = self._query_parser(query)
#         if rollback:
#             transact = self.conn.begin()
#         try:
#             for q in query:
#                 self.conn.execute(q)
            
#             if rollback:
#                 transact.commit()
        
#         except Exception as err:
#             logger.error('Transaction Failed !', err)
#             if rollback:
#                 transact.rollback()
#                 raise
    

#     def query_table(self, query):
#         # query = self._query_parser(query)
#         return pd.read_sql(query, self.engine) 


#     def fetch(self, query):
#         query = self._query_parser(query)
#         results = []
#         for q in query:
#             result = self.conn.execute(q)
#             if len(query) > 1:
#                 results.append([row[0] for row in result])
#             else:
#                 results = [row[0] for row in result]       
#         return results       
    
    
#     def _query_parser(self,query):
#         if query[-4:] == '.sql':
#             with open(query) as sql_file:
#                 query = sql_file.read()
        
#         query = sqlparse.split(
#                     sqlparse.format(
#                         query, strip_comments=True
#                     )
#                 )
#         return query


# if __name__=='__main__':
#     f1_db = F1Database()
#     fk_df = f1_db.fetch_fk_constraints('circuits')
#     print(fk_df)













#--------------------------------------------------------------------------------------



    
    # def fetch_last(self, table_name):
    #     query = f"""
    #     SELECT TOP 1 *
    #     FROM {table_name}
    #     ORDER BY date_added desc
    #     """
    #     return self.session.query_table(query)
    
    
    # query = """
    #     SELECT DISTINCT TABLE_NAME
    #     FROM INFORMATION_SCHEMA.COLUMNS
    #     WHERE (TABLE_SCHEMA = 'dbo') AND (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
    #     """
    # query  = './f1_pipeline/f1_sql_server/create_tables.sql'
    
    
    # f1_db.engine.dispose()
    # print(result)
    # conn = f1_db.session.conn
    # transact = conn.begin()
    # try:
    #     conn.execute('create table a (i int)')
    #     transact.commit()
    #     conn.execute('create table a (i int)')
    #     transact.commit()
    # except:
    #     transact.rollback()
    # finally:
    #     transact.close()
    # conn.close()

# class F1Database:

#     def __init__(self, config_file = 'f1_pipeline/db.cfg', config_name = 'SQL_DB'):
#         session = F1Session(config_file, config_name)




#     def query_identity_tables(self):
#         """
#         return tables with identity constraint
#         """
#         query = """
#         SELECT DISTINCT TABLE_NAME
#         FROM INFORMATION_SCHEMA.COLUMNS
#         WHERE (TABLE_SCHEMA = 'dbo') AND (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
#         """
#         return [row[0] for row in self.query_execute_result(query)]
    
#     def engine_dispose(self):
#         self.engine.dispose()

    # def get_all_tables():
    #      """
    #     return all tables currently defined
    #     """
    #     query = """
    #         SELECT DISTINCT TABLE_NAME
    #         FROM INFORMATION_SCHEMA.COLUMNS
    #         WHERE (TABLE_SCHEMA = 'dbo') AND (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
    #         """
    #     return session.executor.query(query,engine)

    # def table_exist(self,table_name):
        # query = f"SELECT count(*) FROM {table_name}"
# 
        # with engine.connect() as conn:
        #     try:
        #         result = conn.execute(query)
        #     except sa.exc.ProgrammingError as err:
        #         return False
        #     exists = False
        #     for row in result:
        #         print(row)
        #         if row != (0,):
        #             exists = True     
        # if not exists:
        #     print(f'{table_name} is already populated') 
        # return ?.query_execute_result(query)
        



# class Executor:
#     def __init__(self, engine)


# class F1Session():
#     def __init__(self, config_file, config_name):
#         f1_db = F1Database()
#         self.engine = self.engine_create(config_file,config_name)
#         self.engine = f1_db.engine 

#     def file_query_reader(self,filepath):
#         with open(filepath) as sql_file:
#             sql_raw = sql_file.read()
#         return sqlparse.split(
#                     sqlparse.format(
#                         sql_raw, strip_comments=True
#                     )
#                 )
#     def engine_create(self, config_file, config_name):
#         _config = configparser.ConfigParser()
#         _config.read(config_file)
#         _config_string = 'mssql+pyodbc://{3}:{4}@{1}/{2}?driver={0}&Mars_Connection=YES'
#         url = _config_string.format(*_config[config_name].values())
#         return create_engine(url)
    # def execute_query():

    # def execute_query_result():
    



   












   
    # def create_schema(self, create_queries = "./f1_pipeline/f1_sql_server/create_tables.sql"):
    #     """
    #     create tables and realationships in SQLServer database
    #     """
    #     logger.info('Transaction begins ...')
    #     try:
    #         self.query_execute(create_queries, rollback= False)
    #         logger.info('Transactions completed succesfully !')
    #     except Exception as err:
    #         logger.error('Transaction Feiled !')


    # def query_execute(self, queries, rollback = False, logger = True, connection = None):
    #     assert not (rollback & connection), 'connection was passed, rollback manually'
        
    #     if queries[-4:] == '.sql':
    #         queries = self.file_query_reader(queries)
    
    #     if rollback:
    #         self._conn_execute_transact(queries, _logger = logger)        
    #     else:
    #         self._conn_execute(queries, connection, _logger = logger, )


    # def query_execute_result(self, query, rise_error = False):
    #     if query[-4:] == '.sql':
    #         query = self.file_query_reader(query)
    #     with self.engine.connect() as conn:
    #         try:
    #             result = conn.execute(text(query))
    #         except Exception as err:
    #             if rise_error:
    #                 logger.error(err)
    #                 raise
    #             else:
    #                 print(err)
    #         result_list = [row for row in result]
    #     return result_list

    # def _conn_execute(self, queries, conn, _logger = True ):
    #     if conn == None:
    #         conn = self.engine.connect()            
    #     for query in queries:
    #         try:
    #             conn.execute(text(query))
    #         except Exception as err:
    #             if _logger:
    #                 logger.error(err)
    #             else:
    #                 print(err.args[1])
    #             pass
    #         finally:
    #             conn.close()

    # def _conn_execute_transact(self, queries, _logger = True):
    #     with self.engine.connect() as conn:
    #         with conn.begin() as transact:   
    #             for query in queries:
    #                 try:
    #                     conn.execute(text(query))
    #                     transact.commit()
    #                 except Exception as err:
    #                     if _logger:
    #                         logger.error(err)
    #                     transact.rollback()
    #                     raise
    #                 finally:
    #                     conn.close()
      

    # def drop_tables():
    #     """
    #     create tables and realationships in SQLServer database
    #     """
    #     path = "./database/sql_server/drop_tables.sql"




    # def df_to_sql(df, table_name):
    #     try:
    #         print(f"\n populating {table_name} ...")
    #         df.to_sql(table_name, engine, if_exists='append', index=False)
    #         print(f"{table_name} was successfuly populated")
    #     except Exception as err:
    #         print(f"{table_name} wasn't populated with the folloing error: \n", err ,'\n')
    #         raise Exception

    # def set_identity_insert_on(table_name):
    #     assert table_name in get_identity_tables()
    #     query = f"SET IDENTITY_INSERT {table_name} ON"
    #     with engine.connect() as conn:
    #         conn.execute(query)

    # def set_identity_insert_off(table_name):
    #     assert table_name in get_identity_tables()
    #     query = f"SET IDENTITY_INSERT {table_name} OFF"
    #     with engine.connect() as conn:
    #         conn.execute(query)
