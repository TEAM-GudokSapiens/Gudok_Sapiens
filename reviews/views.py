from django.shortcuts import render
from .models import Review
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from reviews.forms import ReviewCreateForm


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreateForm
    success_url = reverse_lazy('services:services_detail')
    template_name = 'reviews/create.html'

    def form_valid(self, form):
        temp_review = form.save(commit=False)
        temp_review.target = self.object.service
        temp_review.user = self.request.user
        # temp_review.target = form.data.get('target')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('services:services_detail', kwargs={'pk': self.object.target.id})

# def create(request):
#     ctx = {"create": create}
#     return render(request, 'revieews/create.html', context=ctx)
