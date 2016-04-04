from django.db import models

# Create your models here.



class Author(models.Model):
    first=models.CharField(max_length=50)
    last=models.CharField(max_length=50)
    middle=models.CharField(max_length=50)
    def __unicode__(self):
        return self.last

class Tag(models.Model):
    name=models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Affiliation(models.Model):
    name=models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Article(models.Model):
    title=models.CharField(max_length=300)
    abstract=models.TextField()
    pub_date=models.DateField()
    authors=models.ManyToManyField(Author)
    tags=models.ManyToManyField(Tag)
    affiliations=models.ManyToManyField(Affiliation)
    link=models.CharField(max_length=200)
    def __unicode__(self):
        return self.title
