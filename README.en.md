# 📊 Sales ETL Pipeline –> Airflow + PostgreSQL + Superset

## Architecture

Apache Airflow – orchestration ETL
PostgreSQL – DWH
Apache Superset – visualization
Docker – containerization

## Run

    git clone 
    docker compose build --no-cache
    docker compose up
    docker exec -it superset superset fab create-admin
    docker exec -it superset superset init
    
### Web services

*   **Airflow** -> http://localhost:5053
*   **Superset** -> http://localhost:5054
*   **client-postgres** -> localhost:5051

## 🔄 Data Flow

Data is loaded from CSV (data/orders.csv) into the raw layer via Airflow.
It is then cleaned and transferred to the DWH layer.
After this, aggregated mart displays are created in a separate DAG.
Superset connects only to the mart tables and builds the dashboard.
This maintains the **raw → dwh → mart architecture** and the separation of responsibilities between layers.


