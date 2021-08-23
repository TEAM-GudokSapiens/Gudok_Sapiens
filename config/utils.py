import datetime
import random

from django.db.models.aggregates import Max
from services.models import Service
from django.db.models import Avg
from django.db.models import Exists, OuterRef
from likes.models import Dib
from django.core.paginator import Paginator


def get_filename(filename):
    string = "asdf"
    for i in range(1, 20):
        string += str(random.randrange(0, 10))

    return filename.upper()+string


def get_random_services(request, input_num):
    max_id = Service.objects.all().aggregate(max_id=Max("id"))["max_id"]
    new_list = []
    while input_num != len(new_list):
        pk = random.randint(1, max_id)
        service = Service.objects.annotate(is_dib=Exists(Dib.objects.filter(users__pk=request.user.id, service_id=OuterRef(
            'pk')))).annotate(avg_reviews=Avg('review__score')).filter(pk=pk).first()
        if service and service not in new_list:
            new_list.append(service)

    return new_list


def make_paginator(request, queryset, NUM_OF_PAGINATOR=5):
    paginator = Paginator(queryset, NUM_OF_PAGINATOR)
    page = request.GET.get('page')
    queryset_list = paginator.get_page(page)
    return queryset_list
