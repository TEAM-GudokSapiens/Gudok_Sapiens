from django import forms
from django.forms.widgets import NumberInput

class StarWidget(forms.TextInput):
    input_type = 'rating'
    template_name = 'reviews/star_rate.html'

    class Media:
        css = {
            'all': [
                'widgets/rateit/rateit.css'
            ],
        }
        js = [
            "//code.jquery.com/jquery-3.4.1.min.js",
            'widgets/rateit/jquery.rateit.min.js',
        ]

    def build_attrs(self, *args, **kwargs):
            attrs = super().build_attrs(*args, **kwargs)
            attrs.update({
                'min': 0,
                'max': 5,
                'step': 0.5,
            })
            return attrs

class RangeInput(NumberInput):
    input_type = "range"