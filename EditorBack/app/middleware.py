from app.utils import check_token
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# 白名单，表示请求里面的路由时不验证登录信息
API_WHITELIST = ["/sign-in/", "/sign-up/"]

class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # print(request.path)
        if request.path not in API_WHITELIST:
            # 从请求头中获取 username 和 token
            account = request.META.get('HTTP_ACCOUNT')
            token = request.META.get('HTTP_TOKEN')
            # print(account, token)
            if account is None or token is None:
                return JsonResponse({'errno': 100001, 'msg': "未查询到登录信息"})
            else:
                # 调用 check_token 函数验证
                if check_token(account, token):
                    pass
                else:
                    return JsonResponse({'errno': 100002,
                                         'msg': "登录信息错误或已过期"})