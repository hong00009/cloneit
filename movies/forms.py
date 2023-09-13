from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows':'1'}), 
        label='',
    )
    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 6)],
        label='rate',
        required=True,
    )
    class Meta:
        model = Comment
        fields = ('content', 'rating',)
