from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance

# Register your models here.

# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)

# Book Inline


class BookInline(admin.StackedInline):
    model = Book
    extra = 0
    # Book.display_genre
    fields = ('isbn', 'title', 'summary')
    # list_display = ('title', 'author', 'display_genre')


# Define the admin class


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')

    # fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# BookInstance Inline
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    fields = ('book', 'status', 'due_back', 'id')


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]
# Register the Admin classes for BookInstance using the decorator


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )
