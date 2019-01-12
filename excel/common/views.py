from django.http import HttpResponse
from django.shortcuts import render

from common.captcha import Captcha
from common.utils import gen_captcha_text





def captcha(request):
    code_text = gen_captcha_text()
    code_bytes = Captcha.instance().generate(code_text)
    return HttpResponse(code_bytes, content_type='image/png')