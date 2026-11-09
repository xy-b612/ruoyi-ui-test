import time
import allure
from playwright.sync_api import expect
from allure_commons.types import Severity

@allure.feature("用户管理模块")
@allure.story("新增用户功能")
@allure.title("TC_USER_001 新增用户成功")
@allure.severity(Severity.CRITICAL)
def test_add_user(user_page):
    """TC_USER_001 新增用户成功"""
    ts = int(time.time() * 1000)
    username = f"test_{ts}"
    nickname = f"测试用户_{ts}"

    user_page.goto()
    user_page.click_add()
    user_page.fill_user_form(nickname, username, "123456", sex="男")
    user_page.submit()

    user_page.search(username)
    expect(user_page.get_row(username)).to_be_visible(timeout=5000)


@allure.feature("用户管理模块")
@allure.story("搜索用户功能")
@allure.title("TC_USER_002 搜索用户")
@allure.severity(Severity.CRITICAL)
def test_search_user(user_page, created_user):
    """TC_USER_002 搜索用户"""
    user_page.search(created_user)
    expect(user_page.get_row(created_user)).to_be_visible()


@allure.feature("用户管理模块")
@allure.story("修改用户功能")
@allure.title("TC_USER_003 修改用户昵称")
@allure.severity(Severity.CRITICAL)
def test_edit_user_nickname(user_page, created_user):
    """TC_USER_003 修改用户昵称"""
    new_nickname = "修改后的昵称"
    user_page.edit_nickname(created_user, new_nickname)

    expect(user_page.page.locator(".el-message")).to_contain_text("成功")
    user_page.search(created_user)
    expect(user_page.get_row(new_nickname)).to_be_visible()


@allure.feature("用户管理模块")
@allure.story("删除用户功能")
@allure.title("TC_USER_004 删除用户")
@allure.severity(Severity.CRITICAL)
def test_delete_user(user_page, created_user):
    """TC_USER_004 删除用户"""
    user_page.delete_user(created_user)

    expect(user_page.page.locator(".el-message")).to_contain_text("成功")
    user_page.search(created_user)
    # 删除后应该搜不到（表格显示"暂无数据"）
    expect(user_page.page.get_by_text("暂无数据")).to_be_visible()


@allure.feature("用户管理模块")
@allure.story("新增用户功能")
@allure.title("TC_USER_005 新增用户-用户名为空（前端校验）")
@allure.severity(Severity.NORMAL    )
def test_add_user_empty_username(user_page):
    """TC_USER_005 新增用户-用户名为空（前端校验）"""
    user_page.goto()
    user_page.click_add()

    dialog = user_page.page.get_by_role("dialog", name="添加用户")
    dialog.get_by_role("textbox", name="请输入用户昵称").fill("测试")
    dialog.get_by_role("textbox", name="请输入用户密码").fill("123456")
    dialog.get_by_role("button", name="确 定").click()

    expect(dialog.get_by_text("用户名称不能为空")).to_be_visible() 
