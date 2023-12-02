import csv,sys, os, django,datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eIzbori.settings')
django.setup()
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Process.models import *

# user = get_user_model()
# list = list(user.objects.all())
# print(list)
# for item in list:
#     id = item.id
#     usermodel = get_user_model()
#     newballot = ballot()
#     newballot.votes = usermodel.objects.get(id = id)
#     newballot.votetype = 0
#     newballot.save()
elections = election.objects.latest('id')
date = elections.date
votes = {}
regions = [item for item in regional_center.objects.all()]
for region in regions:
    votes[region] = {}
    locals = [item for item in region.local_center_set.all()]
    for local in locals:
        votes[region][local] = {}
        Sample = [item for item in local.is_within_set.all()]
        HistoricalSet= []
        for item in Sample:
            HistoricalSet.append(item.history.as_of(date))
        members = [ item.user for item in HistoricalSet ]
        for member in members:
            count = ballot.objects.filter(votes = member,election = 2).count()
            votes[region][local][member] = count
print(votes)

# elections = [item for item in election.objects.all()]
# print(elections)
# elec = election()
# elec.Phase = 1
# elec.date = datetime.datetime.now().date()
# elec.name_of_election = "test"
# elec.save()


# votes = {}
# regions = list(regional_center.objects.all())
# for region in regions:
#    votes[region] = {}
#    locals = list(region.local_center_set.all())
#    for local in locals:
#       votes[region][local] = {}
#       iswithinset = list(local.is_within_set.all())
#       members = []
#       for item in iswithinset:
#          members.append(item.user)
#       for member in members:
#             count = ballot.objects.filter(votes = member).count()
#             votes[region][local][member] = count
# print(votes)


            
# user = CustomUser.objects.get(first_name = "Pat")
# print(is_within.objects.get(user = user).local_center.name)

# instance = is_within.objects.get(user=user)
# snapshot = instance.history.as_of(datetime.datetime.now())
# print(snapshot)

# fields = snapshot._meta.fields


# # Print field names and their corresponding values
# for field in fields:
#     field_name = field.name
#     field_value = getattr(snapshot, field_name)
#     print(f"{field_name}: {field_value}")



# iswith = is_within.objects.get(user = user)
# loc = iswith.local_center
# votees = is_within.objects.get(local_center = loc)
# print(votees.id)
# key = 2
# user = key_of.objects.get(key = key).user
# local_cent = is_within.objects.get(user = user).local_center
# voteeslist = list(is_within.objects.filter(local_center = local_cent))
# votees = []
# for object in voteeslist:
#     votees.append(object.user)
# print(user)

# voteesdict = {}
# for object in votees:
#     dict = {}
#     name = f"{object.first_name} {object.last_name}"
#     id = object.id
#     dict['name'] = name
#     dict['id'] = id
#     voteesdict[f"votee {len(voteesdict)}"] = dict
# print(user)
# currentuser = { 'local_center':local_cent.name, 'name':f"{user.first_name} {user.last_name}", 'licence' : user.licence}

# context = { 'currentuser': currentuser , 'votees' : voteesdict, 'key':key }
# print(context)