from django import forms
from .models import Review

REVIEW_POINT_CHOICES = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
)


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['target', 'photo', 'title', 'content', 'score', 'period']
        widgets = {
            'target': forms.HiddenInput(),
            'score': forms.Select(choices=REVIEW_POINT_CHOICES)
        }
