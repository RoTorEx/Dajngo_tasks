import datetime
import random as r

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Q, Avg
from faker import Faker

from books_authors.models import Author, Publisher, Book, Sales


def index(request):
    # Task_1: Посчитать количесто книг выпущенных после 2000 года
    count_of_books = Book.objects.filter(publish_date__gt=datetime.date(2000, 1, 1)).count()
    print(f"Count of books:\u001b[36m {count_of_books}\u001b[0m.\n")

    # Task_2: Вывести только имена авторов для книг которые не содержат букву "А" в своем имени
    author_names = Book.objects.exclude(name__contains="A").values_list("authors__name", flat=True).distinct()

    for name in author_names:
        print(f"\u001b[37m{name}\u001b[0m", end=" : ")
    print("\n")

    # Task_3: Получить последнюю опубликованную книгу двумя способами. Аналогично с первой опубликованной книгой
    first_way = Book.objects.order_by("publish_date")
    first_old, first_young = first_way.first().name, first_way.last().name
    second_way = Book.objects.order_by("-publish_date")
    second_old, second_young = second_way.reverse()[0].name, second_way[0].name
    print(f"Oldest: '\u001b[33m{first_old}\u001b[0m'. Youngest: '\u001b[33m{first_young}\u001b[0m'.")
    print(f"First method is equivalent to second: {first_old == second_old and first_young == second_young}.\n")

    # Task_4: Посчитать для каждого автора его количество книг
    author_count = Book.objects.values_list("authors__name").annotate(Count("authors"))
    print(f"List of authors count:\u001b[32m {list(author_count)}\u001b[0m.\n")

    # Task_5: Вывести авторов у которых количество книг больше 5, используя метод alias
    author_count_more_5 = Book.objects.values_list("authors__name", flat=True).alias(
        books=Count("authors")).filter(books__gt=5)
    print(f"List of authors which have more then 5 books: \u001b[31m{list(author_count_more_5)}\u001b[0m\.\n")

    # Task_6: Вывести по одному имени книги для каждого года
    books_with_year = Book.objects.values_list("publish_date__year", "name")
    values_dict = {tpl[0]: tpl[1] for tpl in books_with_year}

    for year in sorted([year for year in values_dict.keys()]):
        print(f"Book of\u001b[34m {year}\u001b[0m year is\u001b[31m \"{values_dict[year]}\u001b[0m\"")
    print()

    # Task_7: Одним запросом получить для книг имена паблишеров, не подгружая остальные поля из связанной модели
    publishers_list = Book.objects.select_related("publisher")

    for i in publishers_list:
        print(f"\u001b[33m{i.publisher.name}\u001b[0m", sep=" : ", end="")
    print("\n\n")

    # !Upgrade
    # Task_8: В один запрос для автора выбрать список всех книг исключая их цену
    author = Author.objects.order_by("?").values_list("name", flat=True).first()
    books = list(Book.objects.filter(authors__name=author).values_list('name', flat=True))
    print(f"List of books:\u001b[32m {books}\u001b[0m.\n")

    # Task_9: С помощью Django ORM написать сырой SQL запрос для получения всех объектов автора
    author = r.choice(Author.objects.raw("SELECT * FROM books_authors_author LIMIT 1"))
    print(f"\u001b[35m{author.name}\u001b[0m ==< ~ >==\u001b[35m {author.birth_day.date}\u001b[0m", end="\n\n")

    # Task_10: Проверить существует ли книга с id=100
    print("Book exists!" if Book.objects.filter(id=100).exists() else "\u001b[31mNope :'(\u001b[0m", end="\n\n")

    # Task_11: Получить паблишеров у авторов книг которых день рождения в 16 или 18 веке
    publishers = Book.objects.values_list("publisher__name", flat=True).filter(
        Q(authors__birth_day__year__gt="1500") & Q(authors__birth_day__year__lt="1600") |
        Q(authors__birth_day__year__gt="1700") & Q(authors__birth_day__year__lt="1800"))
    print(f"List of publishers:\u001b[30m {list(publishers)}\u001b[0m", end="\n\n")

    # Task_12: Создать если не существует книга с именем Эйафьядлаёкюдель
    if not Book.objects.filter(name="Эйафьядлаёкюдель").exists():
        date = f"{r.randint(1900, 2020)}-{r.randint(1, 12)}-{r.randint(1, 28)}"
        time = f"{r.randint(1, 12)}:{r.randint(0, 59)}:{r.randint(0, 59)}+00:00"

        book = Book.objects.create(
            name="Эйафьядлаёкюдель",
            publisher=r.choice(Publisher.objects.all()),
            publish_date=date + " " + time,
            price=float(f"{r.triangular(1488, 1488.99):.2f}")
        )
        book.authors.set([r.randint(1, 20) for loop in range(5)])

        print("\"Эйафьядлаёкюдель\"\u001b[34m added to database!\u001b[0m\n")

    else:
        print("\"Эйафьядлаёкюдель\"\u001b[31m already exists! Removing...\u001b[0m\n")
        Book.objects.filter(name="Эйафьядлаёкюдель").delete()

    # Task_13: Создать 5 книг одном запросом
    date = f"{r.randint(1900, 2020)}-{r.randint(1, 12)}-{r.randint(1, 28)}"
    time = f"{r.randint(1, 12)}:{r.randint(0, 59)}:{r.randint(0, 59)}+00:00"

    objs = [
        Book(
            name=Faker().word() + Faker().word(),
            publisher=r.choice(Publisher.objects.all()),
            # authors=[1, 2],  # ? Как тут можно добавить нескольких авторов с использованием метода set()?
            publish_date=date + " " + time,
            price=float(f"{r.triangular(0, 999.99):.2f}")
        )
        for i in range(5)
    ]
    Book.objects.bulk_create(objs=objs)

    print("\u001b[31mAdded 5 new books to DB!\u001b[0m\n")

    # Task_14: Получить год рождения самого древнего автора
    year = Author.objects.order_by("birth_day").values_list("birth_day__year", flat=True).first()
    print(f"The most oldest author was born at\u001b[33m {year}\u001b[0m year.\n")

    # Task_15: Найти самое богатое издания по общей стоимости книг
    expensive_pub = Book.objects.annotate(pub_price=Avg("price")).order_by("-pub_price").values_list("pub_price", "publisher__name").first()
    print(f"\u001b[36m {expensive_pub[1]}\u001b[0m have\u001b[35m {expensive_pub[0]}\u001b[0m$.", end="\n\n")

    # Task_16: Показать список книг цена которых больше цены продаж за 20 февраля 2002 года
    sale_at_feb = Sales.objects.filter(date=datetime.date(2002, 2, 20))
    red_date = datetime.date(2002, 2, 20)
    red_price = float(f"{r.triangular(777, 777.99):.2f}")

    if not sale_at_feb:
        Sales.objects.create(
            date=red_date,
            total_sold_usd=red_price
        )

    books_list = list(Book.objects.filter(price__gt=red_price).values("name", "price").order_by("price"))

    print(f"List of books:\u001b[31m  {books_list}\u001b[0m ")

    return HttpResponse("Hello!")
