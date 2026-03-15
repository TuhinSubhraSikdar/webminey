from django.shortcuts import render
from .handlers.bag_words import extract_bag_of_words


def bag_of_words_view(request):
    context = {}

    if request.method == 'POST':
        url = request.POST.get('url')

        result = extract_bag_of_words(url)

        context = result

    return render(request, 'tools/bag_of_words.html', context)