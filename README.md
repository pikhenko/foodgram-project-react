# Сайт "Продуктовый помощник Foodgram"
На этом сайте пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Ресурсы Foodgram



## Установка
1. Склонируйте репозиторий:
    ```
    git clone git@github.com:pikhenko/foodgram-project-react.git
    ```


2. Находясь в папке с кодом создайте виртуальное окружение:
    ```
    cd foodgram-project-react
    ```
    ```
    python -m venv env
    ```
3. Активируйте виртуальное акружение  
    * Для Windows:
        ```
        source venv\scripts\activate
        ```
    * Для Linux/Mac:
        ```
        sorce venv/bin/activate
        ```
4. Установите зависимости:
    ```
    cd backend/
    ```
    ```
    python -m pip install -r requirements.txt
    ```


## Action workflow:
В проекте Foodgram при пуше в ветку main код автоматически деплоится на сервер http://51.250.31.101/



![example workflow](https://github.com/pikhenko/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)





docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py add_igridiensts_db
docker-compose exec backend python manage.py add_tags_db
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --noinput

a