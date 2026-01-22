from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Add custom metric
metrics.info('app_info', 'Application info', version='1.0.0')

@app.route('/')
def home():
    """Main endpoint"""
    logger.info("Home endpoint accessed")
    return jsonify({
        "message": "Hello DevOps!",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        "status": "healthy",
        "service": "devops-pipeline-app"
    }), 200

@app.route('/ready')
def ready():
    """Readiness probe endpoint for Kubernetes"""
    # Add actual readiness checks here (DB connection, etc.)
    return jsonify({
        "status": "ready",
        "service": "devops-pipeline-app"
    }), 200

@app.route('/info')
def info():
    """Application information endpoint"""
    return jsonify({
        "app_name": "DevOps Full Pipeline",
        "version": "1.0.0",
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "python_version": "3.11"
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({
        "error": "Internal server error",
        "status": 500
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)