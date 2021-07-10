from django import forms
from eShopUser.models.feedback import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['name','feedback']