# Django tasks


## Django ORM
```python
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_day = models.DateTimeField()


class Publisher(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    publish_date = models.DateTimeField()
    price = models.FloatField()


class Sales(models.Model):
    date = models.DateTimeField()
    total_sold_usd = models.FloatField()
```
1. Посчитать количесто книг выпущенных после 2000 года
2. Вывести **только** имена авторов для книг которые не содержат букву `А` в своем имени
3. Получить последнюю опубликованную книгу двумя способами. Аналогично с первой опубликованной книгой
4. Посчитать для каждого автора его количество книг
5. Вывести авторов у которых количество книг больше 5, используя метод `alias`
6. Вывести по одному имени книги для каждого года
7. Одним запросом получить для книг имена паблишеров, не подгружая остальные поля из связанной модели
8. В один запрос для автора выбрать список всех книг исключая их цену
9. С помощью Django ORM написать сырой SQL запрос для получения всех объектов автора
10. Проверить существует ли книга с `id`=100
11. Получить паблишеров у авторов книг которых день рождения в 16 или 18 веке
12. Создать если не существует книга с именем `Эйафьядлаёкюдель`
13. Создать 5 книг одном запросом
14. Получить год рождения самого древнего автора
15. Найти самое богатое издания по общей стоимости книг
16. Показать список книг цена которых больше цены продаж за 20 февраля 2002 года

## Description

Enter *pipenv shel* and then *./fill_db* to make migrations, generate random fixtures in json format, load data into database and finally run server.

Also don't forget to create a superuser: *python manage.py createsuperuser*.
