import re
import allure
from playwright.sync_api import expect
from allure_commons.types import Severity
from pages.login_page import LoginPage


# ---------- 正向 ----------
@allure.feature("登录模块")
@allure.story("登录功能")
@allure.title("TC_LOGIN_001 登录页正常加载")
@allure.severity(Severity.BLOCKER)
def test_login_page_load(page):
    """TC_LOGIN_001 登录页正常加载"""
    login = LoginPage(page)
    login.goto()

    expect(page.get_by_placeholder("账号")).to_be_visible()
    expect(page.get_by_placeholder("密码")).to_be_visible()
    expect(page.get_by_role("button", name="登 录")).to_be_visible()


@allure.feature("登录模块")
@allure.story("登录功能")
@allure.title("TC_LOGIN_002 正常登录成功 —— 注意只有 1 行！")
@allure.severity(Severity.BLOCKER)
def test_login_success(logged_in_page):
    """TC_LOGIN_002 正常登录成功 —— 注意只有 1 行！"""
    expect(logged_in_page).to_have_url(re.compile(r".*/index"))


# ---------- 异常 ----------
@allure.feature("登录模块")
@allure.story("登录功能")
@allure.title("TC_LOGIN_003 密码错误")
@allure.severity(Severity.NORMAL)
def test_login_wrong_password(page):
    """TC_LOGIN_003 密码错误"""
    login = LoginPage(page)
    login.login_with_auto_captcha("admin", "wrong_password")

    expect(page.locator(".el-message")).to_contain_text("用户不存在/密码错误")


@allure.feature("登录模块")
@allure.story("登录功能")
@allure.title("TC_LOGIN_004 账号为空（前端校验）")
@allure.severity(Severity.NORMAL)
def test_login_empty_username(page):
    """TC_LOGIN_004 账号为空（前端校验）"""
    login = LoginPage(page)
    login.goto()
    login.login("", "admin123", "")

    expect(page.get_by_text("请输入您的账号")).to_be_visible()


@allure.feature("登录模块")
@allure.story("登录功能")
@allure.title("TC_LOGIN_005 密码为空（前端校验）")
@allure.severity(Severity.NORMAL)
def test_login_empty_password(page):
    """TC_LOGIN_005 密码为空（前端校验）"""
    login = LoginPage(page)
    login.goto()
    login.login("admin", "", "")

    expect(page.get_by_text("请输入您的密码")).to_be_visible()
