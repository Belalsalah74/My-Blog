from django import forms
from .models import Article, Category, Comments



class CommentForm(forms.ModelForm):
    content = forms.CharField(label='',required=False,widget=forms.Textarea({'rows':4,'placeholder':'Add comment'}))
    
    class Meta:
        model = Comments
        fields = ['content']
    
    def is_valid(self):
        # super().is_valid()
        content = self.data.get('content')
        if len(str(content)) == 0 :
            return False
        return True

 

class CategoryForm(forms.ModelForm):
    name = forms.CharField(min_length=2,required=False,widget=forms.TextInput({'placeholder':'Category name',}))
    class Meta:
        model = Category
        fields = ['name']

    # def clean(self):
    #     name = self.cleaned_data['name']
    #     if len(str(name)) > 0:
    #         return self.cleaned_data
    #     return None

    def is_valid(self):
        super().is_valid()
        name = self.data['name']
        if len(str(name)) == 0:
            return False
        return True

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'New category'
    
class ArticleForm(forms.ModelForm):
    qs = Category.objects.all()
    category = forms.ModelMultipleChoiceField(queryset=qs,required=False)
    # title = forms.CharField(widget=forms.TextInput({'placeholder':'Article title','autofocus':'on','autocomplete':'off','padding':'20px'}),label='',)
    # content = forms.Textarea()
   

    class Meta:
        model = Article
        fields = ['title','content','category']
        

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs.update({'placeholder':'Article title','autofocus':'on','margin-bottom':20})
        # self.fields['title'].label = ''        
        # self.fields['content'].label = ''        



    # def clean(self):
    #     title = self.cleaned_data['title']
    #     titles_q = Article.objects.filter(title__exact=title)
    #     if titles_q.exists():
    #         self.add_error('title', f'{title} already taken, please choose another one')
    #     return self.cleaned_data

# =================================================================

class ArticleTry(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean(self) :
        cleaned_data = self.cleaned_data
        title = cleaned_data['title']
        titles = Article.objects.filter(title__exact=title).values('title')
        content = cleaned_data['content']
        for i in range(len(titles)):
            if title.lower() in titles[i]['title']:
                self.add_error('title', 'this title is taken')
                # raise forms.ValidationError('Title already exists!!!')
        if title in content:
            self.add_error('content','content error')
        return cleaned_data


    # def clean_title(self):
    #     cleaned_data = self.cleaned_data
    #     title = cleaned_data['title']
    #     titles = Article.objects.filter(title__exact=title).values('title')
    #     for i in range(len(titles)):
    #         if title.lower() in titles[i]['title']:
    #             raise forms.ValidationError('Title already exists!!!')
    #     return title


    # def clean_content(self):
    #     cleaned_data = self.cleaned_data
    #     content = cleaned_data['content']
    #     return content
