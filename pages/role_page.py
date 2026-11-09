from playwright.sync_api import Page, expect


class RolePage:
    """角色管理页"""

    def __init__(self, page: Page):
        self.page = page
        self.add_button = page.get_by_role("button", name="新增")
        self.search_input = page.locator(".el-form--inline").get_by_placeholder(
            "请输入角色名称"
        )
        self.search_btn = page.get_by_role("button", name="搜索")

    def goto(self):
        """首页进入角色管理"""
        self.page.get_by_role("menuitem", name="系统管理").click()
        self.page.get_by_role("menuitem", name="角色管理").click()
        expect(self.page.locator(".el-table__row").first).to_be_visible()
        expect(self.page.locator(".el-table__header-wrapper")).to_contain_text(
            "角色名称"
        )

    def click_add(self):
        """点新增，等"添加角色"弹窗"""
        self.add_button.click()
        expect(self.page.get_by_role("dialog", name="添加角色")).to_be_visible(
            timeout=5000
        )

    def fill_role_form(self, role_name, role_key):
        """填角色名称 + 权限字符（其他用默认值）"""
        dialog = self.page.get_by_role("dialog", name="添加角色")
        dialog.get_by_role("textbox", name="请输入角色名称").fill(role_name)
        dialog.get_by_role("textbox", name="请输入权限字符").fill(role_key)

    def check_menu(self, menu_label):
        """勾选菜单权限树里的某个节点"""
        dialog = self.page.get_by_role("dialog", name="添加角色")
        dialog.get_by_role("treeitem", name=menu_label).locator(
            ".el-checkbox__inner"
        ).click()

    def submit(self):
        """点确定，等弹窗关闭"""
        dialog = self.page.get_by_role("dialog", name="添加角色")
        dialog.get_by_role("button", name="确 定").click()
        expect(dialog).to_be_hidden(timeout=5000)

    def search(self, keyword):
        """按角色名称搜索"""
        self.search_input.fill(keyword)
        self.search_btn.click()

    def get_row(self, text):
        """按文本找表格行"""
        return self.page.locator(".el-table__row").filter(has_text=text)

    def delete_role(self, role_name):
        """搜索并删除该角色"""
        self.search(role_name)
        row = self.get_row(role_name)
        row.get_by_role("button", name="删除").click()
        confirm_box = self.page.get_by_role("dialog", name="系统提示")
        confirm_box.get_by_role("button", name="确定").click()
        self.search(role_name)
        target_row = self.get_row(role_name)
        expect(target_row).to_be_hidden(timeout=5000)

    def click_edit(self, role_name):    
        """点某行的修改，等"修改角色"弹窗，返回弹窗对象"""
        self.search(role_name)
        self.get_row(role_name).get_by_role("button", name="修改").click()
        edit_dialog = self.page.get_by_role("dialog", name="修改角色")
        expect(edit_dialog).to_be_visible(timeout=5000)
        return edit_dialog

    def edit_role_name(self, old_rolename, new_rolename):
        """修改角色名称"""
        dialog = self.click_edit(old_rolename)
        dialog.get_by_role("textbox", name="请输入角色名称").fill(new_rolename)
        dialog.get_by_role("button", name="确 定").click()
        expect(dialog).to_be_hidden(timeout=5000)
