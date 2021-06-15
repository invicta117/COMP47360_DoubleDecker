from django.shortcuts import render
from django.http import HttpResponse # origionated from https://docs.djangoproject.com/en/3.2/intro/tutorial01/
# Create your views here.
def main(request): #  origionated from  https://docs.djangoproject.com/en/3.2/intro/tutorial01/
    return render(request, 'doubledecker/index.html')