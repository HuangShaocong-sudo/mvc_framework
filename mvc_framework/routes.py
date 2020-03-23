import json
import os
import uuid
from functools import wraps

from jinja2 import FileSystemLoader, Environment

from mvc_framework.utils import log
from demo_app.models.user import User
from demo_app.models.session import Session


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        u = Session.find_user(session_id=session_id)
        return u
    else:
        return User.guest()


csrf_tokens = {}


def new_csrf_token(request):
    u = current_user(request)
    if u is not None:
        token = str(uuid.uuid4())
        csrf_tokens[token] = u.id
        return token


def csrf_required(route_function):
    # csrf 防御装饰器
    def f(request):
        log('csrf_required', route_function)
        token = request.query['csrf_token']
        u = current_user(request)
        if token in csrf_tokens and csrf_tokens[token] == u.id:
            csrf_tokens.pop(token)
            return route_function(request)
        else:
            return error(request)
    return f


# noinspection PyUnusedLocal
def error(request):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    return b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'
    # return b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'.encode()


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=xxx
    """
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def redirect(url, result='', headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    if len(result) > 0:
        formatted_url = '{}?result={}'.format(
            url, result
        )
    else:
        formatted_url = url
    h = {
        'Location': formatted_url,
    }
    if isinstance(headers, dict):
        h.update(headers)

    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分，只是个重定向的响应
    # HTTP 1.1 302 ok
    # Location: /todo
    #
    r = response_with_headers(h, 302) + '\r\n'
    return r.encode()


def html_response(filename, **kwargs):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    body = JinjaTemplate.render(filename, **kwargs)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data):
    headers = {
        'Content-Type': 'application/json',
    }
    header = response_with_headers(headers)
    body = json.dumps(data, indent=2, ensure_ascii=False)
    r = header + '\r\n' + body
    return r.encode()


def login_required(route_function):
    """
    response = login_required(route_edit)
    response(request)
    """

    def f(request):
        log('login_required', route_function)
        u = current_user(request)
        if u.is_guest():
            log('login_required is_guest', u)
            return redirect('/login/view')
        else:
            return route_function(request)

    return f


def _initialized_environment():
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(os.path.join('demo_app', 'templates'))
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class JinjaTemplate:
    env = _initialized_environment()

    @classmethod
    def render(cls, filename, **kwargs):
        t = cls.env.get_template(filename)
        return t.render(**kwargs)
