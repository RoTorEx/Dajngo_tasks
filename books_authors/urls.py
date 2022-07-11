from django.urls import path

from books_authors.views import index


urlpatterns = [
    path("", index, name="home")
]
