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
        self.groups = {}
        self.read = {}
        self.ack = {}

    def exists(self, stream):

        return stream in self.queue

    def xinfo_groups(self, stream):

        return self.groups[stream]

    def xgroup_create(self, stream, name, mkstream=False):

        self.groups[stream] = {
            "name": name
        }

        if mkstream:
            self.queue[stream] = []

    def xreadgroup(self, group, consumer, streams, count=0, block=5000):

        self.read = {
            "group": group,
            "consumer": consumer,
            "streams": streams,
            "count": count,
            "block": block
        }

        stream = list(streams.keys())[0]

        return [
            [
                stream,
                [
                    [
                        "id",
                        self.queue[stream].pop(0)
                    ]
                ]
            ]
        ]

    def xack(self, stream, group, id):

        self.ack = {
            "stream": stream,
            "group": group,
            "id": id
        }
{% endif %}

class TestDaemon(micro_logger_unittest.TestCase):

    maxDiff = None

    @unittest.mock.patch.dict('os.environ', {"K8S_POD": "unit", "SLEEP": "7", "LOG_LEVEL": "INFO"})
    @unittest.mock.patch("micro_logger.getLogger", micro_logger_unittest.MockLogger)
    @unittest.mock.patch('relations_restx.Source', relations.unittest.MockSource)
{% if 'redis' in microservices %}    @unittest.mock.patch('redis.Redis', MockRedis)
{% endif %}    def setUp(self):

        self.daemon = service.Daemon()

    @unittest.mock.patch.dict('os.environ', {"K8S_POD": "test", "SLEEP": "7", "LOG_LEVEL": "INFO"})
    @unittest.mock.patch("micro_logger.getLogger", micro_logger_unittest.MockLogger)
    @unittest.mock.patch('relations_restx.Source', relations.unittest.MockSource)
{% if 'redis' in microservices %}    @unittest.mock.patch('redis.Redis', MockRedis)
{% endif %}    def test___init__(self):

        daemon = service.Daemon()

        self.assertEqual(daemon.name, "test")

        self.assertEqual(daemon.sleep, 7)

        self.assertEqual(daemon.logger.name, "{{ service }}-{{ daemon }}")

        self.assertIsInstance(relations.source("{{ service }}"), relations.unittest.MockSource)
{% if 'redis' in microservices %}
        self.assertEqual(daemon.redis.host, "{{ redis }}.{{ service }}")
        self.assertEqual(daemon.redis.queue["{{ service }}/person"], []){% endif %}{% if 'redis' in microservices %}

    def test_process(self):

        self.daemon.redis.queue["{{ service }}/person"].append({})

        self.daemon.process()

        person = {{ code }}.Person("Tom").create()
        self.daemon.redis.queue["{{ service }}/person"].append({"person": json.dumps(person.export())})

        self.daemon.process()
        self.assertLogged(self.daemon.logger, "info", "person", extra={"person": person.export()})

    @unittest.mock.patch('prometheus_client.start_http_server')
    def test_run(self, mock_prom):

        self.daemon.process = unittest.mock.MagicMock(side_effect=Exception("loop"))

        self.assertRaisesRegex(Exception, "loop", self.daemon.run)

        mock_prom.assert_called_once_with(80){% else %}
    def test_process(self):

        person = {{ code }}.Person("Tom").create()

        self.daemon.process()

        self.assertLogged(self.daemon.logger, "info", "person", extra={"person": person.export()})

    @unittest.mock.patch('prometheus_client.start_http_server')
    @unittest.mock.patch('time.sleep')
    def test_run(self, mock_sleep, mock_prom):

        mock_sleep.side_effect = Exception("loop")

        self.assertRaisesRegex(Exception, "loop", self.daemon.run)

        mock_prom.assert_called_once_with(80)
{% endif %}
