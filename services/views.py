from django.shortcuts import render
from .models import Service

# TODO:카테고리 별로 db에 요청해야함
def services_list(request):
    services = Service.objects.all()
    ctx = {'services': services}
    return render(request, 'services/list.html', context=ctx)


