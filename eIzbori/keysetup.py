import csv,sys, os, django,datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eIzbori.settings')
django.setup()
from django.conf import settings

from django.contrib.auth import get_user_model
from Process.models import *


user = get_user_model()
a = 1

userlist = list(user.objects.all())

print(userlist)
for item in userlist:
    keylist = key_of()
    keylist.key = a
    a+= 1
    keylist.user = item
    keylist.save()