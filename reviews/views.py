from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Service, Review

# Create your views here.


@csrf_exempt
def submit_ajax(request):
    req = json.loads(request.body)
    service_id = req['service_id']
    title = req['title']
    content = req['content']
    score = req['stars']
    period = req['period']
    service = Service.objects.get(id=service_id)
    review = Review.objects.create(target=service, user=request.user,
                                   title=title, content=content, score=score, period=period)
    review.save()
    return JsonResponse({'service_id': service_id, 'review_id': review.id, 'content': review.content})
