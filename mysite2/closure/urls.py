from django.conf.urls import url

from . import views


urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),

    #url(r'^/tree/$', views.index_tree, name='index_tree'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/ancestor/$', views.detail_ancestor, name='detail_ancestor'),
    url(r'^(?P<closure_id>[0-9]+)/tree/$', views.detail_tree, name='detail_tree'),

    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
