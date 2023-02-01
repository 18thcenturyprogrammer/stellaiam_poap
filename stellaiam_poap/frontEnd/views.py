from django.shortcuts import render


# Create your views here.
def home(request, *args, **kwargs):
	return render(request, 'frontEnd/home.html')

def index(request, *args, **kwargs):
	return render(request, 'frontEnd/index.html')