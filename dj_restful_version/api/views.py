from django.http import JsonResponse, HttpResponse
from rest_framework .views import APIView
from api.models import UserInfo, UserToken
from api.utils.permision import MyPermission
from api.utils.throttle import VisitThrottle

ORDER_DICT = {
    1: {
        'name': '女朋友',
        'age': 18,
        'gender': '女',
        'content': '....'
    },
    2: {
        'name': '男朋友',
        'age': 22,
        'gender': '男',
        'content': '....'
    },
}


def md5(user):
    import hashlib
    import time

    ctime = str(time.time())

    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


# from rest_framework.throttling import BaseThrottle
# import time
#
# VISIT_RECORD = {}
#
#
# class VisitThrottle(object):
#     """60s内只能访问3次"""
#
#     def __init__(self):
#         self.history = None
#
#     def allow_request(self, request, view):
#         # 1.获取用户IP
#         remote_addr = request.META.get('REMOTE_ADDR')
#         # 获取当前时间
#         ctime = time.time()
#         if remote_addr not in VISIT_RECORD:
#             # 利用时间记录访问次数
#             VISIT_RECORD[remote_addr] = [ctime,]
#             return True
#
#         # 获取历史访问记录列表
#         history = VISIT_RECORD.get(remote_addr)
#         self.history = history
#
#         # 如果当前时间减去60s还大于我们访问记录中的最早的数据，说明该数据是在距离60秒前的数据，则将其删除
#         # 同时将最新的时间数据插入在列表最左侧
#         # 此处目的：控制列表仅保留60s以内的数据
#         while history and history[-1] < ctime - 60:
#             # 删除60s以外的数据
#             history.pop()
#
#         # 如果列表长度小于3，则将新的访问数据加入列表
#         if len(history) < 3:
#             history.insert(0, ctime)
#             return True  # 表示可以继续访问
#         else:
#             return False  # 表示访问频率过高，被限制
#
#     def wait(self):
#         # 可以实现用户界面提示，提示用户还需要等待多久才能继续访问
#         ctime = time.time()
#         # 获取剩余限制时间
#         last_time = 60 - (ctime - self.history[-1])
#         return last_time


class AuthView(APIView):
    """
    用户登录认证
    """
    # 不需要认证的视图进行如下配置，覆盖全局认证即可
    authentication_classes = []
    # 不需要权限如下配置，覆盖全局配置即可
    permission_classes = []
    # 未登录用户遵循该节流模式
    throttle_classes = [VisitThrottle,]

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'

            # 为登录用户创建token
            token = md5(user)
            ret['token'] = token
            # 存在就更新，不存在则创建
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})
        except Exception as e:
            pass

        return JsonResponse(ret)


# class Authtication(object):
#     def authenticate(self, request):
#         token = request._request.GET.get('token')
#         token_obj = UserToken.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed('用户认证失败')
#         # 在rest framework内部会将整个两个字段赋值给request,以供认证操作使用
#         return (token_obj.user, token_obj)
#
#     def authenticate_header(self, request):
#         pass


class OrderView(APIView):
    """
    订单相关业务（SVIP才有权限查看）
    """
    def get(self, request, *args, **kwargs):
        # Todo: request.user 拿到的就是token_obj.user
        # Todo: request.auth 拿到的就是token_obj
        # token = request._request.GET.get('token')
        # if not token:
        #     return HttpResponse('用户未登录')

        ret = {'code': 1000, 'msg': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfoView(APIView):
    """
    个人中心（普通用户、VIP用户有权限）
    """
    # 使用该权限覆盖全局权限
    permission_classes = [MyPermission,]

    def get(self, request, *args, **kwargs):
        # self.dispatch()
        print(request.user)
        return HttpResponse('用户信息')

