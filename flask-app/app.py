from flask import Flask, jsonify, request
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST,
    CollectorRegistry, multiprocess
)
import time

app = Flask(__name__)

# 1. Define metrics
http_requests_total = Counter(
    'myapp_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_duration_seconds = Histogram(
    'myapp_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5]
)

active_users = Gauge(
    'myapp_active_users',
    'Currently active users'
)
orders_total = Counter(
    'myapp_orders_total',
    'Total orders',
    ['status']  # 'success' | 'failed'
)

# 2. Middleware — time every request
@app.before_request
def start_timer():
    request._start_time = time.time()

@app.after_request
def record_metrics(response):
    duration = time.time() - request._start_time
    http_requests_total.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    http_duration_seconds.labels(
        method=request.method,
        endpoint=request.path
    ).observe(duration)
    return response

# 3. /metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# 4. app's actual routes
@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        # ... ordering an item logic ...
        orders_total.labels(status='success').inc()
        return jsonify({'ok': True})
    except Exception as e:
        orders_total.labels(status='failed').inc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)