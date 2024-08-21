from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args={
    'owner':'david',
    'retries':5,
    'retru_delay':timedelta(minutes=2)
}

with DAG(
    dag_id='oir_first_dag_v4',
    default_args=default_args,
    description='this is our first dag that we write',
    start_date=datetime(2024,8,18,2),
    schedule_interval='@daily'
) as dag:
    task1=BashOperator(
        task_id='first_task',
        bash_command='echo hello world this is the first task'
    )

    task2=BashOperator(
        task_id='second_task',
        bash_command='echo hey i am the second task and I will be running after the firdt task'
    )

    task3=BashOperator(
        task_id='third_task',
        bash_command='echo hey i am the third task and I will be running at the same time that task 2'
    )
    task1.set_downstream(task2)
    task1.set_downstream(task3)