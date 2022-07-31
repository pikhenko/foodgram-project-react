# praktikum_new_diplom
docker-compose exec backend python manage.py makemigrations

docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py add_igridiensts_db

docker-compose exec backend python manage.py add_tags_db

docker-compose exec backend python manage.py createsuperuser

docker-compose exec backend python manage.py collectstatic --noinput

a