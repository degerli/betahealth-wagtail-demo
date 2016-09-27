Start
-----

1. `$ docker-compose build`
2. `$ docker-compose up`
3. In another terminal session:
    - Run DB migrations: `$ docker-compose run wagtail python manage.py migrate`
    - Create superuser: `$ docker-compose run wagtail python manage.py createsuperuser`
4. Visit [http://localhost:8000/]()
