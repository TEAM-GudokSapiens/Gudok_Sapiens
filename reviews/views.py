from django.shortcuts import render
from .models import Review
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from reviews.forms import ReviewCreateForm
from services.models import Service
# import json
# from django.views.decorators.csrf import csrf_exempt
# from django.http.response import JsonResponse
# from .models import Review
# from services.models import Service


# Create your views here.
# def review_create(request):
#     if not request.user.is_authenticated:  # 로그인이 안되어있을 경우
#         return redirect('/users/login')

#     if request.method == 'POST':  # post
#         form = ReviewCreateForm(request.POST, request.FILES)
#         print(form)
#         if form.is_valid():
#             target_id = request.session.get('target')
#             user_id = request.session.get('user')
#             target = request.target
#             user = request.user
#             new_review = Review(
#                 photo=form.cleaned_data['photo'],
#                 title=form.cleaned_data['title'],
#                 content=form.cleaned_data['content'],
#                 target=target,
#                 user=user
#             )
#             new_review.save()
#             return redirect('services:services_detail')
#         else:
#             form = ReviewCreateForm(request.post)

#     else:  # get
#         form = ReviewCreateForm()
#         ctx = {'form': form}
#         return render(request, template_name='reviews/create.html', context=ctx)


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreateForm
    success_url = reverse_lazy('services:services_detail')
    template_name = 'reviews/create.html'

    def form_valid(self, form):
        # temp_review = form.save(commit=False)
        # temp_review.target = form.cleand_data['target']
        # temp_review.user = self.request.user
        form.instance.user = self.request.user
        form.instance.target = Service.objects.get(pk=2)

        return super(ReviewCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('services:services_detail', kwargs={'pk': self.object.target.id})


# @csrf_exempt
# def submit_ajax(request):
#     req = json.loads(request.body)
#     service_id = req['service_id']
#     title = req['title']
#     content = req['content']
#     score = req['score']
#     period = req['period']
#     photo = req['photo']
#     service = Service.objects.get(id=service_id)
#     review = Review.objects.create(target=service, user=request.user, photo=photo,
#                                    title=title, content=content, score=score, period=period)
#     review.save()
#     return JsonResponse({'service_id': service_id, 'review_id': review.id,
#                          'review_title': review.title, 'review_content': review.content, 'review_score': review.score,
#                          'review_period': review.period, 'review_updated_at': review.updated_at, 'review_photo': review.photo.url})
