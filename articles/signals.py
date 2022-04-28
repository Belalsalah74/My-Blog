from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Article
from django.utils.text import slugify

@receiver(post_save,sender=Article)
def article_post_save(instance,*args,**kwargs,):
    if instance.slug is None:
        instance.slug = slugify(instance.title)
        instance.save()

    qs = Article.objects.filter(slug=instance.slug).exclude(id=instance.id)
    
    if qs.exists():
        instance.slug = slugify(f'{instance.slug}-{instance.id}')
        instance.save()
    
    qs_t = Article.objects.filter(title__exact=instance.title).exclude(id=instance.id)
    if qs_t.exists():
        instance.title = f'{instance.title}-{instance.id}'
        instance.save()
