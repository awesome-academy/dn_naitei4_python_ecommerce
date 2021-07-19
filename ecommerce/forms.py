from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Cart, Comment, Profile, Review

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birthday','address')
        labels = {'birthday':_('birthday'),'address':_('address')}

class ReviewForm(forms.ModelForm):
    def clean_rate(self):
        data = self.cleaned_data.get("rate", 5)
        if data < 1 or data > 5:
            raise forms.ValidationError("Rate must be within range 1 to 5")
        if not str(data).isdigit() :
            raise forms.ValidationError("Rate must be interger")
        return data

    class Meta:
        model = Review
        fields = ["rate", "title","content"]
        help_texts = {
            'title': 'Your review title must be at least 20 characters.',
            'content': 'Your review content must be at least 50 characters.'
        }
        widgets = {
            'rate': forms.NumberInput(attrs={'class':'form-control','min':'1','max':'5'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rate'].widget.attrs.update(size='60')
        self.fields['title'].widget.attrs.update(size='60')
        self.fields['content'].widget.attrs.update(size='60')
        self.fields['title'].help_text = '<small class="form-text text-muted">Your review title must be at least 20 characters.</small>'
        self.fields['content'].help_text = '<small class="form-text text-muted">Your review content must be at least 50 characters.</small>'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        help_texts = { 'comment' : 'Your comment content must be at least 5 characters.'}
        widgets = { 
            'comment' : forms.Textarea(attrs={'class':'form-control'})
        }

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]
        widgets = { 
            'quantity' : forms.NumberInput(attrs={'class':'form-control'})
        }
