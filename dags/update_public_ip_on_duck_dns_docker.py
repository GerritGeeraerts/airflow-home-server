from datetime import timedelta

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="duckdns_public_ip_updater_bash",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    # Run every 15 minutes. Adjust as needed.
    schedule_interval=timedelta(hours=1),
    catchup=False,
    doc_md="""
    ### DuckDNS IP Updater DAG (Bash Version)

    This DAG uses a BashOperator to run the `docker run` command directly.
    """,
    tags=["docker", "networking"],
) as dag:
    # Remember to use the FULL HOST PATHS in the command, because the command
    # is passed to the Docker Daemon running on the host.
    run_docker_command_task = BashOperator(
        task_id="run_duckdns_updater_via_bash",
	bash_command="""
	id ; docker run --rm --name duckdns-updater-task \
  	-v "/home/gg/airflow-volume-project-code/update-public-ip-on-duck-dns/last_public_ip.txt:/app/last_public_ip.txt:z" \
  	-v "/home/gg/airflow-volume-project-code/update-public-ip-on-duck-dns/.env:/app/.env:ro" \
  	--user 1000:0 \
  	duckdns-updater
	""",
)
