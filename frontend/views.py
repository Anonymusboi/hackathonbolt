from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
    # Sends it to index.html, which then leads to main.js, which is basically a combination of everything in src
    # It starts from index.js to App.js then just follow the code from there.
    return render(request, 'frontend/index.html') 