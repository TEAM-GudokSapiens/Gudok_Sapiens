import services
from django.shortcuts import redirect, render
from .models import Dib
from django.http.response import JsonResponse

# Create your views here.
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
    
