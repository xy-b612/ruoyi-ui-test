import time
import allure
from playwright.sync_api import expect
from allure_commons.types import Severity

@allure.feature("角色管理模块")
@allure.story("新增角色功能")
@allure.title("TC_ROLE_001 新增角色")
@allure.severity(Severity.CRITICAL)
def test_add_role(role_page):
    """TC_ROLE_001 新增角色"""
    temp = int(time.time() * 1000)
    rolename = f"test_{temp}"
    access = f"UItest_{temp}"

    role_page.goto()
    role_page.click_add()
    role_page.fill_role_form(rolename, access)
    role_page.check_menu("系统管理")
    role_page.submit()

    role_page.search(rolename)
    expect(role_page.get_row(rolename)).to_be_visible(timeout=8000)


@allure.feature("角色管理模块")
@allure.story("新增角色功能")
@allure.title("TC_ROLE_002 新增角色-角色名为空")
@allure.severity(Severity.NORMAL)
def test_add_role_empty_name(role_page):
    """TC_ROLE_002 新增角色-角色名为空"""
    temp = int(time.time() * 1000)
    access = f"UItest_{temp}"

    role_page.goto()
    role_page.click_add()

    dialog = role_page.page.get_by_role("dialog", name="添加角色")
    dialog.get_by_role("textbox", name="请输入权限字符").fill(access)
    dialog.get_by_role("button", name="确 定").click()

    expect(dialog.get_by_text("角色名称不能为空")).to_be_visible() 


@allure.feature("角色管理模块")
@allure.story("修改角色功能")
@allure.title("TC_ROLE_003 修改角色名称")
@allure.severity(Severity.CRITICAL)
def test_edit_role_name(role_page, created_role):
    """TC_ROLE_003 修改角色名称"""
    old_rolename=created_role["name"]
    temp = int(time.time()*1000)
    new_rolename = f"test_{temp}"

    role_page.edit_role_name(old_rolename, new_rolename)

    created_role["name"] = new_rolename
    expect(
        role_page.page.locator(".el-message").filter(has_text="修改成功")
    ).to_be_visible(timeout=5000)
    role_page.search(new_rolename)
    expect(role_page.get_row(new_rolename)).to_be_visible()


@allure.feature("角色管理模块")
@allure.story("删除角色功能")
@allure.title("TC_ROLE_004 删除角色")
@allure.severity(Severity.CRITICAL)
def test_delete_role(role_page, created_role):
    """TC_ROLE_004 删除角色"""
    rolename = created_role["name"]
    role_page.delete_role(rolename)

    expect(
        role_page.page.locator(".el-message").filter(has_text="删除成功")
    ).to_be_visible(timeout=5000)

    # 删除后应该搜不到（表格显示"暂无数据"）
    role_page.search(rolename)
    expect(role_page.page.get_by_text("暂无数据")).to_be_visible()
