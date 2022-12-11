"""
Module for the OPenGUI API
"""

# pylint: disable=no-self-use

import json

import micro_logger

import flask
import flask_restx
import prometheus_flask_exporter
{% if 'redis' in microservices %}import redis
{% endif %}
import relations
import relations_pymysql
import relations_restx

import {{ code }}

metrics = prometheus_flask_exporter.PrometheusMetrics.for_app_factory()

def build():
    """
    Builds the Flask App
    """

    import service # pylint: disable=import-outside-toplevel

    app = flask.Flask("{{ service }}-{{ api }}")

    app.logger = micro_logger.getLogger("{{ service }}-{{ api }}")

    metrics.init_app(app)

    api = flask_restx.Api(app)
{% if 'redis' in microservices %}
    app.redis = redis.Redis(host='{{ redis }}.{{ service }}', encoding="utf-8", decode_responses=True)
{% endif %}
    with open("/opt/service/secret/mysql.json", "r") as mysql_file:
        app.source = relations_pymysql.Source(
            "{{ service }}", schema="{{ code }}", autocommit=True, **json.loads(mysql_file.read())
        )

    def ping():
        app.source.connection.ping(True)

    app.before_request(ping)

    api.add_resource(Health, '/health')

    relations_restx.attach(api, service, relations.models({{ code }}, {{ code }}.Base))

    return app

class Health(flask_restx.Resource):
    """
    Class for Health checks
    """

    def get(self):
        """
        Just return ok
        """
        return {"message": "OK"}
