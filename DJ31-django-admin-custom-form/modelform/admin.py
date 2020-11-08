from django.contrib import admin

# Register your models here.
from .models import Author, Book
from .forms import AuthorForm, BookForm


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorForm  # 覆写form


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookForm  # 覆写form
