from django.contrib import admin
from .models import Article
from .models import Tag
from .models import Author
from .models import Affiliation


# Register your models here.



admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Affiliation)
