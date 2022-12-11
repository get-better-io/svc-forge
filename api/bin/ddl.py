#!/usr/bin/env python

import relations
import relations_pymysql

import {{ code }}

source = relations_pymysql.Source("{{ service }}", schema="{{ code }}", connection=False)

migrations = relations.Migrations()

migrations.generate(relations.models({{ code }}, {{ code }}.Base))
migrations.convert("{{ service }}")
