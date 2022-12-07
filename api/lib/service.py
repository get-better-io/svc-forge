#!/usr/bin/env python

import flask
import flask_restx

import relations
import relations_restx

import micro_logger

import {{ code }}


def build():
    """
    Builds the Flask App
    """

    app = flask.Flask("{{ service }}-{{ api }}")
    api = relations_restx.Api(app)

    app.source = relations.unittest.MockSource("{{ service }}")

    api.add_resource(Health, '/health')

    relations_restx.attach(api, {{ code }}, relations.models({{ code }}, {{ code }}.Base))

    app.logger = micro_logger.getLogger(app.name)

    app.logger.debug("init")

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
