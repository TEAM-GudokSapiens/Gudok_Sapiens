from django.shortcuts import render
from .models import Service


def main(request):
    ctx = {"main": main}
    return render(request, 'services/main.html', context=ctx)
# Create your views here.


def services_detail(request, pk):
    service = Service.objects.get(id=pk)
    ctx = {'service': service}
    return render(request, 'services/detail.html', context=ctx)
