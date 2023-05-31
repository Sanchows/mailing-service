# mailing-service

## Stack
Python3.10, Django Rest Framework, PostgreSQL, Celery, Redis, Prometheus, Grafana.

## Additional features
Numbers: 3, 5, 6(django admin), 10(partially)

## Getting started

Clone this repository and enter into root directory. Run the following command:
```
docker-compose up
```
This should create and run docker containers such as:
1. Web application (http://127.0.0.1:8000)
2. Redis
3. PostgreSQL
4. Celery worker
5. Celery flower (http://127.0.0.1:5555)
6. Prometheus (http://127.0.0.1:9090)
7. Grafana (http://127.0.0.1:3000)

## How to use
1. To access the Admin panel, you need create a superuser. Open terminal and enter to the root directory of project. Then:
```
docker exec -it mailing-service_webapp_1 sh
./manage.py createsuperuser
```
2. You can see on the API documentation http://127.0.0.1:8000/swagger/
3. Before creating a client or a maling, you need to create some tags and mobile operator's codes by using the Admin panel http://127.0.0.1:8000/admin
4. Then, try to use an API through Swagger.

## Features
- Tasks monitoring (Celery flower http://127.0.0.1:5555)
- Prometheus (http://127.0.0.1:9090)
- Grafana (http://127.0.0.1:3000)
