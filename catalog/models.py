

from django.db import models
#
from django.contrib.auth.models import User

# Used to generate URLs by reversing the URL patterns
from django.urls import reverse


# Required for unique book instances
import uuid


#
from datetime import date


# Create your models here.

class Genre(models.Model):

    # Field
    """Model representing a book gener."""
    name = models.CharField(
        max_length=200, help_text='Enter the book genre (e.g. Science Fiction.)')

    # Method
    def __str__(self):
        """String for a representing the Model object."""
        return self.name


class Book(models.Model):
    # objects = models.Manager()

    # Field
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(
        max_length=1000, help_text='Enter the brief description of the book.')
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Charactor <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book.')

    # class Meta

    class Meta:
        permissions = (("book_all", "set_book_all"),)

    # Method

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
        # return reverse('book-detail', kwargs={'pk': str(self.id)})

    # def get_absolute_url(self):
    #    """Return the url to access a detail for this book."""
    #    # print(">>>>>", reverse('book-detail', args=[str(self.id)]))
    #    return reverse('model-detail-view', args=[str(self.id)])
    #    return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        # display top 3 genre
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    # Field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library.')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    # Metadata

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "set_book_as_returned"),
                       ("can_show_borrowed_all", "set_show_borrowed_all"),)

    # Method

    def __str__(self):
        """String for representing the Model of object."""
        return f'{self.id} ({self.book.title})'
        #- {self.status} - {self.get_status_display()}

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True

        return False


class Author(models.Model):
    """Model representing an author."""
    #objects = models.Manager

    # Field
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank='True')

    # Metadata
    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("author_all", "set_author_all"),)

    # Method
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
        # return reverse('author-detail', kwargs={'key': str(self.id)})

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
