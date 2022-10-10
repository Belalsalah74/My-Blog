from django import forms
from .models import Article, Category, Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control  my-3', 'placeholder': 'Leave a comment','rows':'','cols':''})
        self.fields['content'].label = ''


 

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control  my-3', 'placeholder': 'Category name'})
    

class ArticleForm(forms.ModelForm):
    qs = Category.objects.all()
    category = forms.ModelMultipleChoiceField(queryset=qs,required=False)
   

    class Meta:
        model = Article
        fields = ['title','content','category']
        

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label=''
            self.fields[field].help_text=''
            if field == 'category':
                self.fields[field].label = 'Choose category'

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control  my-3', 'placeholder': 'Enter article title'})
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control  my-3', 'placeholder': 'What is on your mind'})
    
        self.fields['category'].widget.attrs.update(
            {'class': 'form-select  my-1', })
    
       