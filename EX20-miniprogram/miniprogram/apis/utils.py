from django.conf import settings


def get_wechat_login_code_url(code):
    """
    https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
    """
    return f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.MINIPROGRAM_CONFIG['APPID']}&secret={settings.MINIPROGRAM_CONFIG['SECRET']}&js_code={code}&grant_type=authorization_code"
