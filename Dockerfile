# official python image as parent image
FROM python:3.11-slim

# working directory
WORKDIR /app

#copy files into"/app" container
COPY . /app

# upgrade pip before install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install curl to hit first endpoint to show backend status NOTE: DONT CHANGE ORDER OF RUN COMMANDS: This runs as root since lines:16 & 20 haven't run yet
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# create a new group 
RUN groupadd -r devgroup

# create a new user and add it to the new group
RUN useradd -r -g devgroup backend_container

# change ownership of the files in /app to be owned by backend_container in the "devgroup" group
RUN chown -R backend_container:devgroup /app 
# make launch.sh executable 
RUN chmod +x launch.sh


# run commands in the container rather than the host device
# this prevenets attacks and priviledge escalation on the server USER backend_container
USER backend_container


# Expose port for api connection (container port)
EXPOSE 5000


#Labels
LABEL version="2.0.0"
LABEL description="neobank backend application Docker image"
LABEL maintainer="Eli"
