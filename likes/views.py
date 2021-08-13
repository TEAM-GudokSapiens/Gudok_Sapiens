from django.http.request import HttpRequest
import services
from django.shortcuts import redirect, render
from .models import Dib, Help
from django.http.response import HttpResponse, JsonResponse
from users.decorators import login_message_required
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_message_required
def likes_dibs(request, pk):
    new_dib, created = Dib.objects.get_or_create(users_id=request.user.id, service_id=pk)
    # created==True면 이번에 만들었음.
    # created ==False -> not created ==True는 이미 만들어져서 삭제하러 가는 것. 
    if not created:
        new_dib.delete()
    else:
        pass

# 직전 url를 설정하기 
    previous_url = request.META.get('HTTP_REFERER')

    return redirect(previous_url)

@login_message_required
def likes_helps(request, pk):
    new_help, created = Help.objects.get_or_create(users_id=request.user.id, review_id=pk)
    # created==True면 이번에 만들었음.
    # created ==False -> not created ==True는 이미 만들어져서 삭제하러 가는 것. 
    if not created:
        new_help.delete()
    else:
        pass

# 직전 url를 설정하기 
    previous_url = request.META.get('HTTP_REFERER')

    return redirect(previous_url)

@csrf_exempt
def dibs_ajax(request):
    req = json.loads(request.body)
    service_id = req['id']
    print(service_id)
    new_dib, created = Dib.objects.get_or_create(users_id=request.user.id, service_id=service_id)
    # created==True면 이번에 만들었음.
    # created ==False -> not created ==True는 이미 만들어져서 삭제하러 가는 것. 
    if not created:
        new_dib.delete()
    else:
        pass
    
    return JsonResponse({'id': service_id})

@csrf_exempt
def help_ajax(request):
    req = json.loads(request.body)
    review_id = req['id']
    new_help, created = Help.objects.get_or_create(users_id=request.user.id, review_id=review_id)
    # created==True면 이번에 만들었음.
    # created ==False -> not created ==True는 이미 만들어져서 삭제하러 가는 것. 
    if not created:
        new_help.delete()
    else:
        pass
    
    return JsonResponse({'id': review_id})