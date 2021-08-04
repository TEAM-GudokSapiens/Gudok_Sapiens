from django.shortcuts import render
from .models import *
from django.contrib import messages 
from django.db.models import Q
from django.views.generic import View, ListView

def main(request):
    ctx = {"main": main}
    return render(request, 'services/main.html', context=ctx)

# 전체 보기 페이지
def services_list(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    ctx = {
        'services': services,
        'categories':categories,
        }
    return render(request, 'services/list.html', context=ctx)

# 카테고리별 페이지 보기
def category_list(request, slug):
    services = Service.objects.filter(category__slug__contains = slug)
    categories = Category.objects.all()

    ctx = {
        'services': services,
        'categories':categories,
        }
    return render(request, 'services/list.html', context=ctx)

def services_detail(request, pk):
    service = Service.objects.get(id=pk)
    ctx = {'service': service}
    return render(request, 'services/detail.html', context=ctx)


class ServiceListView(ListView):
    model = Service
    template_name = 'services/search_result.html'
    context_object_name = 'service_list_view'

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        service_list = Service.objects.all()

        if search_keyword :
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_service_list = service_list.filter(Q (name__icontains=search_keyword) | Q(intro__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'name_content':
                    search_service_list = service_list.filter(Q (name__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'name':
                    search_service_list = service_list.filter(name__icontains=search_keyword)
                elif search_type == 'intro':
                    search_service_list = service_list.filter(intro__icontains=search_keyword)
                elif search_type == 'content':
                    search_service_list = service_list.filter(content__icontains=search_keyword)
                
                return search_service_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return service_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type

        return context



