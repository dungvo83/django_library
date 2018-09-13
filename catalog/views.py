from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre

from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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

    # number of visits in this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    template_name = 'catalog/book_list.html'
    context_object_name = 'book_list'

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

    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'

    def book_detail_view(request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            print('>>> book:', book)
        except Book.DoesNotExist:
            raise Http404('Book does not exist...')
        return render(request, template_name, context={'book': book})

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
    paginate_by = 5

    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'
    context_object_name = 'author'

    def author_detail_view(request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404('Author does not exist...')
        return render(request, template_name, context={'author': author})


class LoanBookByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanBookByAllListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to all customer."""
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinstance_list_borrowed_all.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            # option1
            #book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            # option2
            book_instance.due_back = book_renewal_form.cleaned_data['due_back']

            book_instance.save()

            # redirect to a new URL:
            url1 = reverse('all-borrowed')
            url2 = reverse_lazy('all-borrowed')
            print("url1 >>", type(url1), url1)
            print("url2 >>", type(url2), url2)

            # return HttpResponseRedirect(reverse('all-borrowed'))
            return HttpResponseRedirect(reverse_lazy('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # option1
        # book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        # option2

        book_renewal_form = RenewBookForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

#
# Model Author: create, update, delete
#


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_birth': '05/01/2018'}
    permission_required = 'catalog.author_all'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.author_all'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.author_all'


#
# Model Book: create, update, delete
#


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    initial = {}
    permission_required = 'catalog.book_all'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.book_all'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.book_all'


def test(request, id):
    print('->>>> value:', id)

    return render(request, 'catalog/author_detail.html', context={'data': id})
