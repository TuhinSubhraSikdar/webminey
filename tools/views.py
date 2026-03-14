from django.shortcuts import render

def bag_of_words(request):
    return render(request, 'tools/bag_of_words.html')
