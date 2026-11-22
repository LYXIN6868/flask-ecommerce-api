# Flask 电商后端

一个用于自动化测试练习的轻量电商后端，基于 **Flask + SQLAlchemy + MySQL** 实现，包含用户注册/登录、商品列表/详情、购物车增删改查，使用 **JWT** 做身份认证。

项目配套两个测试仓库：

- `ecommerce-api-automation`：接口自动化测试框架（pytest + requests + Allure + MySQL 断言）
- `ecommerce-ui-automation`：UI 自动化测试框架（Selenium + PO 模式 + Allure，目标站 saucedemo）

## 技术栈

- Python 3.10+
- Flask 3.x / Flask-SQLAlchemy
- MySQL 5.7+
- PyJWT
- Werkzeug 密码哈希

## 项目结构

```text
flask-ecommerce-api/
├── app.py                  # 服务入口、全局请求拦截
├── conf/                   # 数据库、JWT、日志、响应码配置
├── routes/                 # 蓝图：account / goods / cart
├── rules/                  # 各接口的请求方法、报文格式、必传参数规则
├── tables/                 # SQLAlchemy 表模型
├── utils/                  # 数据库、JWT、序列化工具
├── sql/init.sql            # 建库建表脚本（可选）
├── seed.py                 # 初始化演示用户和商品
├── logs/                   # 运行日志
├── .env.example            # 环境变量示例
└── requirements.txt
```

## 快速开始

### 1. 安装依赖

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. 配置数据库

复制环境变量文件并按本机情况修改：

```bash
copy .env.example .env
```

默认连接 `127.0.0.1:3306` 的 `root / root`，数据库名为 `flask_shop`。

初始化方式二选一：

```bash
# 方式一：先执行 SQL 建表，再写入演示数据
mysql -uroot -proot < sql/init.sql
python seed.py

# 方式二：直接执行 seed.py，SQLAlchemy 会自动建表
python seed.py
```

执行成功后会创建演示账号：

```text
用户名：admin
密码：123456
```

### 3. 启动服务

```bash
python app.py
```

默认地址：`http://127.0.0.1:8081`

访问 `http://127.0.0.1:8081/` 看到 `flask-ecommerce-api is running` 即启动成功。

## 接口说明

| 模块 | 方法 | 路径 | 说明 | 是否需要 token |
|---|---|---|---|---|
| 用户 | POST | `/account/login` | 登录，返回 JWT | 否 |
| 用户 | POST | `/account/register` | 注册 | 否 |
| 商品 | GET | `/goods/list` | 商品列表，支持 page/size | 否 |
| 商品 | GET | `/goods/detail/<gid>` | 商品详情 | 否 |
| 商品 | POST | `/goods/add` | 新增商品（演示用） | 否 |
| 购物车 | GET | `/cart/list` | 购物车列表，支持 page/size | 是 |
| 购物车 | POST | `/cart/add` | 加入购物车 | 是 |
| 购物车 | POST | `/cart/update` | 修改购物车数量 | 是 |
| 购物车 | POST | `/cart/delete` | 删除购物车商品 | 是 |

请求头中的 token 格式：

```text
token: <登录接口返回的 JWT>
```

### 响应格式

```json
{
  "code": 1,
  "msg": "success",
  "data": {}
}
```

列表接口额外返回 `total` 字段。

### 响应码

| code | 含义 |
|---|---|
| 1 | 成功 |
| -1 | 用户名或密码错误 |
| -2 | token 过期 |
| -3 | token 非法 |
| -4 | 参数非法 |
| -5 | 服务器内部错误 |
| -6 | 请求方式错误 |
| -7 | 请求报文格式错误 |
| -8 | 未携带 token |
| -9 | 数据或接口不存在 |
| -10 | 用户名已存在 |

### 示例

登录：

```bash
curl -X POST http://127.0.0.1:8081/account/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"123456\"}"
```

加入购物车：

```bash
curl -X POST http://127.0.0.1:8081/cart/add \
  -H "Content-Type: application/json" \
  -H "token: <上一步返回的 token>" \
  -d "{\"gid\":1,\"count\":2}"
```

## 设计说明

- **Blueprint 分层**：用户、商品、购物车按模块拆分，路由、规则、模型、工具各司其职。
- **统一请求拦截**：`app.py` 在进入路由前统一校验接口是否存在、请求方法、`Content-Type` 和必传参数。
- **JWT 鉴权**：登录后签发 token，购物车蓝图统一校验，并把 uid 挂到 `request` 上。
- **密码安全**：数据库只保存 Werkzeug 生成的密码哈希，不保存明文。
- **配置外置**：数据库、端口、JWT 密钥全部通过环境变量读取，仓库中不提交真实密码。

## 可写进简历的亮点

- 基于 Flask Blueprint 搭建分层电商后端，提供用户、商品、购物车三类 REST 接口。
- 使用 JWT + 密码哈希实现登录鉴权，统一响应码并封装全局请求参数校验。
- 通过 SQLAlchemy ORM 完成多表关联查询，购物车与商品联查、数量累加与用户数据隔离。
- 项目作为接口/UI 自动化测试的被测系统，可与两个测试仓库组成完整的技术闭环。

## License

MIT
