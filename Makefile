all:
	docker-compose up
detached:
	docker-compose up -d
stop:
	docker-compose stop web
down:
	docker-compose down
attach:
	docker-compose exec web bash
db:
	docker-compose exec postgres psql -U app -d pp
restart:
	docker-compose restart web nginx
check:
	docker-compose exec web python manage.py check
shell:
	docker-compose exec web python manage.py shell
build:
	docker-compose build
rebuild:
	docker-compose build --no-cache web
blank: stop
	docker-compose exec postgres psql -U app -d postgres -c 'DROP DATABASE pp;'
wipe: blank
	docker-compose exec postgres psql -U app -d postgres -c 'CREATE DATABASE pp;'
	$(MAKE) restart
	docker-compose exec web python manage.py migrate
dbonly:
	docker-compose exec postgres pg_dump -U app pp > ../bkp/dbonly.sql
restoredbonly: blank
	docker-compose up -d postgres
	docker-compose exec -T postgres psql -U app -d postgres -c 'CREATE DATABASE pp;'
	docker-compose exec -T postgres psql -U app pp < ../bkp/dbonly.sql
	$(MAKE) restart
backup:
	docker-compose exec -T postgres pg_dumpall -U app > ../bkp/bkp.sql
restore: blank
	docker-compose up -d postgres
	docker-compose exec -T postgres psql -U app -d postgres < ../bkp/bkp.sql
	$(MAKE) restart
dumptest:
	docker-compose exec web python manage.py dumpdata --indent 2 -e auth.permission -e contenttypes -e sessions -e silk -o pp/fixtures/test.json
loadtest: wipe
	docker-compose exec web python manage.py loaddata pp/fixtures/test.json
test:
	docker-compose exec web python manage.py test
coverage:
	-docker-compose exec web coverage run manage.py test
	docker-compose exec web coverage html
	open app/htmlcov/index.html
dumpusers:
	docker-compose exec web python manage.py dumpdata --indent 2 auth authtoken -e auth.permission -o users.json
restoreusers:
	docker-compose exec web python manage.py loaddata users.json
