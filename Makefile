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
	docker-compose exec postgres psql -U app
restart:
	docker-compose restart web nginx
build:
	docker-compose build
rebuild:
	docker-compose build --no-cache web
wipe: stop
	docker-compose exec postgres psql -U app -d postgres -c 'DROP DATABASE app;'
	docker-compose exec postgres psql -U app -d postgres -c 'CREATE DATABASE app;'
	$(MAKE) restart
	docker-compose exec web python manage.py migrate
reload: wipe
	docker-compose exec web python manage.py loaddata /vol/data/json/app.json
dumptest:
	docker-compose exec web python manage.py dumpdata --indent 2 -e admin.logentry -e auth.permission -e contenttypes -e sessions -o abstracts/fixtures/test.json
loadtest: wipe
	docker-compose exec web python manage.py loaddata abstracts/fixtures/test.json
test:
	docker-compose exec web python manage.py test --parallel 4
coverage:
	-docker-compose exec web coverage run manage.py test
	docker-compose exec web coverage html
