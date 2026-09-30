# skylark-yun-web

Vue 2 + Django 在线课程学习项目，使用 MySQL、Redis 和 Celery，适合本地开发与学习。

## 使用方式

### 启动项目

安装并启动 Docker Desktop（Linux 容器），在项目根目录执行：

```powershell
git clone git@github.com:China6577/skylark-yun-web.git
cd skylark-yun-web
Copy-Item .env.example .env
```

编辑 `.env`，设置自己的 `MYSQL_ROOT_PASSWORD`、`MYSQL_PASSWORD` 和 `DJANGO_SECRET_KEY`；签名密钥使用较长的随机字符串。短信配置为可选项，使用短信注册时才需要填写腾讯云凭据、应用 ID、签名和模板 ID。

```powershell
docker compose config --quiet
docker compose up -d --build
docker compose ps
```

启动时自动执行数据库迁移。首次运行需要下载镜像并安装依赖，等待数据库健康检查和前端编译完成后访问：

| 入口 | 地址 |
| --- | --- |
| 首页 | http://localhost:8080/ |
| 课程列表 | http://localhost:8080/course |
| 用户登录 | http://localhost:8080/user/login |
| 管理后台 | http://localhost:8000/admin/ |
| 后端接口 | http://localhost:8000/ |

Compose 启动 `web`、`api`、`db`、`redis`、`worker` 五个服务，项目名为 `skylark-yun-web`。MySQL 和 Redis 仅在容器网络中开放；Python 依赖安装在容器内 `/opt/venv`，无需在宿主机安装。

### 账号与业务数据

新环境默认只有表结构，不包含账号、课程或其他业务数据。创建管理员：

```powershell
docker compose exec api /opt/venv/bin/python manage.py createsuperuser
```

按提示设置用户名、邮箱和密码，再登录后台添加课程分类、讲师、课程、章节、轮播图和导航。需要普通用户测试账号时，可在后台“用户”中新增；前端注册需要短信服务。

当前开发机已有本地测试账号：普通用户 `testuser` / `TestUser2026!`，管理员 `testadmin` / `TestAdmin2026!`。这些账号不会随代码自动创建；公开的演示密码仅用于本地测试。

恢复已有数据时，需要自行导入 MySQL 备份，并将配套上传文件放入 `skylark_api/skylark_api/uploads/`。文件通过 `/media/` 提供访问，但页面内容还需要数据库中的对应记录。数据库备份、上传文件和真实用户数据不包含在代码仓库中。

### 常用操作

```powershell
# 查看日志
docker compose logs --tail 100 api worker web

# 停止 / 再次启动
docker compose stop
docker compose up -d

# 修改代码或依赖后重建
docker compose up -d --build

# 删除容器和网络，保留数据库数据卷
docker compose down
```

数据库保存在 Compose 数据卷中，上传文件保存在宿主机 uploads 目录。`docker compose down -v` 会清空数据库数据卷。已初始化数据库的密码不会因修改 `.env` 而自动更新。

前端后端地址配置在 `skylark_vue/src/settings.js`，默认 `http://127.0.0.1:8000`。当前配置使用 Vue 和 Django 开发服务器；正式部署还需完善服务器、访问控制、HTTPS 等配置。

## 代码结构

```text
skylark-yun-web/
├── compose.yaml                 # 五个服务的容器配置
├── .env.example                 # 环境变量示例
├── skylark_api/                 # Django 后端
│   ├── Dockerfile
│   ├── manage.py
│   ├── mycelery/                # Celery 配置与短信任务
│   └── skylark_api/
│       ├── settings/            # 开发配置、常量和生产配置草稿
│       ├── urls.py              # 后端总路由
│       ├── requirements.txt     # 后端依赖
│       ├── utils/               # 公共模型和异常处理
│       ├── libs/tencent/        # 腾讯云短信封装
│       ├── uploads/             # 本地上传文件，不提交
│       └── apps/
│           ├── Home/            # 轮播广告与导航
│           ├── User/            # 用户、登录、注册和用户订单接口
│           ├── Course/          # 分类、课程、讲师、章节和定价
│           ├── Cart/            # Redis 购物车
│           ├── Order/           # 订单与订单明细
│           └── Coupon/          # 优惠券与用户优惠券
└── skylark_vue/                 # Vue 前端
    ├── Dockerfile
    ├── package.json
    ├── public/static/           # 页面静态图片、样式和视频
    └── src/
        ├── main.js              # 应用入口
        ├── settings.js          # 后端地址
        ├── routers/index.js     # 页面路由
        ├── store/index.js       # 购物车状态
        └── components/
            ├── common/          # 页头、页脚、轮播图和购物车条目
            ├── Home.vue         # 首页
            ├── Course.vue       # 课程列表
            ├── Detail.vue       # 课程详情
            ├── Login.vue        # 登录
            ├── Register.vue     # 注册
            ├── Cart.vue         # 购物车与结算界面
            └── UserOrder.vue    # 订单页面（待完善）
```

## 功能状态

### 已实现

- 首页轮播图、顶部和底部导航从数据库读取。
- 用户名或手机号密码登录、JWT 签发与刷新、记住登录和退出登录。
- 课程分类、列表筛选与排序、分页、课程详情、章节查询及详情页视频展示。
- Redis 购物车：添加、删除、有效期选择、单项勾选、全选与结算数据查询。
- Django 管理后台：管理用户、课程、讲师、轮播图、导航、优惠券和订单等数据。
- 图片、视频等上传文件访问，以及 MySQL、Redis、Celery 的 Docker Compose 集成。

### 部分实现或尚未实现

| 功能 | 当前状态 |
| --- | --- |
| 短信注册 | 已有验证码、Celery 短信任务及注册接口，需要有效的腾讯云短信配置；登录页短信登录未接入 |
| 订单与结算 | 已有订单模型、创建接口和结算界面，生成流程及校验仍有待修复，尚未形成可靠完整流程 |
| 我的订单 | 已有后端用户订单接口，但前端仍有静态示例、接口地址和登录状态问题 |
| 支付 | 未接入完整支付、回调和支付状态更新流程 |
| 优惠券 | 已有模型、查询与结算计算代码；独立“我的优惠券”页面及完整使用流程未完成 |
| 题库、学位课、好课 | 导航来自数据库，目前链接指向首页，没有独立页面 |
| 学习中心、我的账户 | 页头存在入口，但没有对应页面或功能 |
| 购买后学习与进度 | 有课程购买记录模型，完整学习中心、学习进度与权限流程未完成 |
| 密码找回 | 没有完整找回流程 |
| 生产部署与自动化测试 | 目前以开发环境为主，生产配置和业务测试尚未完善 |
