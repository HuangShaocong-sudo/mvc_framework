from demo_app import all_route_dict
from mvc_framework.server import configured_wsgi_app

# app 是一个配置好的函数(gunicorn 接口变量) wsgi_app(environ, start_response)
app = configured_wsgi_app(all_route_dict())
