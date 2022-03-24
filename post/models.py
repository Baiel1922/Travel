from django.core.validators import MaxValueValidator
from django.db import models

from account.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField()
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    pin = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        ordering = ['id']


class PostImage(models.Model):
    image = models.ImageField(upload_to='images', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    pin = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.author}: {self.pin} - {self.rating}'
