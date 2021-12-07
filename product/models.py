from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     cash = models.DecimalField(max_digits=7, decimal_places=2,default=0)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     tag= models.CharField(max_length=255,unique=True,null=False)
#     SEX_CHOICES = (
#         ('F', 'Female',),
#         ('M', 'Male',),
#         )
#     sex = models.CharField(
#         max_length=1,
#         choices=SEX_CHOICES,
#     )

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Category(models.Model):
    name= models.CharField(max_length=255)
    description= models.CharField(max_length=1000, null=True)
    slug = models.SlugField()

    class Meta:
        ordering=('name',)

    def __str__(self):
        return self.name
   
    def get_absolute_url(self):
        return f'/{self.slug}'

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE,null=True)
    name= models.CharField(max_length=255)
    description= models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    no_of_pieces = models.DecimalField(max_digits=4, decimal_places=1, default=1)
    slug = models.SlugField()
    thumbnail=models.ImageField(upload_to='uploads/',blank=True,null=True)
    imagemain=models.ImageField(upload_to='uploads/',blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'

    def get_imagemain (self):
        if self.imagemain:
            return'http://127.0.0.1:8000'+ self.imagemain.url
        return ''
    def get_thumbnail (self):
        if self.thumbnail:
            return'http://127.0.0.1:8000'+ self.thumbnail.url
        else:
            if self.imagemain:
                self.thumbnail = self.make_thumbnail(self.imagemain)
                self.save()

                return'http://127.0.0.1:8000'+ self.thumbnail.url
            else:
                return ''
    def make_thumbnail (self, imagemain, size=(300,200)) :
        img = Image.open(imagemain)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG',quality=85)
        thumbnail = File(thumb_io,name=imagemain.name)
        return thumbnail

# class Order(models.Model):
#     maker= models.ForeignKey(Profile,related_name='orders',on_delete=models.CASCADE,null=False)
#     product = models.ForeignKey(Product,related_name='orders',on_delete=models.CASCADE,null=False)
#     sold = models.BooleanField(default=False)
#     amount = models.DecimalField(max_digits=3,decimal_places=0, default=1)

# class Gift (models.Model):
#     order= models.ForeignKey(Order,related_name='gift',on_delete=models.CASCADE,null=False)
#     reciever= models.ForeignKey(Profile,related_name='gifts',on_delete=models.CASCADE,null=False)

# class Transaction (models.Model):
#     sender = models.ForeignKey(Profile,related_name= 'sent_money',on_delete=models.CASCADE,null=False)
#     reciever = models.ForeignKey(Profile,related_name= 'recieved_money',on_delete=models.CASCADE,null=False)
#     transaction_size = models.DecimalField(max_digits=3,decimal_places=2, default=0)
    
# class Share(models.Model):
#     product=models.ForeignKey(Product,related_name='shared_by',on_delete=models.CASCADE,null=False)
#     share_holder=models.ForeignKey(Profile,related_name='shared',on_delete=models.CASCADE,null=False)