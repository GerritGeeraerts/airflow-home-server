initialize airflow, do not skip this step:
docker compose up airflow-init

run airflow:
docker compose up

go to localhost:8080 log in
run the the task initialize_database manualy, from this point on the other tasks will work correctly

in http://localhost:5050 you can login with admin@example.com admin
here you can vew the databases that are being filled by the dags