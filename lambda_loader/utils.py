import psycopg2
import json
import operator

# Create RDS connection
def make_conn(db_name, db_user, db_host, db_pass, db_port):
    conn = None
    conn_string = "dbname='%s' user='%s' host='%s' password='%s' port=%s" % (
    db_name, db_user, db_host, db_pass, db_port)
    print(conn_string)
    try:
        conn = psycopg2.connect(conn_string)
    except Exception as e:
        print("I am unable to connect to the database")
        print(e)
        raise e
    return conn

# Execute sql query
def execute_query(conn, query: str, with_commit=True):
    cur = conn.cursor()
    print(f"EXECUTING : {query}")
    cur.execute(query)
    if with_commit:
        conn.commit()
    cur.close()

def import_csv_from_s3(conn, table_name: str, table_schema: str, s3_bucket: str, filepath: str, region_name: str,
                       options: str):
    print(f"LOADING {filepath} FROM BUCKET {s3_bucket} located on region {region_name} into RDS table {table_name}")
    # set datetime style
    execute_query(conn, "set datestyle TO ISO,DMY;")
    
    # truncate table before load
    execute_query(conn, f"trunctate table {table_schema}.{table_name};")
    
    # Import csv file into rds table
    query = f"SELECT aws_s3.table_import_from_s3('{table_schema}.{table_name}', '', '{options}', '{s3_bucket}', '{filepath}', '{region_name}');"

    conn.commit()
    print("SUCCESS")

def map_name_table(file_name: str):

    table_name = "no_table"
    
    if file_name == "":
        table_name = ""

    
    if table_name == "no_table":
        raise Exception(f"no table match with filename, please implement the mapping")

    return table_name
 