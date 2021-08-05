from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from datetime import date,datetime,timedelta
from .models import *

# 공지사항

def notice(request):
    notices = Notice.objects.order_by('-created_at')
    paginator = Paginator(notices, 15) #한페이지에 15개씩

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'community/notice.html', {'notices':notices , 'page_obj':page_obj})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'community/notice_detail.html', {'notice': notice})


# 매거진

def magazine(request):
    magazines = Magazine.objects.order_by('-created_at')
    paginator = Paginator(magazines, 10) #한페이지에 10개씩

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'community/magazine.html', {'magazines':magazines , 'page_obj':page_obj})

def magazine_detail(request, pk):
    magazine = get_object_or_404(Magazine, pk=pk)
    return render(request, 'community/magazine_detail.html', {'magazine': magazine})