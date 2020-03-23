## 一个基于 Socket 的 Web MVC 框架 

#### 实现功能

- **HTTP Sever**
  - 使用 **Socket API** 实现 **监听请求** 和 **发送响应**
  - 手写实现 **HTTP** 报文的 **解析**和**拼接**  
- **MVC 框架**
  - M：实现了基于 MySQL 的 **ORM**
  - V：使用 **Jinja2** 渲染模板提高开发效率同时使数据有序显示；使用模板继承实现前端界面的代码复用和风格统一
  - C：利用**Python 高阶函数** 和 **字典** 实现 **路由分发**，以**装饰器**形式实现权限验证
  - 前后端分离, 实现基于 **AJAX** 技术异步刷新的 **单页应用**
  - 实现用户管理，包括注册、登录、密码的摘要和加盐保护、**Session** 管理、**权限验证**
  - 支持对**CSRF**、**XSS** 等攻击的防御

主要功能展示

![image](https://github.com/HuangShaocong-sudo/mvc_framework/blob/master/mvc_framework_app.gif)

![image](https://github.com/HuangShaocong-sudo/mvc_framework/blob/master/framework_log.gif)