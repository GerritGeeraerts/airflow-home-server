from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

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
dag = DAG(
    'update_public_ip_on_duck_dns',
    default_args=default_args,
    description='A simple DAG to update public IP on Duck DNS',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2023, 1, 1),  # replace with your start date
    catchup=False,
)

# Define the Bash command to activate the virtual environment, run the script, and deactivate the virtual environment
run_script_command = """
cd /opt/airflow/project-code/update-public-ip-on-duck-dns
source /opt/airflow/project-code/update-public-ip-on-duck-dns/.venv/bin/activate
set -e
python /opt/airflow/project-code/update-public-ip-on-duck-dns/main.py
"""

# Define the task
run_script_task = BashOperator(
    task_id='run_update_public_ip_script',
    bash_command=run_script_command,
    dag=dag,
)

# Set up the task in the DAG
run_script_task
