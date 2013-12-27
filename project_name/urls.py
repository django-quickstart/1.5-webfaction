from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns("")

# Admin URLs
from django.contrib import admin
admin.autodiscover()
urlpatterns += patterns("", 
  url(r'^admin/', include(admin.site.urls)),
)


#Custom URLS
urlpatterns += patterns('',
  #Account management, baked in  
  url(r'^accounts/', include('allauth.urls')),

  #Grabs homepage
  url(r'^', include('{{ project_name }}.misc.urls')),
)

# Static and Media URLS
if settings.SERVE_MEDIA_LOCALLY:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)