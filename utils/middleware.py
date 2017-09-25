# 判断用户是否登录中间件
class UrlPathRrecordMiddleware(object):
    """记录上一次访问的地址中间件"""
    # 以下地址和 ajax 请求地址不需要记录
    exclude_path = ['/user/login/', '/user/logout/', '/user/register/']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path not in UrlPathRrecordMiddleware.exclude_path and not request.is_ajax():
            # 将地址记录到 session 中
            request.session['pre_url_path'] = request.path
