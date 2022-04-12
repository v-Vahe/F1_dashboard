
def do_some():
    return 'foo'


query_identity_tables = ( 
    """
        SELECT DISTINCT TABLE_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE (TABLE_SCHEMA = 'dbo') AND (OBJECTPROPERTY(OBJECT_ID(TABLE_NAME), 'TableHasIdentity') = 1)
    """
)