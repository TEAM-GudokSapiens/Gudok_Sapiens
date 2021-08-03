from django.shortcuts import render
from .models import Service

# TODO:카테고리 별로 db에 요청해야함
def services_list(request):
    services = Service.objects.all()
    ctx = {'services': services}
    return render(request, 'services/list.html', context=ctx)

def category_list(request, slug):
    services = Service.objects.filter(category.slug==slug)
    ctx = {'services': services}
    return render(request, 'services/list.html', context=ctx)


def services_detail(request, pk):
    service = Service.objects.get(id=pk)
    ctx = {'service': service}
    return render(request, 'services/detail.html', context=ctx)

