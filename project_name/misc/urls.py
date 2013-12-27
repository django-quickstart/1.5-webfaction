from django.conf.urls import patterns, include, url

urlpatterns = patterns('{{ project_name }}.misc.views',
  url(r'^$', 'home', name='home'),
)
