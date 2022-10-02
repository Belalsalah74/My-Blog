from django import forms
from .models import Article, Category, Comments



class CommentForm(forms.ModelForm):    
    class Meta:
        model = Comments
        fields = ['content']


 

class CategoryForm(forms.ModelForm):
    name = forms.CharField(min_length=2,required=False,widget=forms.TextInput({'placeholder':'Category name',}))
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'New category'
    
class ArticleForm(forms.ModelForm):
    qs = Category.objects.all()
    category = forms.ModelMultipleChoiceField(queryset=qs,required=False)
   

    class Meta:
        model = Article
        fields = ['title','content','category']
        

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
       