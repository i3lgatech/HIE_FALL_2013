from django.conf.urls import patterns, include, url
from django.contrib import admin
from activityapp import shane, vik

admin.autodiscover()

urlpatterns = patterns(
	#url(r'^putactivity/'
	#url(r'^admin/', include(admin.site.url))
  # url(r'^', include(router.urls)),
   #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # Examples:
    # url(r'^$', 'activity.views.home', name='home'),
    # url(r'^activity/', include('activity.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^addActivity/', shane.addActivity, name='addactivity'),
    url(r'^addSteps/', shane.addSteps, name='addSteps'),
    url(r'^getReport/', vik.getReport, name='getReport'),
    url(r'^sendAlert/', vik.sendAlert, name='sendAlert'),
    url(r'^sendReport/', vik.sendReport, name='sendReport')

)
