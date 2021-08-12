from django.db.models.fields import DecimalField
from django.shortcuts import redirect, render
from .models import *
from community.models import Magazine
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from taggit.models import Tag
from reviews.forms import ReviewCreateForm

# 전체 보기 페이지
def main(request):
    magazine_list = Magazine.objects.all()
    # 찜을 많이 받은 서비스를 우선적으로 배치
    # 추후에 별점 순으로 변경할 수 있음
    services = Service.objects.annotate(
        num_dibs=Count('dib')).order_by('-num_dibs')[:8]
    ctx = {
        'magazine_list': magazine_list,
        'services': services,
    }
    return render(request, 'services/main.html', context=ctx)

def services_list(request):
    services_list = Service.objects.all()
    categories = Category.objects.all()
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    paginator = Paginator(services_list, 3)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    avg_of_reviews = Service.objects.annotate(avg_reviews=Avg('review__score'))
    # avg_of_reviews = round(avg_of_reviews * 2) / 2

    ctx = {
        'services': services,
        'categories': categories,
        'avg_of_reviews':avg_of_reviews,
    }
    return render(request, 'services/list.html', context=ctx)

# 카테고리별 페이지 보기


def category_list(request, category_slug):
    services_list = Service.objects.filter(
        category__slug__contains=category_slug)
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
        subcategory__slug__contains=sub_category_slug)
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
    service = Service.objects.get(id=pk)
    review_form = ReviewCreateForm()
    number_of_dibs = service.dib_set.all().count()
    avg_of_reviews = service.review.aggregate(Avg('score'))['score__avg']
    avg_of_reviews = round(avg_of_reviews * 2) / 2
    # num_of_full_stars = int(avg_of_reviews // 1)
    # is_half_star = True if avg_of_reviews % 1 ==0.5 else False 

    ctx = {
        'service': service, 
        'form': review_form,
        'number''_of_dibs': number_of_dibs,
        'avg_of_reviews':avg_of_reviews,
        }
    return render(request, 'services/detail.html', context=ctx)


def search(request):
    categories = Category.objects.all()
    query = request.GET.get('search_key')
    search_type = request.GET.get('type')
    if query:
        if search_type == "all":
            results = Service.objects.filter(Q(name__icontains=query) | Q(
            intro__icontains=query) | Q(content__icontains=query)).distinct()
        elif search_type == "name":
            results = Service.objects.filter(name__icontains=query)
        elif search_type == "intro":
            results = Service.objects.filter(intro__icontains=query)
        elif search_type == "content":
            results = Service.objects.filter(content__icontains=query)
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
            num_tags=Count('tags')).filter(num_tags__gte=len(selected)).distinct()

        ctx = {
            'services': services,
            'categories': categories,
        }

        return render(request, 'services/list.html', context=ctx)
    else:
        return render(request, 'services/tags_list.html')
