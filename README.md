# Devops - Node.js Project with MongoDB and Mongo Express

This is a simple Node.js application that demonstrates building and running an app using Docker Compose alongside MongoDB and Mongo Express, with support for deploying the app to **AWS ECR** and **EC2**.

---

## Features

* Node.js application (`my-app`)
* MongoDB database
* Mongo Express web interface for MongoDB
* Fully containerized setup with Docker Compose
* CI/CD pipeline for ECR and EC2 deployments

---

## Prerequisites

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)
* AWS account with:

  * ECR repository
  * IAM user with push/pull permissions
* SSH access to the EC2 instance

---

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

2. Create a `.env` file to store your secrets:

```bash
MONGO_USERNAME=your-mongo-username
MONGO_PASSWORD=your-mongo-password
DB_PASSWORD=your-app-db-password
```

---

## Running Locally

Use Docker Compose to build and run all services:

```bash
docker compose --env-file .env up --build
```

* `my-app` will be built from the local Dockerfile.
* `mongodb` and `mongo-express` images will be pulled from Docker Hub.

Access services:

* Node.js app: [http://localhost:3000](http://localhost:3000)
* Mongo Express: [http://localhost:8081](http://localhost:8081)
* MongoDB runs internally on port 27017.

Stop services:

```bash
docker compose down
```

---

## Deployment to AWS ECR

1. Build the Docker image and tag it with the ECR repository URI:

```bash
docker build -t my-app:latest ./app
docker tag my-app:latest <AWS_ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/my-app:latest
```

2. Login to ECR:

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com
```

3. Push the image:

```bash
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/my-app:latest
```

> **Tip:** For CI/CD, use GitHub Actions with secrets for AWS credentials and dynamic image tagging.

---

## Deployment to EC2 via SSH

1. SSH into your EC2 instance:

```bash
ssh -i <key.pem> ec2-user@<EC2_PUBLIC_IP>
```

2. Pull the latest image from ECR:

```bash
docker login -u AWS -p $(aws ecr get-login-password --region <region>) <AWS_ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com
docker pull <AWS_ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/my-app:latest
```

3. Update `docker-compose.yml` on EC2 to reference the ECR image:

```yaml
my-app:
  image: <AWS_ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/my-app:latest
  ports:
    - 3000:3000
  environment:
    DB_PASSWORD: ${DB_PASSWORD}
```

4. Run Docker Compose:

```bash
export DB_PASSWORD=<your-app-db-password>
docker compose up -d
```

* MongoDB and Mongo Express can either be local on EC2 or connected via your existing Docker Compose setup.

5. To update the app later:

```bash
docker compose pull
docker compose up -d
```

---

## Notes

* **Secrets**: Never commit `.env` files with passwords. Use GitHub Secrets for CI/CD.
* **Dynamic versioning**: Use image tags like `1.0.${GITHUB_RUN_NUMBER}` for unique builds.
* **CI/CD**: Your GitHub Actions workflow can automate build, push to ECR, and trigger deployment on EC2 via SSH.

---

This README now covers **local development**, **ECR deployment**, and **EC2 deployment**, making it ready for both dev and production workflows.
