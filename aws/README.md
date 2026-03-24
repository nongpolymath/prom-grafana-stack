# AWS Cloud Deployment

This directory contains the configuration and instructions for deploying the Prometheus & Grafana monitoring stack on Amazon Web Services (AWS), specifically using an EC2 instance.

## Prerequisites

1.  **AWS Account**: Access to the AWS Console or CLI.
2.  **Terraform**: Installed locally (optional, for infrastructure provisioning).
3.  **SSH Key Pair**: Created in AWS to access the EC2 instance.

## Deployment Steps

### 1. Provision Infrastructure (Terraform)

Navigate to the `terraform/` directory and run the following to create an EC2 instance with the necessary security group rules.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

*Note: Check `main.tf` and update `ami` IDs or `region` variables as needed for your location.*

### 2. Prepare the Instance

SSH into your new instance:

```bash
ssh -i /path/to/key.pem ubuntu@<EC2-PUBLIC-IP>
```

Install Docker and Docker Compose:

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
# Log out and log back in for group changes to take effect
```

### 3. Deploy the Stack

Clone this repository (or copy the files) to the instance. Navigate to the `aws/` directory and run the specific AWS compose file.

**Important**: The `docker-compose.aws.yml` file is configured with relative paths (`../`) to access the configuration files in the parent directories.

```bash
cd prom-grafana-stack/aws
docker-compose -f docker-compose.aws.yml up -d
```

### 4. Access Services

Ensure your Security Group allows traffic on the following ports:
-   **Grafana**: `http://<EC2-PUBLIC-IP>:3000` (Login: `admin`/`admin`)
-   **Prometheus**: `http://<EC2-PUBLIC-IP>:9090`
-   **Flask App**: `http://<EC2-PUBLIC-IP>:5000`

## Security Note
The provided Terraform and Docker configurations expose ports publicly for demonstration purposes. For a production environment, restrict access to your IP address or use an SSH tunnel / VPN.