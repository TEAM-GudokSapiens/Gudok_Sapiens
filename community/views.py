from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta

from .models import *
from .forms import BoardForm
from users.models import User
from django.http.response import JsonResponse
import json
# 공지사항


def notice(request):
    notices = Notice.objects.order_by('-created_at')
    paginator = Paginator(notices, 15)  # 한페이지에 15개씩

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'community/notice.html', {'notices': notices, 'page_obj': page_obj})


def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'community/notice_detail.html', {'notice': notice})


# 매거진

def magazine(request):
    magazines = Magazine.objects.order_by('-created_at')
    paginator = Paginator(magazines, 10)  # 한페이지에 10개씩

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'community/magazine.html', {'magazines': magazines, 'page_obj': page_obj})


def magazine_detail(request, pk):
    magazine = get_object_or_404(Magazine, pk=pk)
    return render(request, 'community/magazine_detail.html', {'magazine': magazine})


# 자유게시판

def board(request):
    boards = Board.objects.order_by('-created_at')
    paginator = Paginator(boards, 10)  # 한페이지에 10개씩

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'community/board.html', {'boards': boards, 'page_obj': page_obj})


def board_create(request):
    if not request.user.is_authenticated:  # 로그인이 안되어있을 경우
        return redirect('/users/login')

    if request.method == 'POST':  # post
        form = BoardForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            user_id = request.session.get('user')
            user = request.user
            new_board = Board(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                img=form.cleaned_data['img'],
                user=user
            )
            new_board.save()
            return redirect('community:board')
        else:
            print('------------------------')

    else:  # get
        form = BoardForm()
        ctx = {'form': form}
        return render(request, template_name='community/board_create.html', context=ctx)


def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'community/board_detail.html', {'board': board})


def board_delete(request, pk):
    post = Board.objects.get(id=pk)
    post.delete()
    return redirect('community:board')
