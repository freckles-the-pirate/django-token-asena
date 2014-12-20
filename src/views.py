from django.shortcuts import render
from .models import *

def view(request):

    context = { '' : '' }
    return render(request, 'index.html', context)

