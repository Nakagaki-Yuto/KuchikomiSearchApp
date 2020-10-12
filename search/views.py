from django.shortcuts import render

# Create your views here.
def search_screen(request):
    return render(request, 'search/search_screen.html', {})