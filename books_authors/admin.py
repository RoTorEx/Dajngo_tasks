from django.contrib import admin

from books_authors.models import Author, Publisher, Book, Sales

models = (Author, Publisher, Book, Sales)

for m in models:
    admin.site.register(m)
