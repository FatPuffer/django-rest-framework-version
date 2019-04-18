# django-rest-framework-version

# 1. 版本

    a. URL中通过GET传参（）

      自定义：?version=v2
      
         class ParamVersion(object):

            def determine_version(self, request, *args, **kwargs):
                
                version = request.query_params.get('version')
                
                return version


        class UsersView(APIView):

            versioning_class = ParamVersion

            def get(self, request, *args, **kwargs):
                
                print(request.version)  # 获取版本
                
                return HttpResponse('用户列表')
        
    b. 全局配置
        
        访问形式：?version=v1
        
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
            
            
            
