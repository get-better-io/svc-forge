import unittest
import unittest.mock

import relations.unittest
import micro_logger_unittest


import service


class TestRestful(relations.unittest.TestCase):

    maxDiff = None

    @unittest.mock.patch("micro_logger.getLogger", micro_logger_unittest.MockLogger)
    def setUp(self):

        self.app = service.build()
        self.api = self.app.test_client()

class TestApi(TestRestful, micro_logger_unittest.TestCase):

    def test_build(self):

        app = service.build(False)

        self.assertEqual(app.name, "{{ craft }}-{{ api }}")
        self.assertEqual(app.logger.name, "{{ craft }}-{{ api }}")

        self.assertLogged(self.app.logger, "debug", "init")

class TestHealth(TestRestful):

    def test_get(self):

        self.assertStatusValue(self.api.get("/health"), 200, "message", "OK")
