import os
import pandas as pd
import sqlalchemy as sa
from f1_sql_server import F1Database
from logs import logger
from datetime import datetime
from logs import logger 


# uploads sorce csv table into a dataframe
def upload_source_df(file_name):
    file_path = os.path.join(os.getcwd(),
        'f1_pipeline','csv_data', file_name)
    try:
        source = pd.read_csv(file_path).replace([r'\N'],'')
    except Exception as err:
        logger.error(
            f'problem reading {file_name}' + 
            '\n error message: {err}')
        raise
    
    return source


# uploads target sql table into a dataframe
def upload_target_df(table_name, db_engine):
    query = f'Select * FROM {table_name}'
    try:
        target = pd.read_sql(query, db_engine)
    except Exception as err:
        logger.error(
            f'problem uploading {table_name}' + 
            ' \n error message: {err}')
        raise
    
    return target


# detects changes from last etl
def detect_updates(source_df, target_df):
    target_df = target_df.drop(
        labels = ['created_date','modified_date'], 
        axis = 1)
    
    changes = source_df[
        ~source_df.apply(tuple, axis=1).isin(target_df.apply(tuple, axis=1))]

    inserts = changes[
        ~changes.iloc[:,0] \
            .isin(target_df.iloc[:,0])]
   
    modified = pd.DataFrame([])

    return (modified, inserts)


# stages rows to be updated and inserted
def stage_updates(updates_df, inserts_df, table_name):
    staged_update_table = False 
    staged_insert_table = False
    if not updates_df.empty:
        logger.info('')
        updates_df.to_csv(os.path.join(
            os.getcwd(),'f1_pipeline','sql_stage', 
            f'updated_{table_name} {datetime.now()}.csv'))
        staged_update_table = True
    
    if not inserts_df.empty:
        inserts_df.to_csv(os.path.join(
            os.getcwd(),'f1_pipeline', 'sql_stage', 
            f'new_{table_name} {datetime.now()}.csv'))
        staged_insert_table = True

    elif updates_df.empty:
        logger.info('No updates were found!')
        pass

    return (staged_update_table,
        staged_insert_table)


def insert(inserts_df, table_name, engine):
    if not inserts_df.empty:
        inserts_df.to_sql(
            name = table_name, 
            con = f1_db.engine, 
            if_exists ='append', 
            index=False,
            chunksize=200
            )
      


if __name__=='__main__':
    
    f1_db = F1Database()
    
    
    # f1_db.drop_tables()
    # f1_db.create_schema()


    # stage new/updated rows
    updates = {}
    inserts = {}    
    for table_name in f1_db.ordered_tables:
        source_df = upload_source_df(table_name + '.csv')
        target_df = upload_target_df(table_name, f1_db.engine)
        updates_df, inserts_df = detect_updates(source_df, target_df)
        try:
            logger.info(f"attempting to stage '{table_name}' ...")
            update_staged, insert_staged = stage_updates(updates_df, inserts_df, table_name)
            if update_staged == False and insert_staged == False:
                continue
            
            if update_staged:
                updates[table_name] = updates_df    
            
            if insert_staged == True:
                inserts[table_name] =  inserts_df
            
            logger.info(f"staged '{table_name}'")
        
        except Exception as err:
            logger.error(
                f"problem staging '{table_name}'" +
                "'\n' eroor message: {err}")
    

    # insert new into db
    transaction = f1_db.connection.begin()
    try:
  
        for table_name in f1_db.ordered_tables:

            if table_name not in inserts.keys():
                continue
            
            if table_name in f1_db.fetch_identiry_tables():
                f1_db.set_identity_insert_on(table_name)

            inserts[table_name]['created_date'] = datetime.now()
            inserts[table_name]['modified_date'] = datetime.now()
            
            logger.info(f"'inserting new '{table_name}' ...")
            insert(inserts[table_name], table_name, f1_db.engine)

            if table_name in f1_db.fetch_identiry_tables():
                f1_db.set_identity_insert_off(table_name)
            
            logger.info(f"new '{table_name}' inserted")
        
        transaction.commit()
        

    except Exception as err:
        transaction.rollback()
        logger.error(
            'Failed to upsert.' +
            'Rolled back the transaction' +
            f'\n err: {err}')
        


    # update modified rows
    pass

















































































































    # modified = changes[
    #     changes.iloc[:,1] \
    #         .isin(target_df.iloc[:,1])]
    # # print(modified)







    # # inserts_df = inserts_df.reset_index(drop=True)
    # f1_db.set_identity_insert_on('circuits')
    # inserts_df = pd.read_csv('f1_pipeline/csv_data/circuits.csv')
    # print(inserts_df)
    # inserts_df.drop(columns='circuitId')
    # inserts_df['date_added'] = pd.datetime.now()
    # inserts_df.to_sql('circuits', f1_db.engine, if_exists ='replace', index=False)
    # print(inserts_df)
    # f1_db.set_identity_insert_off('circuits')
    

# https://stackoverflow.com/questions/42461959/how-do-i-perform-an-update-of-existing-rows-of-a-db-table-using-a-pandas-datafra

    # f1_db.engine.execution_options(autocommit=False)
    # with f1_db.engine.connect() as conn:
    #     with conn.begin():
    #         # 1. Insert
    #         conn.execute(
    #         “INSERT INTO staff SELECT * FROM tmp_insert_table ;”
    #         )
    #         # 2. Update 
    #         conn.execute( 
    #         “””
    #         UPDATE staff s
    #         INNER JOIN tmp_update_table u ON s.id = u.id
    #         SET s.name_surname = u.name_surname,
    #         s.section = u.section
    #         WHERE s.id = u.id;
    #         “””
    #         )
    #         # 3. Delete
    #         conn.execute(“””
    #         DELETE FROM staff s
    #         WHERE s.id IN (SELECT id from tmp_delete_table); 
    #         “””)




    # conn = f1_db.engine.connect()        
    # query = 
    
    # transact = conn.begin()
    # try:
    #     for q in query:
    #         self.conn.execute(q)
        
    #     if rollback:
    #         transact.commit()
    
    # except Exception as err:
    #     logger.error('Transaction Failed !', err)
    #     if rollback:
    #         transact.rollback()
    #         raise
    # dump_tran_test_table(conn)
#     """console output:
# #     [('old_foo', 1), ('old_bar', 2), ('new_baz', 3)]
# #     """
#     tran.rollback()
#     dump_tran_test_table(conn)
#     """console output:
#     [('old_foo', 1), ('old_bar', 2)]
#     """

    # print(modified_df)
    # print(inserts_df)
    # f1_db = F1Database()

    # # extract and clean the source table
    # source = pd.read_csv('./f1_pipeline/csv_data/circuits.csv')
    # source = source.replace([r'\N'],'')
    
    # # extract the current target table
    # target = pd.read_sql('Select * from circuits', f1_db.engine)
    # print(target)
    # # new changes
    # changes = source[~source.apply(tuple, axis=1).isin(target.apply(tuple, axis=1))]
    
    # # new rows to be updated
    # modified = changes[changes.circuitId.isin(target.circuitId)]
    
    # # new rows to be inserted
    # inserts = changes[~changes.circuitId.isin(target.circuitId)]


    # f1_db.session.upsert(modified, inserts, 'circuits')
    # print(inserts)
    # print(modified)
    # changes = source[~source.apply(tuple,1).isin(target.apply(tuple,1))]