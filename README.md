# django-rest-framework-version

# 1. 版本

    a. URL中通过GET传参（）

      自定义：http://127.0.0.1:8000/api/users/?version=v1
      
         class ParamVersion(object):

            def determine_version(self, request, *args, **kwargs):
                
                version = request.query_params.get('version')
                
                return version


        class UsersView(APIView):

            versioning_class = ParamVersion

            def get(self, request, *args, **kwargs):
                
                print(request.version)  # 获取版本
                
                return HttpResponse('用户列表')
        
    b. URL中通过GET传参（）
        
        全局配置访问形式：http://127.0.0.1:8000/api/users/?version=v1
        
        settings.py
            
            REST_FRAMEWORK = {
                "DEFAULT_VERSION": "v1",  # 默认版本
                "ALLOWED_VERSIONS": ["v1", "v2"],  # 允许版本
                "VERSION_PARAM": "version"  # 查询字符串
            }
            
         views.py
         
            from django.http import JsonResponse, HttpResponse
            from rest_framework .views import APIView
            from rest_framework.versioning import QueryParameterVersioning
            
            
            class UsersView(APIView):

                versioning_class = QueryParameterVersioning

                def get(self, request, *args, **kwargs):
                
                    print(request.version)  # 获取版本
                    
                    return HttpResponse('用户列表')
            
    c. URL路由分发形式（推荐使用）
    
        访问形式：http://127.0.0.1:8000/api/v1/users/
    
        settings.py
        
            REST_FRAMEWORK = {
            
                # 全局版本控制
                "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
            }
            
        views.py
        
            from django.http import JsonResponse, HttpResponse
            from rest_framework .views import APIView
            
            class UsersView(APIView):

                def get(self, request, *args, **kwargs):
                
                    print(request.version)  # 直接获取版本
                    
                    return HttpResponse('用户列表')
            
        总 urls.py
            
            from django.conf.urls import url, include

            urlpatterns = [
                url(r'^api/', include('api.urls'))
            ]
            
        urls.py
        
            from django.conf.urls import url
            from .views import UsersView

            urlpatterns = [
                url(r'^(?P<version>[v1|v2]+)/users/$', UsersView.as_view()),
            ]

            
            
