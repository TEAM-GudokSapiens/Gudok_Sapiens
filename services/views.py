from django.db.models.fields import DecimalField
from django.shortcuts import redirect, render
from .models import *
from community.models import Magazine
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from taggit.models import Tag
from reviews.forms import ReviewCreateForm
from reviews.models import Review
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from likes.models import Dib, Help
from django.db.models import Exists, OuterRef
from config.utils import get_random_services
from reviews.models import *

# 전체 보기 페이지


def main(request):
    magazine_list = Magazine.objects.all()
    # 찜을 많이 받은 서비스를 우선적으로 배치
    # 추후에 별점 순으로 변경할 수 있음
    services = Service.objects.annotate(
        num_dibs=Count('dib')).order_by('-num_dibs')[:8].annotate(avg_reviews=Avg('review__score'))
    new_order_services = Service.objects.order_by("-id")[:4]
    random_services = get_random_services(4)
    categories = Category.objects.all()

    ctx = {
        'magazine_list': magazine_list,
        'services': services,
        'random_services':random_services,
        'categories':categories,
        "new_order_services":new_order_services,
    }
    return render(request, 'services/main.html', context=ctx)


def services_list(request):
    services_list = Service.objects.all().annotate(avg_reviews=Avg('review__score')).annotate(
        is_dib=Exists(Dib.objects.filter(
            users=request.user, service_id=OuterRef('pk')))
    )
    categories = Category.objects.all()
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    paginator = Paginator(services_list, 3)
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
    paginator = Paginator(services_list, 3)
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
    paginator = Paginator(services_list, 3)
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
    service = Service.objects.annotate(
        is_dib=Exists(Dib.objects.filter(
            users=request.user, service_id=OuterRef('pk')))
    ).get(id=pk)
    review_form = ReviewCreateForm()
    number_of_dibs = service.dib_set.all().count()
    avg_of_reviews = service.review.aggregate(Avg('score'))['score__avg']
    # num_of_full_stars = int(avg_of_reviews // 1)
    # is_half_star = True if avg_of_reviews % 1 ==0.5 else False
    reviews_order_help = Review.objects.filter(target_id=pk).annotate(dibs_count=Count('reviews_help')).annotate(is_help=Exists(
        Help.objects.filter(users=request.user, review_id=OuterRef('pk'))
    )).order_by('-dibs_count')

    review_list = service.get_review()
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'service': service,
        'form': review_form,
        'number_of_dibs': number_of_dibs,
        'avg_of_reviews': avg_of_reviews,
        'reviews_order_help': reviews_order_help,
        'review_list': review_list,
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
            results = Service.objects.filter(Q(name__icontains=query) | Q(
            intro__icontains=query) | Q(content__icontains=query)).annotate(avg_reviews=Avg('review__score')).distinct()
       
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

# @csrf_exempt
# def dibs_ajax(request):
#     req = json.loads(request.body)
#     print(req)
#     service_id = req['id']
#     new_dib, created = Dib.objects.get_or_create(users_id=request.user.id, service_id=service_id)
#     # created==True면 이번에 만들었음.
#     # created ==False -> not created ==True는 이미 만들어져서 삭제하러 가는 것.
#     if not created:
#         new_dib.delete()
#     else:
#         pass

#     return JsonResponse({'id': service_id})
