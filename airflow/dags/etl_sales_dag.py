import os
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


CSV_FILE = '/opt/airflow/dags/data/orders.csv'

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

def load_csv_to_raw():
    print("TEST --->", os.getcwd())
    df = pd.read_csv(CSV_FILE)
    pg_hook = PostgresHook(postgres_conn_id='ETL_example')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    # создаем raw таблицу если нет
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_sales (
            order_id INT,
            product VARCHAR(50),
            amount INT,
            date DATE
        );
    """)
    conn.commit()

    # вставка данных
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO raw_sales (order_id, product, amount, date)
            VALUES (%s, %s, %s, %s)
        """, (row['order_id'], row['product'], row['amount'], row['date']))
    conn.commit()
    cursor.close()
    conn.close()
    print("CSV loaded into raw_sales")

def transform_to_dwh():
    pg_hook = PostgresHook(postgres_conn_id='ETL_example')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    # создаем dwh таблицу
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dwh_sales_clean AS
        SELECT 
            order_id,
            product,
            amount,
            date
        FROM raw_sales;
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Data transformed into dwh_sales_clean")

with DAG(
    dag_id='etl_sales_dag',
    default_args=default_args,
    start_date=datetime(2026, 2, 28),
    schedule_interval='@daily',
    catchup=False,
    tags=['demo'],
) as dag:

    load_csv = PythonOperator(
        task_id='load_csv_to_raw',
        python_callable=load_csv_to_raw
    )

    transform = PythonOperator(
        task_id='transform_to_dwh',
        python_callable=transform_to_dwh
    )

    load_csv >> transform