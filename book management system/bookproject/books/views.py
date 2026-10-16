
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book


# READ: Display all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {
        'books': books
    })


# CREATE: Add a new book
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        price = request.POST.get('price', '').strip()

        if title and author and price:
            try:
                price_value = int(price)
                if price_value < 0:
                    raise ValueError

                Book.objects.create(
                    title=title,
                    author=author,
                    price=price_value
                )
                return redirect('book_list')
            except ValueError:
                error = 'Enter a valid non-negative integer price.'
                return render(request, 'books/add_book.html', {
                    'error': error
                })

        return render(request, 'books/add_book.html', {
            'error': 'Please fill in all fields.'
        })

    return render(request, 'books/add_book.html')


# UPDATE: Modify a book's price
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        price = request.POST.get('price', '').strip()

        try:
            price_value = int(price)
            if price_value < 0:
                raise ValueError

            book.price = price_value
            book.save()
            return redirect('book_list')
        except ValueError:
            return render(request, 'books/update_book.html', {
                'book': book,
                'error': 'Enter a valid non-negative integer price.'
            })

    return render(request, 'books/update_book.html', {
        'book': book
    })


# DELETE: Remove a book
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()

    return redirect('book_list')
