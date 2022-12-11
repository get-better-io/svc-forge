#!/usr/bin/env python

import json

import micro_logger

import relations
import relations_pymysql

logger = micro_logger.getLogger("{{ service }}-{{ api }}")

with open("/opt/service/secret/mysql.json", "r") as mysql_file:
    source = relations_pymysql.Source("{{ service }}", schema="{{ code }}", autocommit=True, **json.loads(mysql_file.read()))

cursor = source.connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS `{{ code }}`")

migrations = relations.Migrations()

logger.info("migrations", extra={"migrated": migrations.apply("{{ service }}")})
