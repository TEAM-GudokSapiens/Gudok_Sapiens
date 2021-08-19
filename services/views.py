from django.db.models.fields import DecimalField
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from taggit.models import Tag
from reviews.forms import ReviewCreateForm
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from likes.models import Dib, Help
from django.db.models import Exists, OuterRef
from config.utils import get_random_services

from .models import *
from reviews.models import *
from community.models import *

# 전체 보기 페이지


def main(request):
    magazine_list = Magazine.objects.all()
    # 찜을 많이 받은 서비스를 우선적으로 배치
    # 추후에 별점 순으로 변경할 수 있음
    NUM_OF_DISPLAY = 4
    services = Service.objects.annotate(
        num_dibs=Count('dib')).order_by('-num_dibs')[:NUM_OF_DISPLAY].annotate(avg_reviews=Avg('review__score'))
    new_order_services = Service.objects.order_by("-id")[:NUM_OF_DISPLAY]
    num_of_service = Service.objects.all().count()
    if num_of_service >= NUM_OF_DISPLAY:
        random_services = get_random_services(NUM_OF_DISPLAY)
    else:
        random_services = get_random_services(num_of_service)
    categories = Category.objects.all()

    ctx = {
        'magazine_list': magazine_list,
        'services': services,
        'random_services': random_services,
        'categories': categories,
        "new_order_services": new_order_services,
    }
    return render(request, 'services/main.html', context=ctx)


def services_list(request):
    sort = request.GET.get('sort','') #url의 쿼리스트링을 가져온다. 없는 경우 공백을 리턴한다

    if sort == 'dib':
        services_list = Service.objects.annotate(num_dibs=Count('dib')).order_by('-num_dibs', '-created_at')
    elif sort == 'score':
        services_list = Service.objects.annotate(avg_reviews=Avg('review__score')).order_by('-avg_reviews', '-created_at') #복수를 가져올수 있음
    else:
        services_list = Service.objects.order_by('-created_at')

    # if request.user.is_authenticated:
    #     services_list = Service.objects.all().annotate(avg_reviews=Avg('review__score')).annotate(
    #                 is_dib=Exists(Dib.objects.filter(
    #                     users=request.user, service_id=OuterRef('pk')))
    #             )
    # else:
    #     services_list = Service.objects.all().annotate(avg_reviews=Avg('review__score'))
    
    categories = Category.objects.all()
    NUM_OF_PAGINATOR = 10    
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
    }
    
    return render(request, 'services/list.html', context=ctx)


# 카테고리별 페이지 보기


def category_list(request, category_slug):
    services_list = Service.objects.filter(
        category__slug__contains=category_slug).annotate(avg_reviews=Avg('review__score'))
    categories = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=category_slug)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    NUM_OF_PAGINATOR =10
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
        'sub_category_list': sub_category_list,
        'category_slug': category_slug,
    }
    return render(request, 'services/list.html', context=ctx)


def sub_category_list(request, category_slug, sub_category_slug):
    services_list = Service.objects.filter(
        subcategory__slug__contains=sub_category_slug).annotate(avg_reviews=Avg('review__score'))
    categories = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=category_slug)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    NUM_OF_PAGINATOR = 10
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
        'sub_category_list': sub_category_list,
        'category_slug': category_slug,
    }
    return render(request, 'services/list.html', context=ctx)


def services_detail(request, pk):

    if request.user.is_authenticated:
        service = Service.objects.annotate(
            is_dib=Exists(Dib.objects.filter(
                users=request.user, service_id=OuterRef('pk')))
        ).get(id=pk)
        review_form = ReviewCreateForm()
        number_of_dibs = service.dib_set.all().count()
        avg_of_reviews = service.review.aggregate(Avg('score'))['score__avg']
        reviews_order_help = Review.objects.filter(target_id=pk).annotate(helps_count=Count('reviews_help')).annotate(is_help=Exists(
            Help.objects.filter(users=request.user, review_id=OuterRef('pk'))
        )).order_by('-helps_count')

    else:
        service = Service.objects.get(id=pk)
        review_form = ReviewCreateForm()
        number_of_dibs = service.dib_set.all().count()
        avg_of_reviews = service.review.aggregate(Avg('score'))['score__avg']
        reviews_order_help = Review.objects.filter(target_id=pk).annotate(helps_count=Count('reviews_help')).order_by('-helps_count')

    NUM_OF_PAGINATOR = 10
    paginator = Paginator(reviews_order_help, NUM_OF_PAGINATOR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'service': service,
        'form': review_form,
        'number_of_dibs': number_of_dibs,
        'avg_of_reviews': avg_of_reviews,
        'reviews_order_help': reviews_order_help,
        'page_obj': page_obj,
    }
    return render(request, 'services/detail.html', context=ctx)

def search(request):
    categories = Category.objects.all()
    query = request.GET.get('search_key')
    search_type = request.GET.get('type')
    print(request.GET)
    if query:
        if search_type == "all":
            results = Service.objects.filter(Q(name__icontains=query) | Q(
                intro__icontains=query) | Q(content__icontains=query)).annotate(avg_reviews=Avg('review__score')).distinct()
        elif search_type == "name":
            results = Service.objects.filter(name__icontains=query).annotate(
                avg_reviews=Avg('review__score'))
        elif search_type == "intro":
            results = Service.objects.filter(intro__icontains=query).annotate(
                avg_reviews=Avg('review__score'))
        elif search_type == "content":
            results = Service.objects.filter(content__icontains=query).annotate(
                avg_reviews=Avg('review__score'))
        else:
            results = Service.objects.filter(Q(name__icontains=query) | Q(intro__icontains=query) | Q(
                content__icontains=query)).annotate(avg_reviews=Avg('review__score')).distinct()
    else:
        results = []
    ctx = {
        'results': results,
        'query': query,
        'categories': categories,
    }
    return render(request, 'services/search_result.html', context=ctx)


def services_tags(request):
    if request.method == 'POST':
        categories = Category.objects.all()
        selected = request.POST.getlist('selected')
        services = Service.objects.filter(tags__name__in=selected).annotate(
            num_tags=Count('tags')).filter(num_tags__gte=len(selected)).annotate(avg_reviews=Avg('review__score')).distinct()

        ctx = {
            'services': services,
            'categories': categories,
        }

        return render(request, 'services/list.html', context=ctx)
    else:
        return render(request, 'services/tags_list.html')


def same_tag_list(request, tag):
    services = Service.objects.filter(tags__name=tag)
    categories = Category.objects.all()

    ctx = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'services/list.html', context=ctx)

def service_intro(request):
    return render(request, 'services/service_intro.html')