from asena import views
from django.http import HttpResponse

@views.token_protect()
def my_view(request, x, y):
    x = int(x)
    y = int(y)
    return HttpResponse("%d + %d is %d"%(x, y, x+y))