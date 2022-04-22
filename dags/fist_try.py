from airflow.models import DAG
from datetime import datetime


default_arguments = {'owner': 'jdoe','email': 'jdoe@datacamp.com', 'start_date': datetime(2020, 1, 20)}

etl_dag = DAG( 'etl_workflow', default_args=default_arguments )
