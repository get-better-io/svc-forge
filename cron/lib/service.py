"""
Module for the Subnet Queue
"""

# pylint: disable=no-self-use

import micro_logger
{% if 'redis' in microservices %}import json
import redis
{% endif %}
import relations_rest

import {{ code }}

import prometheus_client

REGISTRY = prometheus_client.CollectorRegistry()

PROCESS = prometheus_client.Gauge("process_seconds", "Time to complete a processing task", registry=REGISTRY)
PERSONS = prometheus_client.Summary("persons_processed", "Persons processed", registry=REGISTRY)

class Cron: # pylint: disable=too-few-public-methods
    """
    Cron class to run the processing
    """

    def __init__(self):

        self.logger = micro_logger.getLogger("{{ service }}-{{ cron }}")

        self.source = relations_rest.Source("{{ service }}", url="http://{{ api }}.{{ service }}"){% if 'redis' in microservices %}

        self.redis = redis.Redis(host='{{ redis }}.{{ service }}', encoding="utf-8", decode_responses=True){% endif %}

    @PROCESS.time()
    def process(self):
        """
        Loads subnets and pushes onto the queue
        """

        for person in {{ code }}.Person.many():
            self.logger.info("person", extra={"person": person.export()})
            PERSONS.observe(1){% if 'redis' in microservices %}
            self.redis.xadd("{{ service }}/person", fields={"person": json.dumps(person.export())}){% endif %}

    def run(self):
        """
        Runs through s process
        """

        self.process()

        prometheus_client.push_to_gateway("push.prometheus:9091", "{{ service }}/{{ cron }}", registry=REGISTRY)
