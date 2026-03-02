from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello():
    print("Hello world")

with DAG(
    dag_id="dag_test",
    start_date=datetime(2026, 1, 25),
    schedule="@daily",
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="test_hello",
        python_callable=hello
    )