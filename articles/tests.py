from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from articles.models import Article

class ArticleTestCase(TestCase):

    def setUp(self) -> None:
        self.n_articles = 50
        User.objects.create(username='belal',id=1)
        for i in range(self.n_articles):
            Article.objects.create(title='hello world',user_id=1,content='contentblah')


    def test_qs_exists(self):
        qs = Article.objects.all().exists()
        self.assertTrue(qs)


    def test_qs_count(self):
        qs = Article.objects.count()
        self.assertEqual(qs,self.n_articles)

    def test_slug(self):
        article = Article.objects.order_by('id').first()
        title = article.title
        slug = article.slug
        slug_title = slugify(title)
        self.assertEqual(slug,slug_title)

    # def test_slug_unique(self): #with unique title_signal
    #     qs = Article.objects.all().values_list('slug')
    #     unique_slug_list = list(set(qs))
    #     self.assertEqual(len(qs),len(unique_slug_list))

    def test_slug_unique(self): #with uniqe_title signal turned off
        qs = Article.objects.all().values_list('slug')
        unique_slug_list = list(set(qs))
        self.assertEqual(len(qs),len(unique_slug_list))
    

    # def test_title_unique(self):
    #     qs = Article.objects.all().values_list('title')
    #     unique_title_list = list(set(qs))
    #     self.assertEqual(qs,unique_title_list)
    
    def test_article_search(self):
        qs = Article.objects.search('hello world')
        self.assertIsNotNone(qs.exists())
        self.assertEqual(qs.count(),self.n_articles)
        qs = Article.objects.search('contentblah')
        self.assertIsNotNone(qs.exists())
        self.assertEqual(qs.count(),self.n_articles)