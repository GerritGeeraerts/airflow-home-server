from datetime import datetime, timedelta

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
with DAG(
    dag_id="scrapy_vdab_daily",
    default_args=default_args,
    description='Daily execution of scrapy-vdab-prod Docker container',
    schedule_interval='0 4 * * *',  # Daily at 04:00
    start_date=pendulum.datetime(2024, 12, 24, tz="UTC"),
    catchup=False,
    doc_md="""
    ### Scrapy VDAB Daily DAG
    
    This DAG runs the scrapy-vdab-prod Docker container daily at 04:00.
    The container mounts a datalake volume to persist scraped data.
    """,
    tags=["docker", "scrapy", "daily", "vdab"],
) as dag:
    
    # Define the Docker run task
    run_scrapy_vdab_task = BashOperator(
        task_id="run_scrapy_vdab_prod",
        bash_command="""
        docker run -v datalake:/app/scrapy_vdab/data/datalake scrapy-vdab-prod
        """,
    )
