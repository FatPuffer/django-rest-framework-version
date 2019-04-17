# django-rest-framework-version

# 1. 版本

    a. URL中通过GET传参（）

      自定义：http://127.0.0.1:8000/api/users/?version=v2
      
         class ParamVersion(object):

            def determine_version(self, request, *args, **kwargs):
                
                version = request.query_params.get('version')
                
                return version


        class UsersView(APIView):

            versioning_class = ParamVersion

            def get(self, request, *args, **kwargs):
                
                print(request.version)
                
                return HttpResponse('用户列表')
