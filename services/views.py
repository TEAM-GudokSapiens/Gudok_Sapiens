from django.shortcuts import render
from .models import *
from django.http import HttpResponse

def main(request):
    ctx = {"main": main}
    return render(request, 'services/main.html', context=ctx)

# 전체 보기 페이지
def services_list(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    ctx = {
        'services': services,
        'categories':categories,
        }
    return render(request, 'services/list.html', context=ctx)

# 카테고리별 페이지 보기
def category_list(request, slug):
    services = Service.objects.filter(category__slug__contains = slug)
    categories = Category.objects.all()

    ctx = {
        'services': services,
        'categories':categories,
        }
    return render(request, 'services/list.html', context=ctx)

def services_detail(request, pk):
    service = Service.objects.get(id=pk)
    ctx = {'service': service}
    return render(request, 'services/detail.html', context=ctx)




