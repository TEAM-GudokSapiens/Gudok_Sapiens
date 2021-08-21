from django.shortcuts import redirect, render
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from taggit.models import Tag
from reviews.forms import ReviewCreateForm
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
    NUM_OF_DISPLAY = 4
    
    services = Service.objects.annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef('pk')))).annotate(num_dibs=Count('dib')).annotate(avg_reviews=Avg('review__score')).order_by('-num_dibs')[:NUM_OF_DISPLAY]
    new_order_services = Service.objects.annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef('pk')))).order_by("-id")[:NUM_OF_DISPLAY]

    num_of_service = Service.objects.all().count()
    if num_of_service >= NUM_OF_DISPLAY:
        random_services = get_random_services(request, NUM_OF_DISPLAY)
    else:
        random_services = get_random_services(request, num_of_service)

    categories = Category.objects.all()
    
    services_list_by_category = []
    for category in categories:
        category_services = Service.objects.annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef('pk')))).annotate(num_dibs=Count('dib')).annotate(avg_reviews=Avg('review__score')).filter(category__slug = category.slug).order_by('-num_dibs')[:NUM_OF_DISPLAY]
        services_list_by_category.append(category_services)

    ctx = {
        'magazine_list': magazine_list,
        'services': services,
        'random_services': random_services,
        'categories': categories,
        "new_order_services": new_order_services,
        "services_list_by_category":services_list_by_category,
    }
    return render(request, 'services/main.html', context=ctx)

def main_test(request):
    magazine_list = Magazine.objects.all()
    # 찜을 많이 받은 서비스를 우선적으로 배치
    # 추후에 별점 순으로 변경할 수 있음
    NUM_OF_DISPLAY = 4
    services = Service.objects.annotate(
        num_dibs=Count('dib')).order_by('-num_dibs')[:NUM_OF_DISPLAY].annotate(avg_reviews=Avg('review__score'))
    new_order_services = Service.objects.order_by("-id")[:NUM_OF_DISPLAY]
    num_of_service = Service.objects.all().count()
    if num_of_service >= NUM_OF_DISPLAY:
        random_services = get_random_services(request,NUM_OF_DISPLAY)
    else:
        random_services = get_random_services(request, num_of_service)

    categories = Category.objects.all()

    ctx = {
        'magazine_list': magazine_list,
        'services': services,
        'random_services': random_services,
        'categories': categories,
        "new_order_services": new_order_services,
    }
    return render(request, 'services/main_test.html', context=ctx)


def services_list(request):
    sort = request.GET.get('sort','') #url의 쿼리스트링을 가져온다. 없는 경우 공백을 리턴한다
    
    if sort == 'dib':
        services_list = Service.objects.annotate(avg_reviews=Avg('review__score')).annotate(num_dibs=Count('dib')).annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef('pk')))).order_by('-num_dibs', '-created_at')
    elif sort == 'score':
        services_list = Service.objects.annotate(avg_reviews=Avg('review__score')).annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef('pk')))).order_by('-avg_reviews', '-created_at') #복수를 가져올수 있음
    else:
        services_list = Service.objects.annotate(avg_reviews=Avg('review__score')).annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef('pk')))).order_by('-created_at')
    

    categories = Category.objects.all()
    NUM_OF_PAGINATOR = 12
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
    categories = Category.objects.order_by('-id')
    sub_category_list = SubCategory.objects.filter(category__slug__contains=category_slug).order_by('id')
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
    service = Service.objects.annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef('pk')))).get(id=pk)
    review_form = ReviewCreateForm()
    number_of_dibs = service.dib_set.all().count()
    avg_of_reviews = service.review.aggregate(Avg('score'))['score__avg']
    reviews_order_help = Review.objects.filter(target_id=pk).annotate(
    helps_count=Count('reviews_help')).order_by('-helps_count')

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
# def review(request):
#     review_list = Review.objects.filter(
#         service_id=target_id
#     )
#     paginator = Paginator(review_list, 5)  # 한페이지에 10개씩

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'services/detail.html', {'review_list': review_list, 'page_obj': page_obj})


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

def category_lifestyle(request):
    services_list = Service.objects.filter(
        category__slug__contains=lifestyle).annotate(avg_reviews=Avg('review__score'))
    categories = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=lifestyle)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    NUM_OF_PAGINATOR =10
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
        'sub_category_list': sub_category_list,
        'category_slug': lifestyle,
    }
    return render(request, 'services/list.html', context=ctx)

def category_food(request):
    services_list = Service.objects.filter(
        category__slug__contains=food).annotate(avg_reviews=Avg('review__score'))
    categories = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=food)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    NUM_OF_PAGINATOR =10
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
        'sub_category_list': sub_category_list,
        'category_slug': food,
    }
    return render(request, 'services/list.html', context=ctx)

def category_content(request):
    print(category__slug__contains)
    services_list = Service.objects.filter(
        category__slug__contains=content).annotate(avg_reviews=Avg('review__score'))
    categories = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=content)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    NUM_OF_PAGINATOR =10
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
        'sub_category_list': sub_category_list,
        'category_slug': content,
    }
    return render(request, 'services/list.html', context=ctx)

def category_newsletter(request):
    services_list = Service.objects.filter(
        category__slug__contains=newsletter).annotate(avg_reviews=Avg('review__score'))
    categories = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=newsletter)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    NUM_OF_PAGINATOR =10
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
        'sub_category_list': sub_category_list,
        'category_slug': newsletter,
    }
    return render(request, 'services/list.html', context=ctx)

def category_other(request):
    services_list = Service.objects.filter(
        category__slug__contains=other).annotate(avg_reviews=Avg('review__score'))
    categories = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=other)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    NUM_OF_PAGINATOR =10
    paginator = Paginator(services_list, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
        'categories': categories,
        'sub_category_list': sub_category_list,
        'category_slug': other,
    }
    return render(request, 'services/list.html', context=ctx)

def get_sub_categories(category, subcategory):
    services_list = Service.objects.filter(
        subcategory__slug__contains=subcategory).annotate(avg_reviews=Avg('review__score'))
    category_list = Category.objects.all()
    sub_category_list = SubCategory.objects.filter(
        category__slug__contains=category)
    return services_list, category_list, sub_category_list

def make_paginator(request, queryset, NUM_OF_PAGINATOR=10):
    NUM_OF_PAGINATOR = 10
    paginator = Paginator(queryset, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    queryset_list = paginator.get_page(page)
    return queryset_list


def subcategory_daily_item(request):
    category = "lifestyle" 
    subcategory = "daily_item"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_health(request):
    category = "lifestyle" 
    subcategory = "health"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_clothing(request):
    category = "lifestyle" 
    subcategory = "clothing"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_cleaning(request):
    category = "lifestyle" 
    subcategory = "cleaning"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_delivery(request):
    category = "food" 
    subcategory = "delivery"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_beverage(request):
    category = "food" 
    subcategory = "beverage"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_alcohol(request):
    category = "food" 
    subcategory = "alcohol"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_fruit(request):
    category = "food" 
    subcategory = "fruit"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_health_food(request):
    category = "food" 
    subcategory = "health_food"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_bakery(request):
    category = "food" 
    subcategory = "bakery"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_meal_kit(request):
    category = "food" 
    subcategory = "meal_kit"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_snack(request):
    category = "food" 
    subcategory = "snack"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)


def subcategory_video(request):
    category = "content" 
    subcategory = "video"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_music(request):
    category = "content" 
    subcategory = "music"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)

def subcategory_book(request):
    category = "content" 
    subcategory = "book"
    services_list, category_list, sub_category_list = get_sub_categories(category, subcategory)
    num_of_display = 10
    services = make_paginator(request, services_list, num_of_display)
    
    ctx = {
        'services': services,
        'categories': category_list,
        'sub_category_list': sub_category_list,
        'category_slug': category,
    }
    return render(request, 'services/list.html', context=ctx)