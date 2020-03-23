from demo_app import all_route_dict
from mvc_framework.server import run

if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='localhost',
        port=3000,
    )
    # run(host='0.0.0.0', port=80, route=all_route_dict())  # 在服务器上需设置为host='0.0.0.0', port=80
    run(**config, route=all_route_dict())  # 在服务器上需设置为host='0.0.0.0', port=80
