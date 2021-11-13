# api_yamdb
### Описание
Проект для организации базы данных с отзывами на различные произведения искуства через api на основе RestAPI.
### Технологии
Python\
Django\
Django REST framework
### Запуск проекта в dev-режиме
- Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```
- Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Выполнить миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```

### Примеры запросов
- Получение списка всех произведений
```
http://localhost:8000/api/v1/titles/
```
- Получение списка всех жанров
```
http://localhost:8000/api/v1/genres/
```
- Получение списка всех категорий
```
http://localhost:8000/api/v1/categories/
```
- Получение списка всех отзывов на произведение
```
http://localhost:8000/api/v1/titles/{title_id}/reviews/
```
- Вся Информация
```
http://localhost:8000/redoc/
```
### Авторы
- [Иван](https://github.com/AkuLinker/ "GitHub аккаунт")
- [Роман](https://github.com/Rased1983/ "GitHub аккаунт")
