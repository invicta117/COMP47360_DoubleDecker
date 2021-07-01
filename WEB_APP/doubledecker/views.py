from django.shortcuts import render
# origionated from https://docs.djangoproject.com/en/3.2/intro/tutorial01/
from django.http import HttpResponse
# Create your views here.


def main(request):  # origionated from  https://docs.djangoproject.com/en/3.2/intro/tutorial01/
    return render(request, 'doubledecker/index.html')


# origionated from  https://docs.djangoproject.com/en/3.2/intro/tutorial01/
def explore_view(request):
    return render(request, 'doubledecker/explore.html')
