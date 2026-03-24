# Prometheus & Grafana Monitoring Stack

This repository contains an implementation for a monitoring stack comprising Prometheus, Alertmanager, and an instrumented Python Flask application.

## Directory Structure

- `alertmanager/`: Configuration for Alertmanager routing and notification receivers.
- `prometheus/rules/`: Alerting rules for infrastructure and databases.
- `flask-app/`: A sample web service instrumented with custom Prometheus metrics.

## Components

### 1. Flask Application
Located in `flask-app/app.py`.

This application uses the `prometheus_client` library to expose metrics at `/metrics`.

**Custom Metrics:**
*   `myapp_http_requests_total` (Counter): Request count labeled by method, endpoint, and status.
*   `myapp_http_request_duration_seconds` (Histogram): Request latency buckets.
*   `myapp_orders_total` (Counter): Business logic metric tracking order success/failure.
*   `myapp_active_users` (Gauge): Tracks concurrent users.

**Running the App:**
```bash
pip install flask prometheus-client
python flask-app/app.py
```

### 2. Alerting Rules
Located in `prometheus/rules/alerts.yml`.

Defines three groups of alerts:
1.  **Infrastructure**: Node down, High CPU (>85%), High Memory (>90%), Low Disk Space (<15%).
2.  **Redis**: High Memory (>90%), Instance Down.
3.  **Postgres**: High Connection Usage (>80%).

### 3. Alertmanager Configuration
Located in `alertmanager/alertmanager.yml`.

Handles notification routing based on severity:
*   **Critical Alerts**: Routed to `#alerts-critical` via Slack. Notifies immediately and repeats every hour.
*   **Default/Warning**: Routed to `#alerts` via Slack. Repeats every 4 hours.

**Key Features:**
*   **Grouping**: Alerts are grouped by `alertname` and `instance`.
*   **Inhibition**: Warning alerts are suppressed if a Critical alert is already firing for the same instance.

**Configuration Note:**
You must replace the placeholder URL in `alertmanager.yml` with your actual Slack Webhook URL:
`https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK`

“AWS / Cloud Deployment Ready”

While this stack currently runs locally via Docker Compose, it can be deployed in AWS using ECS/Fargate. Environment variables, volumes, and networking are parameterized for cloud deployment. Prometheus, Grafana, and Alertmanager can be integrated with CloudWatch logs, and the stack can scale horizontally across multiple services.