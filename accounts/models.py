from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=999,blank=True,null=True)
    img = models.ImageField(upload_to='staticfiles/media/profile_pics',default='staticfiles/media/anon.jpg',blank=True,null=True)

    def get_articles(self):
        return self.user.article_set.all()

    def __str__(self):
        return self.user.username




# @receiver(post_save,sender=Profile)
# def resize_img(sender,instance,created,*args, **kwargs):
#     if instance.img is not None:
#        img = Image.open(instance.img.path)
#        output_size = (200,200)
#        img.thumbnail(output_size)
#        img.save(instance.img.path)



