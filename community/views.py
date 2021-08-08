import json
from django import forms
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
from .models import *
from .forms import BoardForm
from users.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from users.decorators import *


# 공지사항


def notice(request):
    notices = Notice.objects.order_by('-created_at')
    paginator = Paginator(notices, 10)  # 한페이지에 10개씩

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

# 댓글쓰기


@login_message_required
def comment_write_view(request, pk):
    target = get_object_or_404(Board, id=pk)
    user = request.POST.get('user')
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(
            target=target, content=content, user=request.user)
        target.save()
        data = {
            'user': user,
            'content': content,
            'created_at': '방금 전',
            'comment_id': comment.id
        }
        if request.user == target.user:
            data['self_comment'] = '(글쓴이)'

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")

# 댓글 삭제


@login_message_required
def comment_delete_view(request, pk):
    target = get_object_or_404(Board, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk=comment_id)

    if request.user == target_comment.user or request.user.level == '1' or request.user.level == '0':
        target_comment.deleted = True
        target_comment.save()
        target.save()
        data = {
            'comment_id': comment_id,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


# 댓글 카운트

def free_detail_view(request, pk):
    comment = Comment.objects.filter(post=pk).order_by('created_at')
    comment_count = comment.exclude(deleted=True).count()

    context = {
        'comments': comment,
        'comment_count': comment_count,
    }

def comment_write_view(request, pk):
    post = get_object_or_404(Board, id=pk)
    user = request.POST.get('user')
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(post=post, content=content, user=request.user)
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()

        data = {
            'user': user,
            'content': content,
            'created_at': '방금 전',
            'comment_count': comment_count,
            'comment_id': comment.id
        }
        if request.user == post.user:
            data['self_comment'] = '(글쓴이)'
        
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


def comment_delete_view(request, pk):
    post = get_object_or_404(Board, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk = comment_id)

    if request.user == target_comment.user or request.user.level == '1' or request.user.level == '0':
        target_comment.deleted = True
        target_comment.save()
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data = {
            'comment_id': comment_id,
            'comment_count': comment_count,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


# 자유게시판 좋아요기능


def likes(request):
    if request.is_ajax():
        board_id = request.GET['board_id']
        post = Board.objects.get(id=board_id)

        if not request.user.is_authenticated:
            message = "로그인을 해주세요"
            context = {'like_count': post.like.count(), "message": message}
            return HttpResponse(json.dumps(context), content_type='application/json')

        user = request.user
        if post.like.filter(id=user.id).exists():
            post.like.remove(user)
            message = "좋아요 취소"
        else:
            post.like.add(user)
            message = "좋아요"

        context = {'like_count': post.like.count(), "message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')


# 검색기능

def search(request):
    notice = Notice.objects.all()
    magazine = Magazine.objects.all()
    board = Board.objects.all()
    query = request.GET.get('search_key')
    if query:
        notice_results = Notice.objects.filter(Q(title__icontains=query) | Q(
            content__icontains=query)).distinct()
        magazine_results = Magazine.objects.filter(Q(title__icontains=query) | Q(
            content__icontains=query)).distinct()
        board_results = Board.objects.filter(Q(title__icontains=query) | Q(
            content__icontains=query)).distinct()
    else:
        results = []
    ctx = {
        'notice_results': notice_results,
        'notice': notice,

        'magazine_results': magazine_results,
        'magazine': magazine,

        'board_results': board_results,
        'board': board,

        'query': query,
    }
    return render(request, 'community/search.html', context=ctx)



