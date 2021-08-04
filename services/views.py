from django.shortcuts import render
from .models import *
from django.contrib import messages 
from django.db.models import Q
from django.views.generic import View, ListView

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

def search(request):
    categories = Category.objects.all()
    query = request.GET.get('search_key')
    if query:
        results = Service.objects.filter(Q (name__icontains=query) | Q(intro__icontains=query) | Q(content__icontains=query)).distinct()
    else:
        results = []
    ctx = {
        'results':results,
        'query':query,
        'categories':categories,
    }
    return render(request, 'services/search_result.html', context=ctx)
        
        

