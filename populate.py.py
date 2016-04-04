import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prepubmed.settings')

import django
django.setup()

from papers.models import article

f=open(r'C:\Users\Jordan Anaya\Desktop\prepubmed\peerj\abstracts.txt')
abstracts=eval(f.read())

##article.objects.create(abstract=abstracts[1032])

