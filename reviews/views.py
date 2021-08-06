from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Review
from services.models import Service


# Create your views here.


@csrf_exempt
def submit_ajax(request):
    req = json.loads(request.body)
    service_id = req['service_id']
    title = req['title']
    content = req['content']
    score = req['score']
    period = req['period']
    photo = req['photo']
    service = Service.objects.get(id=service_id)
    review = Review.objects.create(target=service, user=request.user, photo=photo,
                                   title=title, content=content, score=score, period=period)
    review.save()
    return JsonResponse({'service_id': service_id, 'review_id': review.id,
                         'review_title': review.title, 'review_content': review.content, 'review_score': review.score,
                         'review_period': review.period, 'review_updated_at': review.updated_at, 'review_photo': review.photo.url})
