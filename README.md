# RuoYi-Vue UI 自动化测试

> 基于 **Playwright + pytest** 的 Web UI 自动化测试项目，覆盖若依后台管理系统的**登录**、**用户管理**、**角色管理**三大模块，共 **14 条用例**。
>
> 采用 **Page Object Model** 分层设计，支持 **Allure 可视化报告**与**失败自动截图**。

---

## 📊 测试覆盖

| 模块 | 用例数 | 覆盖场景 |
|------|--------|---------|
| 登录认证 | 5 | 页面加载、正常登录、密码错误、账号为空、密码为空 |
| 用户管理 | 5 | 新增、搜索、修改昵称、删除、用户名为空（前端校验） |
| 角色管理 | 4 | 新增（含菜单权限树）、角色名为空、修改角色名称、删除 |
| **合计** | **14** | 全部通过，耗时约 **50 秒** |

---

## 🛠 技术栈

| 类别 | 使用 |
|------|------|
| 语言 | Python 3.10 |
| UI 自动化 | Playwright (Chromium) |
| 测试框架 | pytest |
| 报告 | Allure |
| 依赖服务 | Redis（读取验证码答案） |

---

## 📁 项目结构

```
RuoYi-UI-Test/
├── pytest.ini                # pytest 配置（testpaths / pythonpath）
├── conftest.py               # 全局 fixture + 失败截图钩子
├── requirements.txt
├── pages/                    # Page Object：一个页面一个类
│   ├── login_page.py         # 登录页
│   ├── user_page.py          # 用户管理页
│   └── role_page.py          # 角色管理页
├── tests/                    # 测试用例：只写「调方法 + 断言」
│   ├── test_login.py
│   ├── test_user.py
│   └── test_role.py
└── utils/
    └── captcha.py            # 从 Redis 读取验证码答案
```

---

## 🏗 核心设计

### 1. Page Object Model 分层

页面元素与操作封装在 `pages/` 下的类中，用例只负责业务步骤与断言。

```python
role = RolePage(page)
role.goto()
role.click_add()
role.fill_role_form(rolename, access)
role.check_menu("系统管理")
role.submit()
role.search(rolename)
expect(role.get_row(rolename)).to_be_visible()
```

> 页面改版时只需维护 Page 类，用例无需改动。

### 2. fixture 分层依赖

```
browser (session，整个会话只启动一次)
  └── page (function，每个用例独立 context，保证隔离)
        └── logged_in_page (已登录的页面)
              ├── user_page ──→ created_user  (建数据 → 交给用例 → 自动清理)
              └── role_page ──→ created_role
```

用例只需声明依赖，pytest 自动按依赖链执行前置与后置。

```python
def test_delete_user(user_page, created_user):
    ...   # created_user 自动创建用户，用例结束后自动删除
```

### 3. 验证码自动登录

若依登录需要图片验证码。本项目通过 `page.expect_response` 捕获 `/captchaImage` 响应拿到 `uuid`，再用 `uuid` 从 Redis 中读取验证码答案，实现**全自动登录**，无需人工干预或关闭验证码。

```python
with page.expect_response("**/captchaImage") as res:
    self.goto()
uuid = res.value.json()["uuid"]
captcha = get_captcha(uuid)          # redis: captcha_codes:{uuid}
```

### 4. 失败自动截图

通过 `pytest_runtest_makereport` 钩子监听用例失败，自动保存失败瞬间的整页截图到 `reports/`。

### 5. 测试数据自动清理

创建数据的 fixture 使用 `yield` 划分前置/后置，用例结束后自动删除测试数据，避免污染环境。

---

## 🚀 快速开始

### 环境要求

- 已部署的 RuoYi-Vue 系统：前端 `http://localhost:8081`、后端 `http://localhost:8080`
- 本地 Redis（默认 `localhost:6379`）

### 安装

```bash
pip install -r requirements.txt
playwright install chromium
```

### 运行

```bash
# 全部用例
pytest

# 指定模块
pytest tests/test_role.py -v

# 生成 Allure 数据
pytest --alluredir=./allure-results
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

---

## 💡 实现中解决的问题

| 问题 | 解决方式 |
|------|---------|
| 搜索框与弹窗输入框 placeholder 同名，触发 **strict mode violation** | 缩小定位作用域，限定在 `.el-form--inline` 搜索表单内 |
| 弹窗关闭后节点仍留在 DOM，导致定位到隐藏元素 | 优先使用 `get_by_role`（基于可访问性树，默认排除隐藏元素） |
| Element UI 的 `el-select` 只读，无法直接 `fill` | 先点击展开，再选中下拉项 |
| 用例失败后数据残留在数据库 | 将「创建成功」的标记时机提前到提交动作之后，而非断言通过之后 |
| Windows 控制台 GBK 编码，`print` 含 emoji 导致 pytest `INTERNALERROR` | 日志统一使用 ASCII 标记 |

---

## 📝 说明

- 被测系统为开源项目 [RuoYi-Vue](https://github.com/yangzongzhuan/RuoYi-Vue)，需自行部署。
- 默认测试账号：`admin / admin123`（可在 `conftest.py` 中修改）。
- 测试数据统一以 `test_` 为前缀命名，便于识别与清理。
