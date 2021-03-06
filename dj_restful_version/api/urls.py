from django.conf.urls import url
from .views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<version>[v1|v2]+)/users/$', UsersView.as_view(), name='xxx'),
    url(r'^(?P<version>[v1|v2]+)/parser/$', ParserView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/roles/$', RoleView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo/$', UserInfoView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$', GroupView.as_view(), name='gp'),
    url(r'^(?P<version>[v1|v2]+)/usergroup/$', UserGroupView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/pageer1/$', Pager1View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/v1/$', View1View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/v2/$', View2View.as_view({'get': 'list'})),
    url(r'^(?P<version>[v1|v2]+)/v3/$', View3View.as_view({'get': 'list', 'post': 'create'})),
    url(r'^(?P<version>[v1|v2]+)/v3/(?P<pk>\d+)$', View3View.as_view({'get': 'retrieve', 'put': 'update',
                                                                      'patch': 'partial_update',
                                                                      'delete': 'destroy'})),
]

