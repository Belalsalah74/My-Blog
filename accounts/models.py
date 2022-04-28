from PIL import Image
from django.dispatch import receiver
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save , post_save




class ProfileQueryset(models.QuerySet):
    def search(self,query):
        lookups = Q(user__username__icontains=query)
        return self.filter(lookups)

class ProfileManager(models.Manager):
    
    def get_queryset(self):
        return ProfileQueryset(self.model,using=self.db)

    def search(self,query):
        return self.get_queryset().search(query)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profile_pics',default='anon.jpg',blank=True,null=True)
    objects = ProfileManager()

    def get_articles(self):
        return self.user.article_set.all()

    def __str__(self):
        return self.user.username




@receiver(post_save,sender=Profile)
def resize_img(sender,instance,created,*args, **kwargs):
    if created and instance.img is not None:
       img = Image.open(instance.img.path)
       output_size = (200,200)
       img.thumbnail(output_size)
       img.save(instance.img.path)
    #    instance.save()

# @receiver(post_save,sender=User)
# def create_profile(sender,instance,created,*args, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#         instance.profile.save()



# @receiver(post_save,sender=User)
# def profile(sender,instance,*args, **kwargs):
#     Profile.objects.get_or_create(user=instance)
#     instance.profile.save()



# @receiver(post_save,sender=User)
# def profile(sender,instance,*args, **kwargs):
#     try :Profile.objects.get(user=instance)

#     except Profile.DoesNotExist:
#         Profile.objects.create(user=instance)
#         instance.profile.save()




