import unittest
import unittest.mock
import micro_logger_unittest
import relations.unittest

import json

import service
import {{ code }}

{% if 'redis' in microservices %}class MockRedis:

    host = None
    queue = None

    def __init__(self, host, **kwargs):

        self.host = host
        self.queue = {}

    def xadd(self, stream, fields):

        self.queue.setdefault(stream, [])
        self.queue[stream].append({"fields": fields}){% endif %}

class TestCron(micro_logger_unittest.TestCase):

    maxDiff = None

    @unittest.mock.patch("micro_logger.getLogger", micro_logger_unittest.MockLogger)
    @unittest.mock.patch('relations_restx.Source', relations.unittest.MockSource)
{% if 'redis' in microservices %}    @unittest.mock.patch('redis.Redis', MockRedis)
{% endif %}    def setUp(self):

        self.cron = service.Cron()

    @unittest.mock.patch.dict('os.environ', {"LOG_LEVEL": "INFO"})
    @unittest.mock.patch("micro_logger.getLogger", micro_logger_unittest.MockLogger)
    @unittest.mock.patch('relations_restx.Source', relations.unittest.MockSource)
{% if 'redis' in microservices %}    @unittest.mock.patch('redis.Redis', MockRedis)
{% endif %}    def test___init__(self):

        cron = service.Cron()

        self.assertEqual(cron.logger.name, "{{ service }}-{{ cron }}")

        self.assertIsInstance(relations.source("{{ service }}"), relations.unittest.MockSource)
{% if 'redis' in microservices %}
        self.assertEqual(cron.redis.host, "{{ redis }}.{{ service }}"){% endif %}

    def test_process(self):

        person = {{ code }}.Person("Tom").create()

        self.cron.process()

        self.assertLogged(self.cron.logger, "info", "person", extra={"person": person.export()})
{% if 'redis' in microservices %}
        self.assertEqual(len(self.cron.redis.queue['{{ service }}/person']), 1)
        self.assertEqual(json.loads(self.cron.redis.queue['{{ service }}/person'][0]["fields"]["person"]), person.export()){% endif %}

    @unittest.mock.patch('prometheus_client.push_to_gateway')
    def test_run(self, mock_push):

        self.cron.run()

        mock_push.assert_called_once_with("push.prometheus:9091", "{{ service }}/cron", registry=service.REGISTRY)
