# official python image as parent image
FROM python:3.11-slim

# working directory
WORKDIR /app

#copy files into"/app" container
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# create a new group 
RUN groupadd -r devgroup

# create a new user and add it to the new group
RUN useradd -r -g devgroup backend_container

# change ownership of the files in /app to be owned by backend_container in the "devgroup" group
RUN chown -R backend_container:devgroup /app 


# run commands in the container rather than the host device
# this prevenets attacks and priviledge escalation on the server
USER backend_container


# Expose port for api connection
# NOTE: I'M NOT TOO CERTAIN WHETHER THIS IS FOR THE CONTAINER PORT OR THE HOST PORT
EXPOSE 8000


#Labels
LABEL version="1.0.0"
LABEL description="Node.js application Docker image"
LABEL maintainer="Eli"
