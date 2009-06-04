from django.conf.urls.defaults import *
from needletail.login import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #(r'^login/$'   , views.login),                 # login page
    (r'^$'         , views.home),                  # home page        
    (r'^newBand/$' , views.new_band),              # create new band
    (r'^Success/$' , views.new_band_success),      # creation successful
    (r'^WebExt/$'  , views.create_website),        # choose your ext name 
    (r'^MyBands/$' , views.choose_band),           # choose band if multiple  
    (r'^bands/'    , views.band_page),             # upon successful login
    # Example:
    # (r'^needletail/', include('needletail.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
