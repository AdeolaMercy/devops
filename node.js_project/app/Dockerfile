#start with the base image. This is a node.js application
#We need node installed
FROM node:13-alpine

#Set environment variables
ENV MONGO_DB_USERNAME=admin \
    MONGO_DB_PASSWORD=password1

#run command to create directory in the container
RUN mkdir -p /home/app

#copy all the files in /app in the repo to /home/app in the container
COPY /app /home/app

#run this command as the entrypoint for docker
CMD['node',"/home/app/server.js"]