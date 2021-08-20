import datetime
import random

from django.db.models.aggregates import Max
from services.models import Service
from django.db.models import Avg


def get_filename(filename):
    string = "asdf"
    for i in range(1,20):
        string+=str(random.randrange(0,10))
        
    return filename.upper()+string

def get_random_services(input_num):
    max_id = Service.objects.all().aggregate(max_id=Max("id"))["max_id"]
    new_list = []
    while input_num != len(new_list):
        pk = random.randint(1, max_id)
        service = Service.objects.annotate(avg_reviews=Avg('review__score')).filter(pk=pk).first()
        if service and service not in new_list:
            new_list.append(service)

    return new_list

