import json
from django.contrib import messages
from django.core.paginator import Paginator
from users.decorators import login_message_required
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .forms import ReviewCreateForm
from .models import Review
from services.models import Service

@login_message_required
@csrf_exempt
def review_create(request, pk):
    if request.method == "POST":
        form = ReviewCreateForm(request.POST, request.FILES)
        if form.is_valid():
            print(form['score'].value())
            review_form = form.save(commit=False)
            review_form.user = request.user
            review_form.target = Service.objects.get(pk=pk)
            review_form.save()            
            messages.success(request, "리뷰가 성공적으로 작성되었습니다!")
            return redirect("services:services_detail", pk)
        else:
            messages.error(request, "리뷰를 양식에 맞춰 작성해주세요.")
            return redirect("services:services_detail", pk)
