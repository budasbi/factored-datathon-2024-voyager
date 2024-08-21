from datetime import datetime,timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args={
    'owner':'david',
    'retries':5,
    'retru_delay':timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_postgres_operatorv01',
    default_args=default_args,
    description='this is our first dag that we write',
    start_date=datetime(2024,8,18),
    schedule_interval='0 0 * * *'
) as dag:
    task1=PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists dag_runs(
                dt date,
                dag_id character varying,
                primary key (dt,dag_id)
            )
        """

    )

 