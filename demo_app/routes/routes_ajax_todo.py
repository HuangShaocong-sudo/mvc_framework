from demo_app.models.todo import Todo
from mvc_framework.routes import (
    current_user,
    html_response, json_response)
from mvc_framework.utils import log


def index(request):
    u = current_user(request)
    return html_response('ajax_todo_index.html')


def all(request):
    ts = [t.__dict__ for t in Todo.all()]
    return json_response(ts)


def add(request):
    form = request.json()
    u = current_user(request)

    Todo.add(form, u.id)
    data = dict(
        message='成功添加 todo'
    )
    return json_response(data)


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/ajax/todo/index': index,
        '/ajax/todo/all': all,
        '/ajax/todo/add': add,
    }
    return d
