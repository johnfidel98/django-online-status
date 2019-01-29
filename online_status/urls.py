from django.conf.urls import url
from online_status.views import users  # , users_json

urlpatterns = [
    url(r'^$', users, name='online_users'),
    # url(r'^json/$', users_json, name='online_users_json'),  # To review
]
