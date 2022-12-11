"""
Module for the Daemon
"""

# pylint: disable=no-self-use

import os
import micro_logger
{% if 'redis' in microservices %}import json
import redis
{% else %}import time

import {{ code }}
{% endif %}
import relations_rest

import prometheus_client

PROCESS = prometheus_client.Gauge("process_seconds", "Time to complete a processing task")
PERSONS = prometheus_client.Summary("persons_processed", "Persons processed")

class Daemon: # pylint: disable=too-few-public-methods
    """
    Daemon class
    """

    def __init__(self):

        self.name = os.environ["K8S_POD"]

        self.sleep = int(os.environ.get("SLEEP", 5))

        self.logger = micro_logger.getLogger("{{ service }}-{{ daemon }}")

        self.source = relations_rest.Source("{{ service }}", url="http://{{ api }}.{{ service }}"){% if 'redis' in microservices %}

        self.redis = redis.Redis(host='{{ redis }}.{{ service }}', encoding="utf-8", decode_responses=True)

        if (
            not self.redis.exists("{{ service }}/person") or
            "daemon" not in [group["name"] for group in self.redis.xinfo_groups("{{ service }}/person")]
        ):
            self.redis.xgroup_create("{{ service }}/person", "daemon", mkstream=True){% endif %}

    @PROCESS.time()
    def process(self):
        """
        Reads people off the queue and logs them
        """
{% if 'redis' in microservices %}
        message = self.redis.xreadgroup("daemon", self.name, {"{{ service }}/person": ">"}, count=1, block=1000*self.sleep)

        if not message or "person" not in message[0][1][0][1]:
            return

        person = json.loads(message[0][1][0][1]["person"])
        self.logger.info("person", extra={"person": person})
        PERSONS.observe(1)
        self.redis.xack("{{ service }}/person", "daemon", message[0][1][0][0]){% else %}
        for person in {{ code }}.Person.many():
            self.logger.info("person", extra={"person": person.export()})
            PERSONS.observe(1){% endif %}

    def run(self):
        """
        Main loop with sleep
        """

        prometheus_client.start_http_server(80)

        while True:
            self.process(){% if 'redis' not in microservices %}
            time.sleep(self.sleep){% endif %}
