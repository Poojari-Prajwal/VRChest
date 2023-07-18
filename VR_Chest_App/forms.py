from django import forms
from django.forms import ModelForm
from .models import Review, Article, DoctorLeave

class ReviewForm(ModelForm):
    class Meta:
        model= Review
        fields= ('Review_username','Review_text','rating')
        widgets= {
            'Review_text':  forms.Textarea(attrs={'class':'form-control','rows':3}),
            'Review_username': forms.TextInput(attrs={'class':'form-control'}), 
            'rating':  forms.Select(attrs={'class':'form-select'})
        }
        labels={
            'Review_username': 'Name * ',
            'Review_text':  'Review',
            'rating':  'Rating * ',
        }

class ArticleForm(ModelForm):
    class Meta :
        model= Article
        fields=('title', 'content', 'link')
        widgets= {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':10}),
            'link': forms.Textarea(attrs={'class':'form-control', 'rows':2})
        }
        labels={
            'title':'Title *',
            'content':'Content *',
            'link':'E-Article link (if any)'
        }
        

class DoctorLeaveForm(forms.ModelForm):
    class Meta:
        model = DoctorLeave
        fields = ['doctor', 'leave_date']