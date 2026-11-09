import pytest
import time
import os
from playwright.sync_api import sync_playwright, expect

from config import HEADLESS
from pages.login_page import LoginPage
from pages.user_page import UserPage
from pages.role_page import RolePage
from utils.captcha import get_captcha


@pytest.fixture(scope="session")
def browser():
    """整个测试会话前启动一次浏览器"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """每个用例一个独立页面"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def logged_in_page(page):
    """返回一个已登录的 page"""
    login = LoginPage(page)

    login.login_with_auto_captcha("admin", "admin123")
    login.assert_login_success()
    return page


@pytest.fixture
def user_page(logged_in_page):
    """返回用户管理页对象（已登录）"""
    return UserPage(logged_in_page)


@pytest.fixture
def role_page(logged_in_page):
    """返回角色管理页对象（已登录）"""
    return RolePage(logged_in_page)


@pytest.fixture
def created_user(user_page):
    """创建一个测试用户，用例结束后自动删除"""
    ts = int(time.time() * 1000)
    username = f"test_{ts}"
    nickname = f"测试用户_{ts}"

    # 前置：创建
    user_page.goto()
    user_page.click_add()
    user_page.fill_user_form(nickname, username, "123456")
    user_page.submit()
    user_page.search(username)
    expect(user_page.get_row(username)).to_be_visible(timeout=5000)

    yield username  # ← 把用户名交给用例

    # 后置：清理
    try:
        user_page.search(username)
        row = user_page.get_row(username)
        if row.count() > 0:
            user_page.delete_user(username)
    except Exception as e:
        print(f"[WARN] 清理失败（不影响结果）: {e}")


@pytest.fixture
def created_role(role_page):
    """创建一个测试角色，用例结束后自动删除"""
    temp = int(time.time() * 1000)
    rolename = f"test_{temp}"
    access = f"UItest_{temp}"

    # 前置
    role_page.goto()
    role_page.click_add()
    role_page.fill_role_form(rolename, access)
    role_page.check_menu("系统管理")
    role_page.submit()
    role_page.search(rolename)
    expect(role_page.get_row(rolename)).to_be_visible(timeout=8000)

    info={"name":rolename,"key":access}

    yield info

    # 后置：清理
    try:
        role_page.search(info["name"])
        row = role_page.get_row(info["name"])
        if row.count() > 0:
            role_page.delete_role(info["name"])
    except Exception as e:
        print(f"[WARN] 清理失败（不影响结果）: {e}")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # 只处理call阶段，并且用例失败
    if rep.when == "call" and rep.failed:
        page = None
        # 从用例参数获取page对象
        funcargs = item.funcargs
        if "page" in funcargs:
            page = funcargs["page"]
        elif "logged_in_page" in funcargs:
            page = funcargs["logged_in_page"]
        elif "user_page" in funcargs:
            page = funcargs["user_page"].page

        if page is not None:
            os.makedirs("reports", exist_ok=True)
            img_path = f"reports/fail_{item.name}.png"
            try:
                page.screenshot(path=img_path, full_page=True)
                print(f"\n[SCREENSHOT] 失败截图已保存: {img_path}")
                # 如果需要同时嵌入allure报告，加上下面两行
                # allure.attach(page.screenshot(full_page=True), name="失败截图", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"\n[WARN] 截图捕获异常: {e}")
