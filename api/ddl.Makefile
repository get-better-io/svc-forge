	test -f secret/mysql.json || echo '{"host": "db.mysql", "user": "root", "password": "local"}' > secret/mysql.json
	test -d {{ api }}/ddl || (cd {{ api }}; make build; make ddl;)
