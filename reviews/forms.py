from django.forms import ModelForm
from .models import Review


class ReviewCreateForm(ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'score', 'period']
