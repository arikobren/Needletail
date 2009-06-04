from django.shortcuts import render_to_response
from django.http      import HttpResponse
from django.http      import HttpResponseRedirect
from django.contrib   import auth
from django.core.mail import send_mail

from django.contrib.auth.models import User

from needletail.login.models import Band
from needletail.login.models import User_Profile

from needletail.login.forms  import NewBandForm
from needletail.login.forms  import LoginForm
from needletail.login.forms  import CreateWebsiteForm


def home(request):
    bands = Band.objects.all()
    if request.method == 'POST':                  #form has been submitted
                                                  #make sure user is browsing
        if request.session.test_cookie_worked():  #with cookies enabled
            request.session.delete_test_cookie()
            form = LoginForm(request.POST)
            if form.is_valid():
                cd   = form.cleaned_data
                user = auth.authenticate(username = cd['username'],
                                         password = cd['password'])

                if user is not None:
                    auth.login(request, user)
#                    website = '/bands/' + user.username
                    return HttpResponseRedirect('/MyBands/')
                    
        else:
            return HttpResponse("Please enable cookies and try again")

    else:
        form = LoginForm()                        #form has not been submitted

        request.session.set_test_cookie()         #ensure the user is browsing
                                                  #with cookies enabled
    return render_to_response('home.html', {'bands':bands, 'form':form})


def new_band(request):
    if request.method == 'POST':                 #if form has been submitted
        form = NewBandForm(request.POST)
        if form.is_valid():                       
            cd = form.cleaned_data
            new_band = Band(name = cd['band_name'])
            new_band.save()
            
            #save band in session variable
            request.session['band_id'] = new_band.id

            #save members
            user   = User.objects.create_user(username     = cd['username'  ],
                                              password     = cd['password'  ],
                                              email        = cd['email'     ],)
            
            user.is_staff     = False
            #user.is_active    = False
            user.is_superuser = False
            user.save()


            user_pro = User_Profile(user  = user)
            user_pro.save()
            user_pro.bands.add(new_band)
            
            
            #send confirmation email
#            send_mail('Needletail is the shit',
#                      'You are fucking registered',
#                      'ariel.kobren@tufts.edu',
#                      [user.email],
#                      fail_silently = False)

            return HttpResponseRedirect('/Success')

    else:
        form = NewBandForm()                       #form has not been submitted
    return render_to_response('newBandForm.html', {'form': form})


def create_website(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = CreateWebsiteForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if request.session['band_id'] is not None:
                    band = Band.objects.get(id = request.session['band_id'])
                    band.web_ext = cd['web_ext']
                    website = "http://127.0.0.1:8000/bands/" + cd['web_ext']
                    return HttpResponseRedirect(website)
        else:
            form = CreateWebsiteForm()
    else:
        return HttpResponseRedirect('/')

    return render_to_response('createWebsite.html', {'form': form})
                
def new_band_success(request):
    return render_to_response('createSuccess.html')


def choose_band(request):
    if request.user.is_authenticated():
        user_pro = User_Profile.objects.get(user = request.user)
        bands    = user_pro.bands.all()
        return render_to_response('myBands.html', {'bands': bands})
    else:
        return HttpResponseRedirect('/')

def band_page(request):
    if request.user.is_authenticated():
        username     = request.user.username
        #band         = Band.objects.get(id = request.session['band_id'])
        #name         = band.name
        band         = request.POST['band']
        return render_to_response('bandPage.html', {'username': username, 
                                                    'band'    : band})
    else:
        return HttpResponseRedirect('/')



