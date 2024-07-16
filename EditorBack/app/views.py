from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from app.models import User
from app.utils import create_token
from app import utils
import json
from PIL import Image
import os
from django.conf import settings
# Create your views here.

# erniebot.api_type = 'aistudio'
# erniebot.access_token = 'b3d27cfee042938a09a088dfd302180c3467118f'

languageNote = """
    注意，你应该先判断一下这句话是中文还是英文，如果是中文，请给我返回中文的内容，
    如果是英文，请给我返回英文内容，只需要返回内容即可，不需要告知我是中文还是英文：
"""

formatNote = """
    注意，你生成的文本要符合相应的排版，如标题类型、列表、缩进、换行等，并且能够在 tiptap 编辑器中渲染（markdown形式）：
"""

@csrf_exempt
def signUp(request):
    # 注册
    if request.method == "POST":
        data = json.loads(request.body)
        account = data.get("account")
        password = data.get("password")
        print(account, password)

        if User.objects.filter(account=account).exists():
            return JsonResponse({"status": False, 'etype': 1, "error": "账号已存在"})

        hashed_password = make_password(password)
        user = User(name="user" + account, account=account, password=hashed_password)
        user.save()

        # request.session["user_info"] = {"id": user.id, "name": user.name}
        # request.session.set_expiry(60 * 60 * 3)
        params = {
            "status": True,
            "message": "注册成功",
            "account": user.account,
            "token": create_token(user.account),
        }
        return JsonResponse(params)
    return JsonResponse({"status": False, "etype": 0, "error": "请求方法错误"})

@csrf_exempt
def signIn(request):
    # 登录
    if request.method == "POST":
        data = json.loads(request.body)
        account = data.get("account")
        password = data.get("password")
        print(account, password)

        if not User.objects.filter(account=account).exists():
            return JsonResponse({"status": False, "etype": 1, "error": "账号不存在"})

        user = User.objects.get(account=account)
        if check_password(password, user.password):
            # request.session["user_info"] = {"id": user.id, "name": user.name}
            # request.session.set_expiry(60 * 60 * 3)
            params = {
                "status": True,
                "message": "登录成功",
                "account": user.account,
                "token": create_token(user.account),
            }
            return JsonResponse(params)
        else:
            return JsonResponse({"status": False, "etype": 2, "error": "密码错误"})
    return JsonResponse({"status": False, "etype": 0, "error": "请求方法错误"})

@csrf_exempt
def getUserProfile(request):
    if request.method == "POST":
        account = request.META.get('HTTP_ACCOUNT')
        user = User.objects.get(account=account)
        params = {
            "status": True,
            "account": account,
            "accessToken": user.accessToken,
        }
        return JsonResponse(params)
    return JsonResponse({"status": False, "etype": 0, "error": "请求方法错误"})


@csrf_exempt
def setAccessToken(request):
    if request.method == "POST":
        account = request.META.get('HTTP_ACCOUNT')
        data = json.loads(request.body)
        access_token = data.get('accessToken')

        user = User.objects.get(account=account)
        user.accessToken = access_token
        user.save()

        params = {
            "status": True,
            "message": "成功设置访问令牌",
        }
        return JsonResponse(params)
    return JsonResponse({"status": False, "etype": 0, "error": "请求方法错误"})\

@csrf_exempt
def modifyPassword(request):
    if request.method == "POST":
        data = json.loads(request.body)
        account = request.META.get('HTTP_ACCOUNT')
        old_password = data.get("oldPassword")
        new_password = data.get("newPassword")
        print(old_password, new_password)

        if not User.objects.filter(account=account).exists():
            return JsonResponse({"status": False, "etype": 1, "error": "账号不存在"})

        user = User.objects.get(account=account)
        if check_password(old_password, user.password):
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            print(hashed_password)
            params = {
                "status": True,
                "message": "成功修改密码",
            }
            return JsonResponse(params)
        else:
            return JsonResponse({"status": False, "etype": 2, "error": "密码错误"})
    return JsonResponse({"status": False, "etype": 0, "error": "请求方法错误"})



@csrf_exempt
def translate(request):
    if request.method == "POST":
        prompt = '''
            请帮我翻译以下内容，在翻译之前，想先判断一下这个内容是不是中文，
            如果是中文，则翻译问英文，如果是其他语言，则需要翻译为中文，注意，
            你只需要返回翻译的结果，不需要对此进行任何解释，不需要除了翻译结果以外的其他任何内容：
        '''
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
        # return JsonResponse({"status": True, "answer": "AI的答案"})
    return JsonResponse({"status": False, "error": "请求方法错误"})


@csrf_exempt
def abstract(request):
    if request.method == "POST":
        prompt = "请帮我总结以下内容(就是做摘要)，并直接返回总结的结果，" + languageNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def decorate(request):
    if request.method == "POST":
        prompt = "请帮我修饰以下内容，并直接返回修饰后的结果，" + languageNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def continueWrite(request):
    if request.method == "POST":
        prompt = "请帮我续写以上内容，发挥你的想象力，添加更多细节，并直接返回续写的结果，" + languageNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def rewrite(request):
    if request.method == "POST":
        prompt = "请帮我检查下面这段话的语法和内容，修改其中的病句（或者不合适的地方），并直接返回改正后的结果，" + languageNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def improveWrite(request):
    if request.method == "POST":
        prompt = "请帮我改进以下内容，对其进行优化，并直接返回改进后的结果，" + languageNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def summarize(request):
    if request.method == "POST":
        prompt = "请帮我总结以下内容，并直接返回总结的结果" + languageNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def analysis(request):
    if request.method == "POST":
        prompt = "请帮我分析以下内容（依照内容选择一个最合适的角度进行分析即可），并直接返回分析的结果" + languageNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def useOCR(request):
    if request.method == "POST":
        file_path = utils.saveFile(request)
        return JsonResponse({"status": True, "answer": utils.handleOCR(file_path)})
        # return JsonResponse({"status": True, "answer": "ok"})
    return JsonResponse({"status": False, "error": "请求方法错误"})


@csrf_exempt
def voiceRecognise(request):
    if request.method == "POST":
        file_path = utils.saveFile(request)
        return JsonResponse({"status": True, "answer": utils.handleVoice(file_path)})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def videoRecognise(request):
    if request.method == "POST":
        file_path = utils.saveFile(request)
        print(file_path)
        return JsonResponse({"status": True, "answer": utils.handleVidio(file_path)})
    return JsonResponse({"status": False, "error": "请求方法错误"})


@csrf_exempt
def projectDocument(request):
    if request.method == "POST":
        prompt = """
            假设你是一个大学生，正在参加学校组织的大学生创新创业项目，下面就是关于项目的简介，请你根据下面的内容，
            写一份详细的项目申请书文档，内容包括：项目背景与意义、项目目标与预期成果、研究内容与方法（理论依据）、
            创新点、技术路线与实施计划等，
        """ + formatNote
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})

@csrf_exempt
def codeEdit(request):
    if request.method == "POST":
        print(request.POST.get("question"))
        prompt = """
               假设你是一个程序员，请根据下面的需求和语言写代码，如果用户没有指定使用的语言，就写Python代码，
               可以在关键代码和重要变量（如参数等）的旁边加上注释，将代码写在markdown的代码块中，
               除了代码块不要给我任何其他的内容，将所有代码都生成完毕再将结果返回给我
           """
        response = utils.getAIResponse(request, prompt)
        return JsonResponse({"status": True, "answer": response.get_result()})
    return JsonResponse({"status": False, "error": "请求方法错误"})