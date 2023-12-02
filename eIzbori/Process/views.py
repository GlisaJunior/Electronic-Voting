from django.shortcuts import render
from Process.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime
import csv
from .forms import CSVUploadForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
# Create your views here.



def login_view(request):


    if request.method == 'POST':
        #does this work?
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email, password = password)
        next_url = request.GET.get('next')

        if user is not None:
            login(request,user)
            
            if next_url:
                print(next_url)
                return redirect(next_url)
            else:
                return HttpResponse("bruh.")
    else:
        return render(request,"login.html")

@login_required
def voting_view(request,key):
    #following if statement only matters AFTER the ballot is filled.



        if request.method == 'POST':
 
            # this IF statement checks if the current user has voted already for the current phase, and checks if there is an active election.
            currentuser = request.user
            user = key_of.objects.get(key = key).user
            if user == currentuser:
                if  user.votestatus == election.objects.latest('id').Phase and election.objects.latest('id').Phase != 2 :
                    votees = [value for key, value in request.POST.items() if key.startswith('checkbox')]
                    if len(votees) > 5:
                        request = HttpResponse("no.")
                        return request
                    elif len(votees) < 1:
                        request = HttpResponse("Nuh-uh.")
                        return request
                    else:
                        for item in votees:
                            usermodel = get_user_model()
                            newballot = ballot()
                            newballot.votes = usermodel.objects.get(id = item)
                            newballot.votetype = election.objects.latest('id').Phase
                            newballot.election = election.objects.latest('id')
                            newballot.save()
                        
                        user.votestatus += 1
                        user.save()

                        # put email system here that confirms that someone successfully voted.
                        response = HttpResponse("Successfully voted.")
                        return response
                else:
                    response = HttpResponse("You have already voted for the current step of the election.")
                    return response
            #TODO make a success html to post to after voting.
            else:
                response = HttpResponse("You are trying to vote on someone elses ballot.")
                return response


        #default method when loading the page for the first time, therefore this will usually happen when loading the page.
        if request.method == 'GET':

            currentuser = request.user
            if currentuser == key_of.objects.get(key = key).user:
                if election.objects.latest('id').Phase == 0:
                    #pulling info from database here v
                    user = key_of.objects.get(key = key).user
                    local_cent = is_within.objects.get(user = user).local_center
                    voteeslist = list(is_within.objects.filter(local_center = local_cent))
                    votees = []

                    for object in voteeslist:
                        votees.append(object.user)
                    
                    #storing the data in a easily accessible format for putting it into html.
                    voteesdict = {}
                    for object in votees:
                        dict = {}
                        name = f"{object.first_name} {object.last_name}"
                        id = object.id
                        dict['name'] = name
                        dict['id'] = id
                        voteesdict[f"votee_{len(voteesdict)}"] = dict


                    #KEEP IN MIND: defining the entire name as "name" here, dont use first_name,last_name, at least not in html.
                    currentuser = { 'local_center':local_cent.name, 'name':f"{user.first_name} {user.last_name}", 'licence' : user.licence}
                    
                    context = { 'currentuser': currentuser , 'key':key, 'votees' : voteesdict }
                    # user > user object
                    # votees > list of user dictionaries pulled from database
                    # key > key that is gotten from the url.
                    return render(request, 'ballot.html', context = context)
            
                if election.objects.latest('id').Phase == 1:
                    user = key_of.objects.get(key = key).user
                    local_cent = is_within.objects.get(user = user).local_center
                    localcentlist = list(is_within.objects.filter(local_center = local_cent))
                    candidates_in_localcent = []
                    for item in localcentlist:
                        candidates_in_localcent.append(item.user)
                    #this gets all the ballots that have someone from the local center of the current user, which is a necessary step to count all the votes per candidate. 
                    ballots = ballot.objects.filter(votes__in = candidates_in_localcent)

                    candidate_dict = {}

                    # to be later ordered in html with {% regroup %}
                    for object in candidates_in_localcent:
                        candidate_dict[object] = ballot.objects.filter(votes = object).count()

                    currentuser = { 'local_center':local_cent.name, 'name':f"{user.first_name} {user.last_name}", 'licence' : user.licence}

                    context = {'currentuser':currentuser, 'key': key, 'votees' : candidate_dict}
                        #TODO ...make ballot2.
                    return render(request, 'ballot2.html', context = context)
                
                if election.objects.latest('id').phase == 2:
                    response = HttpResponse("There is no election going on right now.")
                    return response
            else:
                response = HttpResponse("You are trying to access the wrong ballot.")
                return response

@login_required
def Commission_view(request):
    #TODO make the displayed current election results based on the current phase of the election. ex: if vote phase is 1, filter all votes by vote phase 1 and only display those results.
    if request.method == "POST":
        #AKA if you selected an election, display that election's votes.
        
        #TODO add a filter for the voting section of the election instead of pulling all of the ballots. maybe? add both types of votes into the display.
        if request.POST.get("election"):
            electionInstance = election.objects.get(id = request.POST["election"]) 
            date = electionInstance.date
            votes = {}
            regions = [item for item in regional_center.objects.all()]
            for region in regions:
                votes[region] = {}
                locals = [item for item in region.local_center_set.all()]
                for local in locals:
                    votes[region][local] = {}
                    Sample = [item for item in local.is_within_set.all()]
                    Historical_is_within= []
                    for item in Sample:
                        Historical_is_within.append(item.history.as_of(date))
                    members = [ item.user for item in Historical_is_within ]
                    for member in members:
                        # Ballot model got changed so it keeps track of which election it is tied to.
                        count = ballot.objects.filter(votes = member,election = electionInstance).count()
                        votes[region][local][member] = count
            elections = [item for item in election.objects.all()]
            context = {'votes' : votes, 'elections' : elections}
            return render(request, 'commission.html', context = context)
        
        #TODO different if statements based on which phase you are in.
        elif request.POST.get("advance"):
            if request.POST.get("name_of_election"):
                name = request.POST["name_of_election"]
                new_election = election()
                new_election.name_of_election = name
                new_election.date = datetime.now()
                new_election.Phase = 0
                new_election.save()
                usermodel = get_user_model()
                for user in usermodel.objects.all():
                    user.votestatus = 0
                    user.save()
                return redirect(Commission_view)
            #need to determine whether i should set every users votestatus to the current election phase, after changing election phase. can people vote if they didnt candidate anyone?
            #TODO make a function that will generate a new key for each user after each voting step, and then email that information again.
            elif election.objects.latest('id').Phase != 2:
                elec = election.objects.latest('id')
                elec.Phase += 1
                elec.save()
                return redirect(Commission_view)
            else:
                return HttpResponse("Does not return name of election, but current phase is 2.")
        else:
            return redirect(Commission_view)
    if request.method == "GET":
        votes = {}
        regions = list(regional_center.objects.all())
        for region in regions:
            votes[region] = {}
            locals = list(region.local_center_set.all())
            for local in locals:
                votes[region][local] = {}
                iswithinset = list(local.is_within_set.all())
                members = []
                for item in iswithinset:
                    members.append(item.user)
                    for member in members:
                        count = ballot.objects.filter(votes = member, election = election.objects.latest('id')).count()
                        votes[region][local][member] = count
        elections = [item for item in election.objects.all()]
        latestelection = election.objects.latest('id')
        context = {'votes' : votes,'elections' : elections, 'latestelection' : latestelection}
        return render(request, 'commission.html', context = context )
                #TODO make commision page.

def make_random_password(
        self,
        length=10,
        allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789",
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        
        return get_random_string(length, allowed_chars)

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            reader = csv.reader(csv_file.read().decode("utf-8").splitlines())
            next(reader)

            for row in reader:
                first_name = row[0]
                last_name = row[1]
                email = row[2]
                licence = row[5]
                
                if not CustomUser.objects.filter(licence=licence).exists():
                    instance = CustomUser(licence=licence, first_name=first_name, last_name=last_name, email=email)
                    instance.save()
            
            return render(request, 'success.html', {'redirect_delay': 3000})
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})

def send_email_to_users(subject, message):
    # Get all users from the database
    users = CustomUser.objects.all()

    # Extract the email addresses of the users
    recipient_list = [user.email for user in users]

    # Send the email using Django's send_mail function
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


def create_new_election(request):
    if request.method == 'POST':
        # Process the form data and create the new election

        # Send email to all users
        subject = 'New Election Created'
        message = 'Your credentials will be sent shortly'
        send_email_to_users(subject, message)

        # Redirect or render a success message
        return render(request, 'success.html', {'redirect_delay': 3000})

    # Handle GET request for the create new election page
    return render(request, 'create_election.html')
