![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/docker--compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Proxmox](https://img.shields.io/badge/Proxmox-E57000?style=for-the-badge&logo=proxmox&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

# Airflow setup

I am **orchestrating** all my **Data Ingestion**, **ETL** and other script on an **airflow** server that I am running on
my **dedicated Docker VM** that runs on my **proxmox server** and leverage the scheduled backups of my proxmox server. You can
find more details about my proxmox setup soon. I followed the official documentation
for [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
To be able to run Dockers from inside my airflow docker I avoided a complex **Docker-in-Docker** (**DinD**) approach,
which can lead to issues with storage drivers and build caching, I implemented a more robust **Docker-out-of-Docker** (*
*DooD**) configuration. This method involves mounting the host's Docker socket into the Airflow containers, allowing
them to communicate with the host's Docker daemon. This creates"sibling" containers on the host rather than nested ones,
providing a cleaner, more efficient, and stable architecture. This decision was heavily influenced by Jérôme
Petazzoni's, the the author of the feature that made it possible for Docker to run inside a Docker recommendation, read
more about [Using Docker-in-Docker, Think twice.](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)

Representation in a chart:
```mermaid
graph LR
    subgraph HostVM["Proxmox Server"]
        subgraph Containers["Docker VM"]
            DockerSocket["Host Docker Socket"]
            subgraph DockerContainer["Docker Containers"]
                AirflowContainer["Airflow Docker"]
                OtherContainer["Sibling Docker"]
            end
        end
    end

    AirflowContainer -->|sends docker run| DockerSocket
    DockerSocket -.->|runs| OtherContainer
%% Styling for arrows
    linkStyle 0 stroke: red, stroke-width: 2px, color: red    %% Airflow request sequence AirflowContainer to DockerSocket
    linkStyle 1 stroke: red, stroke-width: 2px, color: red    %% Airflow request sequence DockerSocket to OtherContainer
%% Notes:
%% - Arrows for the user request sequence (User sending 'docker run' to DockerSocket, which runs AirflowContainer) are colored blue.
%% - Arrows for the Airflow request sequence (AirflowContainer sending 'docker run' to DockerSocket, which runs OtherContainer) are colored red.
%% - Airflow Docker and Another Docker are shown in parallel within the Docker Container subgraph.
%% - Docker Socket is explicitly placed inside the Docker VM to show it runs there.
```

# Remarks on installations

In our team I saw these step where most often forgotten by my team members at Becode.
Do not forget to set the `AIRFLOW_UID` by `echo -e "AIRFLOW_UID=$(id -u)" > .env` an also do not forget to initialize
the airflow by running `docker compose up airflow-init`