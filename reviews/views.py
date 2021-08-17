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

def reviews_create(request, pk):
    message={}
    if request.method == "POST":
        form = ReviewCreateForm(request.POST, request.FILES)
        if form.is_valid():
            review_form = form.save(commit=False)
            review_form.user = request.user
            review_form.target = Service.objects.get(pk=pk)
            review_form.save()
            return redirect("services:services_detail", pk)
    else:
        form = ReviewCreateForm()

    ctx = {"form": form,
           "service_pk": pk}
    

    return render(request, "reviews/create.html", ctx)


@login_message_required
@csrf_exempt
def submit_ajax(request, pk):
    if request.method == "POST":
        form = ReviewCreateForm(request.POST, request.FILES)
        if form.is_valid():
            print(form['score'].value())
            review_form = form.save(commit=False)
            review_form.user = request.user
            review_form.target = Service.objects.get(pk=pk)
            review_form.save()
            return redirect("services:services_detail", pk)
        else:
            return redirect("services:services_detail", pk)
