import re
from playwright.sync_api import Page, expect

from config import BASE_URL


class LoginPage:
    """登录页"""

    def __init__(self, page: Page):
        self.page = page
        # 元素定位器集中管理
        self.username_input = page.get_by_placeholder("账号")
        self.password_input = page.get_by_placeholder("密码")
        self.captcha_input = page.get_by_placeholder("验证码")
        self.login_button = page.get_by_role("button", name="登 录")

    def goto(self):
        """打开登录页"""
        self.page.goto(f"{BASE_URL}/login")

    def login(self, username: str, password: str, captcha: str):
        """完整的登录操作"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.captcha_input.fill(captcha)
        self.login_button.click()

    def assert_login_success(self):
        """断言登录成功"""
        expect(self.page).to_have_url(re.compile(r".*/index"), timeout=15000)

    def login_with_auto_captcha(self, username: str, password: str):
        """自动读取验证码并登录（用于测试登录场景）"""
        from utils.captcha import get_captcha

        with self.page.expect_response("**/captchaImage") as res:
            self.goto()
        captcha_data = res.value.json()
        uuid = captcha_data["uuid"]
        captcha_enable = captcha_data.get("captchaEnabled", True)
        if captcha_enable:
            captcha = get_captcha(uuid)
        else:
            captcha = ""
        self.login(username, password, captcha)
