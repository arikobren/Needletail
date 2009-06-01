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
                    return render_to_response('bandPage.html', {'user': user})
                    
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
            
            #save members
            user   = User.objects.create_user(username     = cd['username'  ],
                                              password     = cd['password'  ],
                                              email        = cd['email'     ],)
            
            user.is_staff     = False
            #user.is_active    = False
            user.is_superuser = False
            user.save()
            
            #send confirmation email
#            send_mail('Needletail is the shit',
#                      'You are fucking registered',
#                      'ariel.kobren@tufts.edu',
#                      [user.email],
#                      fail_silently = False)

            return HttpResponseRedirect('/Success/')

    else:
        form = NewBandForm()                       #form has not been submitted
    return render_to_response('newBandForm.html', {'form': form})


def new_band_success(request):
    return render_to_response('createSuccess.html')


def band_page(request):
    name = request.user.get_full_name()
    return render_to_response('bandPage.html', {'name': name})



############BACKUP from 5.28.09################
#def new_band(request):
 #   if request.method == 'POST':                 #if form has been submitted
  #      form = NewBandForm(request.POST)
   #     if form.is_valid():                       
    #        cd = form.cleaned_data
     #       
      #      new_band = Band(name = cd['band_name'])
       #     new_band.save()
        #    
         #   #save members
          #  member   = Band_Member(first_name = cd['first_name'],
          #                         last_name  = cd['last_name' ],
          #                         username   = cd['username'  ],
          #                         password   = cd['password'  ],
          #                         email      = cd['email'     ])
          #
            
#            member.save()
 #           member.groups.add(new_band)        #add the band that they are 
  #                                                #part of to Band_Member
   #         
    #        
     #       return HttpResponseRedirect('/Success/')
#
 #   else:
  #      form = NewBandForm()                       #form has not been submitted
   # return render_to_response('newBandForm.html', {'form': form})
