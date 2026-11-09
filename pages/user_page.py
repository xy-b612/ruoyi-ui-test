from playwright.sync_api import Page, expect


class UserPage:
    """用户管理页"""

    def __init__(self, page: Page):
        self.page = page
        self.add_button = page.get_by_role("button", name="新增")
        self.search_input = page.locator(".el-form--inline").get_by_placeholder(
            "请输入用户名称"
        )
        self.search_button = page.get_by_role("button", name="搜索")

    def goto(self):
        """从首页进入用户管理"""
        self.page.get_by_role("menuitem", name="系统管理").click()
        self.page.get_by_role("menuitem", name="用户管理").click()
        expect(self.page.locator(".el-table__row").first).to_be_visible()

    def click_add(self):
        """点击新增按钮"""
        self.add_button.click()
        expect(self.page.get_by_role("dialog", name="添加用户")).to_be_visible()

    def fill_user_form(self, nickname, username, password, sex="男"):
        """填写新增用户表单"""
        dialog = self.page.get_by_role("dialog", name="添加用户")
        dialog.get_by_role("textbox", name="请输入用户昵称", exact=True).fill(nickname)
        dialog.get_by_role("textbox", name="请输入用户名称", exact=True).fill(username)
        dialog.get_by_role("textbox", name="请输入用户密码", exact=True).fill(password)
        dialog.get_by_role("textbox", name="请选择性别").click()
        self.page.locator(".el-select-dropdown:visible").get_by_text(
            sex, exact=True
        ).click()

    def submit(self):
        """提交新增用户表单"""
        dialog = self.page.get_by_role("dialog", name="添加用户")
        dialog.get_by_role("button", name="确 定").click()
        expect(dialog).to_be_hidden(timeout=8000)

    def search(self, keyword):
        """搜索用户"""
        self.search_input.fill(keyword)
        self.search_button.click()

    def get_row(self, text):
        """按文本找表格行"""
        return self.page.get_by_role("row").filter(has_text=text)

    def delete_user(self, username):
        """删除指定用户"""
        self.search(username)
        self.get_row(username).get_by_role("button", name="删除").click()
        confirm = self.page.get_by_role("dialog", name="系统提示")
        expect(confirm).to_be_visible(timeout=5000)
        confirm.get_by_role("button", name="确定").click()

    def click_edit(self, username):
        """点击某行的"修改"按钮，等编辑弹窗出现"""
        self.get_row(username).get_by_role("button", name="修改").click()
        dialog = self.page.get_by_role("dialog", name="修改用户")
        expect(dialog).to_be_visible()
        return dialog

    def edit_nickname(self, username, new_nickname):
        """修改用户昵称"""
        dialog = self.click_edit(username)
        dialog.get_by_role("textbox", name="请输入用户昵称").fill(new_nickname)
        dialog.get_by_role("button", name="确 定").click()
