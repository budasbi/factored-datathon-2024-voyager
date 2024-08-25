from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import requests
import logging

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 24),  # Set to today's date
    'retries': 1,
}

def fetch_data_from_postgres(**kwargs):
    # Connect to Postgres
    postgres_hook = PostgresHook(postgres_conn_id='postgres_aws')
    # Execute query
    sql = "SELECT * FROM dag_events;"
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    # Fetch data and load it into a DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    # Save the DataFrame to XCom
    kwargs['ti'].xcom_push(key='dataframe', value=df.to_json(orient='split'))

def process_and_send_data(**kwargs):
    # Retrieve the DataFrame from XCom
    df_json = kwargs['ti'].xcom_pull(key='dataframe')
    df = pd.read_json(df_json, orient='split')
    
    # Connect to Postgres
    postgres_hook = PostgresHook(postgres_conn_id='postgres_aws')
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract the value of petal_length
        goldstein = row['goldstein']
        
        # Send the petal_length as raw text to the HTTP endpoint
        try:
            response = requests.post(
                url="https://datathon-122124868216.us-east1.run.app/api/getRisk", 
                data=str(goldstein),  # Send as raw text
                headers={"Content-Type": "text/plain"}  # Indicate the content type as plain text
            )
            # Log the response
            logging.info(f"Response for row {index}: {response.status_code} - {response.text}")
            
            # Insert the result into the dag_model_result table
            response_json = response.json()
            risk_value = response_json[0].get("risk", "unknown")  # Default to "unknown" if "risk" key is missing
            sql_insert = """
                INSERT INTO dag_model_result (risk_result)
                VALUES (%s);
            """
            cursor.execute(sql_insert, (risk_value,))
            connection.commit()
        except Exception as e:
            logging.error(f"Error for row {index}: {str(e)}")
    
    # Close the database connection
    cursor.close()
    connection.close()

with DAG('dag_modelv6',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    fetch_data = PythonOperator(
        task_id='fetch_data_from_postgres',
        python_callable=fetch_data_from_postgres,
        provide_context=True
    )

    process_and_send = PythonOperator(
        task_id='process_and_send_data',
        python_callable=process_and_send_data,
        provide_context=True
    )

    fetch_data >> process_and_send
