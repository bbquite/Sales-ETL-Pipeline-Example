from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    dag_id='mart_sales_dag',
    default_args=default_args,
    start_date=datetime(2026, 2, 28),
    schedule_interval='@daily',
    catchup=False,
    tags=['demo', 'mart'],
) as dag:

    # создаем таблицу с выручкой по дням
    daily_revenue = PostgresOperator(
        task_id='create_daily_revenue',
        postgres_conn_id='ETL_example',
        sql="""
            CREATE TABLE IF NOT EXISTS mart_daily_revenue AS
            SELECT 
                date,
                SUM(amount) AS total_revenue
            FROM dwh_sales_clean
            GROUP BY date
            ORDER BY date;
        """
    )

    # создаем таблицу с топ продуктов
    top_products = PostgresOperator(
        task_id='create_top_products',
        postgres_conn_id='ETL_example',
        sql="""
            CREATE TABLE IF NOT EXISTS mart_top_products AS
            SELECT 
                product,
                SUM(amount) AS total_sales
            FROM dwh_sales_clean
            GROUP BY product
            ORDER BY total_sales DESC;
        """
    )

    # создаем таблицу со средним чеком
    avg_order = PostgresOperator(
        task_id='create_avg_order_amount',
        postgres_conn_id='ETL_example',
        sql="""
            CREATE TABLE IF NOT EXISTS mart_avg_order AS
            SELECT 
                AVG(amount) AS avg_amount
            FROM dwh_sales_clean;
        """
    )

    # порядок выполнения DAG
    daily_revenue >> [top_products, avg_order]