from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Book, Loan
from .forms import BookForm


class StaffRequiredMixin:
    """Mixin that requires user to be a staff member."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'catalogue/book_list.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        return Book.objects.available().select_related('author')


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'catalogue/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_history'] = Loan.objects.filter(
            book=self.object
        ).select_related('member__user').order_by('-date_borrowed')
        return context


class BookCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'catalogue/book_form.html'
    success_url = reverse_lazy('catalogue:book_list')

    def form_valid(self, form):
        form.instance.is_available = True
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'catalogue/book_form.html'
    success_url = reverse_lazy('catalogue:book_list')

    def get_queryset(self):
        return Book.objects.filter(is_available=True)


class BookDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Book
    template_name = 'catalogue/book_confirm_delete.html'
    success_url = reverse_lazy('catalogue:book_list')

    def get_queryset(self):
        return Book.objects.available()
