import json 
from datetime import datetime
from airflow.models import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

default_args={
    'owner':'david',
    'retries':5
}

with DAG(
    dag_id='api_dag',
    default_args=default_args,
    description='this is our first api call',
    start_date=datetime(2024,8,19),
    schedule_interval='@daily'
) as dag:
    task1=HttpSensor(
        task_id='is_api_active',
        http_conn_id='api_posts',
        endpoint='posts/'
    )

    task2=SimpleHttpOperator(
        task_id='get_posts',
        http_conn_id='api_posts',
        endpoint='posts/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )


    task2