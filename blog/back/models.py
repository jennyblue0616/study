from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=20)
    desc = models.CharField(max_length=150)
    content = models.TextField()
    img = models.ImageField(upload_to='article')

    class Meta:
        db_table = 'article'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    desc = models.CharField(max_length=150)
    key = models.ManyToManyField(Article)

    class Meta:
        db_table = 'category'