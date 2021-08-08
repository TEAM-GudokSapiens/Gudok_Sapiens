from django import forms
from .models import Review

REVIEW_POINT_CHOICES = (
    ('1', 1),
    ('1.5', 1.5),
    ('2', 2),
    ('2.5', 2.5),
    ('3', 3),
    ('3.5', 3.5),
    ('4', 4),
    ('4.5', 4.5),
    ('5', 5),
)


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['photo', 'title', 'content', 'score', 'period']
        widgets = {
            'score': forms.Select(choices=REVIEW_POINT_CHOICES)
        }
