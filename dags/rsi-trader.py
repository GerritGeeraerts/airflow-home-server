from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'max_active_runs':15,
}

# Create the DAG
dag = DAG(
    'rsi-trader',
    default_args=default_args,
    description='A script for trading on rsi signals',
    schedule_interval=timedelta(minutes=3),
    start_date=datetime(2024, 12, 24, 11, 19),  # replace with your start date
    catchup=False,
)

# Define the Bash command to activate the virtual environment, run the script, and deactivate the virtual environment
run_script_command = """
cd /opt/airflow/project-code/rsi-trader
source /opt/airflow/project-code/rsi-trader/.venv/bin/activate
set -e
python /opt/airflow/project-code/rsi-trader/main.py
"""

# Define the task
run_script_task = BashOperator(
    task_id='run_rsi_trader',
    bash_command=run_script_command,
    dag=dag,
)

# Set up the task in the DAG
run_script_task
