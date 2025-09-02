FROM apache/airflow:2.9.0
# Change to the root user to install system-wide dependencies
USER root

# Install build-essential, wget, and other necessary packages for TA-Lib
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    tar \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Install Dot NET 8.0 SDK
RUN apt-get update && apt-get install -y dotnet-sdk-8.0 && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y ca-certificates curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli

# Add the airflow user to the docker group to allow it to use the docker socket. 
# The GID of the docker group on the host is usually 999 or similar. 
# A more robust solution is to match the host's GID, but this often works. 
# First, create the group 'docker', then add 'airflow' user to it. 

RUN groupadd -g 999 docker || true && usermod -aG docker airflow 

# Switch back to airflow user
USER airflow
# ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION}
RUN #pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
