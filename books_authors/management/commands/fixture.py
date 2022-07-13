import os
import json
import random as r

from faker import Faker

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Expanding the functionality of the basic app commands.'''

    def handle(self, *args, **options):
        dir = os.path.abspath(os.curdir)
        fixtures_dir = dir + "/books_authors/fixtures"

        # Author
        with open(f"{fixtures_dir}/author.json", "w") as file:
            data_list = []

            for i in range(20):
                date = f"{r.randint(1700, 2000)}-{r.randint(1, 12)}-{r.randint(1,28)}"
                time = f"{r.randint(1,12)}:{r.randint(0,59)}:{r.randint(0,59)}+00:00"

                data_dir = {
                    "model": "books_authors.Author",
                    "pk": i + 1,
                    "fields": {
                        "name": Faker().name(),
                        "birth_day": date + " " + time
                    }
                }

                data_list.append(data_dir)
            json.dump(data_list, file, indent=4, ensure_ascii=False)

        # Publisher
        with open(f"{fixtures_dir}/publisher.json", "w") as file:
            data_list = []

            for i in range(8):
                data_dir = {
                    "model": "books_authors.Publisher",
                    "pk": i + 1,
                    "fields": {
                        "name": Faker().company(),
                    }
                }

                data_list.append(data_dir)
            json.dump(data_list, file, indent=4)

        # Books
        with open(f"{fixtures_dir}/books.json", "w") as file:
            data_list = []

            for i in range(80):
                date = f"{r.randint(1900, 2020)}-{r.randint(1, 12)}-{r.randint(1,28)}"
                time = f"{r.randint(1,12)}:{r.randint(0,59)}:{r.randint(0,59)}+00:00"

                data_dir = {
                    "model": "books_authors.Book",
                    "pk": i + 1,
                    "fields": {
                        "name": " ".join([Faker().word() for i in range(r.randint(1, 5))]).capitalize(),
                        "authors": [r.randint(1, 20) for i in range(r.randint(1, 3))],
                        "publisher": r.randint(1, 8),
                        "publish_date": date + " " + time,
                        "price": float(f"{r.triangular(1234):.2f}")
                    }
                }

                data_list.append(data_dir)
            json.dump(data_list, file, indent=4)

        # Sales
        with open(f"{fixtures_dir}/sales.json", "w") as file:
            data_list = []

            for i in range(15):
                date = f"{r.randint(2010, 2022)}-{r.randint(1, 12)}-{r.randint(1,28)}"
                time = f"{r.randint(1,12)}:{r.randint(0,59)}:{r.randint(0,59)}+00:00"

                data_dir = {
                    "model": "books_authors.Sales",
                    "pk": i + 1,
                    "fields": {
                        "date": date + " " + time,
                        "total_sold_usd": float(f"{r.triangular(500):.2f}")
                    }
                }

                data_list.append(data_dir)
            json.dump(data_list, file, indent=4)
