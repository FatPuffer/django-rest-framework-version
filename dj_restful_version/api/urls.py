from django.conf.urls import url
from .views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<version>[v1|v2]+)/users/$', UsersView.as_view(), name='xxx'),
]
