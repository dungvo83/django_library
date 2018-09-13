from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre

from django.views import generic
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available book (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.all().count()

    # count genre
    num_genres = Book.objects.values('genre').distinct().count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    template_name = 'catalog/book_list_alibaba.html'
    context_object_name = 'my_book_list'

    # context_object_name = 'my_book_list'  # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='wars')[:5]  # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    def get_queryset(self):

        # return Book.objects.filter(title__icontains='wars')[:5]  # Get 5 books containing the title war

        return Book.objects.all()

    # def get_context_data(self, **kwargs):
    #    # Call the base implementation first to get the context
    #    context = super(BookListView, self)

    #    # Create any data and add it to context
    #    context['some_data'] = 'This is just some data'

    #    return context


class BookDetailView(generic.DetailView):
    model = Book

    template_name = 'catalog/book_detail_alibaba.html'
    context_object_name = 'book_detail'

    # def book_detail_view(request, primary_key):
    #    try:
    #        book = Book.objects.get(pk=primary_key)
    #        print('>>> book:', book)
    #    except Book.DoesNotExist:
    #        raise Http404('Book does not exist...')
    #    return render(request, 'catalog/book_detail.html', context={'book': book})

    # def book_detail_view(request, primary_key):
    # try:
    #    book = Book.objects.get(pk=primary_key)
    # except Book.DoesNotExist:
    #    raise Http404('Book does not exist.')

    #    return render(request, 'catalog/book_detail.html', context={'book': book})

    # def book_detail_view(request, primary_key):
    #    book = get_object_or_404(Book, pk=primary_key)
    #    return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author

    # def author_detail_view(request, pk):
    #    return render(request, 'catalog/author_detail.html', context={'author': '123'})

    # def author_detail_view(request, primary_key):

    #    #lookup_url_kwargs = "key"

    #    author = get_object_or_404(
    #        Author, pk=primary_key
    #    )

    #author = get_object_or_404(Author, id=primary_key)
    #    return render(request, 'catalog/author_detail.html', context={'author': author})


def test(request, id):
    print('->>>> value:', id)

    return render(request, 'catalog/author_detail.html', context={'data': id})
