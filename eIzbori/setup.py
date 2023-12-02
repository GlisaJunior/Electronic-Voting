import csv,sys, os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eIzbori.settings')
django.setup()
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Process.models import *


project_dir = "eIzbori/Process"
sys.path.append(project_dir)


file = "Resources/Sheet3.csv"
data = csv.reader(open(file),delimiter =",")
finlist = {}
for row in data:
    if row[0] != "first_name":
        if row[3]  not in finlist:
            finlist[row[3]] = []
        if row[4] not in finlist[row[3]]:
            finlist[row[3]].append(row[4])

# populates database with local and regional centers and links them together
list = list(dict.keys(finlist))
for item in list:
    reg = regional_center()
    reg.name = item
    reg.save()
    for center in finlist[item]:
        loc = local_center()
        loc.name = center
        loc.regional_center = reg
        loc.save()
     
     
#fills is_within table  with user and local center id's upon user generation.
data = csv.reader(open(file),delimiter =",")
Usermodel = get_user_model()
for row in data:
    if row[0] != "first_name":
        model = Usermodel()
        model.first_name = row[0]
        model.last_name = row[1]
        model.set_password(raw_password=row[5])
        model.email = row[2]
        model.licence = row[5]
        model.votestatus = 2
        model.save()
        
        regionalcent = regional_center.objects.get(name = row[3])
        localcent = regionalcent.local_center_set.get(name = row[4])
        isw = is_within()
        isw.user = model
        print(localcent)
        isw.local_center = localcent
        isw.save()

