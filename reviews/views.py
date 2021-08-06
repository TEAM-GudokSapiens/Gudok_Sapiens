from services.models import Service
from django.shortcuts import render, redirect
from .models import Review
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from reviews.forms import ReviewCreateForm


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'reviews/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.target = Service.objects.get(pk=1)
        return super(ReviewCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('services:services_detail', kwargs={'pk': self.object.target.id})

# def reviews_create(request, pk):
#     if request.method == "POST":
#         form = ReviewCreateForm(request.POST)
#         if form.is_valid():
#             review_form = form.save(commit=False)
#             review_form.user = request.user
#             review_form.target = Service.objects.get(pk=pk)
#             review_form.save()
#             return redirect("services:services_list")
#     else:
#         form = ReviewCreateForm()

#     ctx = {"form": form}
#     return render(request, "reviews/create.html", ctx)
