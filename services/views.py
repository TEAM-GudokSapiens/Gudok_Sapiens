from django.shortcuts import render
<<<<<<< HEAD
from .models import *
from django.contrib import messages 
from django.db.models import Q
from django.views.generic import View, ListView
=======
from .models import Service

from .models import *
from django.contrib import messages
from django.db.models import Q
from django.views.generic import View, ListView

>>>>>>> 0d1a5b323888b404fb0fbd3f9a85b7c455b0649f

def main(request):
    ctx = {"main": main}
    return render(request, 'services/main.html', context=ctx)

# 전체 보기 페이지
<<<<<<< HEAD
=======


>>>>>>> 0d1a5b323888b404fb0fbd3f9a85b7c455b0649f
def services_list(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    ctx = {
        'services': services,
<<<<<<< HEAD
        'categories':categories,
        }
    return render(request, 'services/list.html', context=ctx)

# 카테고리별 페이지 보기
def category_list(request, slug):
    services = Service.objects.filter(category__slug__contains = slug)
=======
        'categories': categories,
    }
    return render(request, 'services/list.html', context=ctx)

# 카테고리별 페이지 보기


def category_list(request, slug):
    services = Service.objects.filter(category__slug__contains=slug)
>>>>>>> 0d1a5b323888b404fb0fbd3f9a85b7c455b0649f
    categories = Category.objects.all()

    ctx = {
        'services': services,
<<<<<<< HEAD
        'categories':categories,
        }
    return render(request, 'services/list.html', context=ctx)

=======
        'categories': categories,
    }
    return render(request, 'services/list.html', context=ctx)


>>>>>>> 0d1a5b323888b404fb0fbd3f9a85b7c455b0649f
def services_detail(request, pk):
    service = Service.objects.get(id=pk)
    ctx = {'service': service}
    return render(request, 'services/detail.html', context=ctx)

<<<<<<< HEAD
=======

>>>>>>> 0d1a5b323888b404fb0fbd3f9a85b7c455b0649f
def search(request):
    categories = Category.objects.all()
    query = request.GET.get('search_key')
    if query:
<<<<<<< HEAD
        results = Service.objects.filter(Q (name__icontains=query) | Q(intro__icontains=query) | Q(content__icontains=query)).distinct()
    else:
        results = []
    ctx = {
        'results':results,
        'query':query,
        'categories':categories,
    }
    return render(request, 'services/search_result.html', context=ctx)
        
        

=======
        results = Service.objects.filter(Q(name__icontains=query) | Q(
            intro__icontains=query) | Q(content__icontains=query)).distinct()
    else:
        results = []
    ctx = {
        'results': results,
        'query': query,
        'categories': categories,
    }
    return render(request, 'services/search_result.html', context=ctx)
>>>>>>> 0d1a5b323888b404fb0fbd3f9a85b7c455b0649f
