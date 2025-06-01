from datetime import datetime, timedelta
from hdfs import InsecureClient
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import ExternalPythonOperator

# from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
import pandas as pd

def create_folder_hdfs():
    client = InsecureClient('http://namenode:9010', user='hdfs')
    client.makedirs('/data_lake/raw')
    client.makedirs('/data_lake/staging')
    client.makedirs('/data_lake/mart')
    client.makedirs('/checkpoints/kafka_data')
    client.makedirs('/data_lake/raw/batch_data')
    client.makedirs('/data_lake/raw/kafka_data')
    
with DAG(
    dag_id='json_batch_pipeline',
    start_date=days_ago(1),
    schedule_interval='00 5 * * *',
    max_active_runs=1,
    tags=["pipeline"],
    default_args={
        "owner":"Airflow"
    }
) as das:
    
    start_operator = EmptyOperator(task_id='start_operator')

    install_libs = BashOperator(
        task_id = 'install_libs',
        bash_command='pip3.9 install requests-kerberos hdfs'
    )

    create_folder_hdfs_operator = ExternalPythonOperator(
        task_id = "create_folder_hdfs",
        python="/usr/local/bin/python3.9",
        python_callable=create_folder_hdfs   
    )

    