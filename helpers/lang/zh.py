from helpers.logger import Cl

border_element = f"{Cl.blue}-----------------------------{Cl.reset}"

APP_TITLE = (
    f"{border_element}\n"
    "长安安装FW-{}\n"
    f"{border_element}"
)
INSTALL_WARNING_NO_ROOT = (
    f"{Cl.yellow}注意：安装的应用程序在安装后无法卸载！\n"
    f"如果要重置您的主机，需要通过系统设置进行出厂重置。\n"
    f"{Cl.red}警告！！！出厂重置可能会删除车辆的TUID！您需要请求授权代表来恢复它。"
)

CERT_DELETE_WARNING = (
    f"{Cl.green}签名已完成。\n"
    f"{border_element}"
    f"{Cl.red}请勿删除CERT文件夹。它是更新应用程序所必需的。\n"
    f"请确保创建CERT文件夹的备份副本，以确保更新可以顺利进行。\n"
    f"{border_element}"
)
INSTALL_ALL_START = "正在安装apks..."
INSTALL_ALL_END = "安装完成"
FIRMWARE_VERSION_SEARCH = "正在搜索固件版本..."
FIRMWARE_VERSION_NOT_FOUND = f"{Cl.red}未找到车载固件版本。"
BUY_ACCESS_MESSAGE = (
    f"\n您必须购买访问权限才能安装应用程序。从菜单中选择适当的项目。\n"
    f"访问权限是为一辆车购买的。")

# titles
WARNING = "！！！警告！！！"

# main
WAITING_DEVICE = "等待设备..."
CONNECT_ERROR = (
    "{}无法连接到设备！{}\n请检查是否安装了驱动程序，并且设备在设备管理器中被检测到，然后重新连接。"
)
DEVICE_IS_CONNECT = "{}设备在线"
CAR_PREPARE = "正在准备车辆数据，请稍候..."
CERT_PREPARE = "正在准备证书，请稍候..."
MSG_DONE = f"[{Cl.green}完成{Cl.reset}]"
MSG_ACCESS_ERROR = f"{Cl.reset}[{Cl.red}访问错误{Cl.reset}]"
MSG_CONNECTION_ERROR = f"{Cl.red}连接错误{Cl.reset}"
MSG_OK = f"[{Cl.green}好{Cl.reset}]"
MSG_FALSE = f"[{Cl.red}错误{Cl.reset}]"
MSG_USER_ERROR = f"[{Cl.red}该车辆已绑定到其他用户{Cl.reset}]"
MSG_UNINSTALL = "应用程序的数据已删除。现在可以删除程序文件夹。"
MSG_TERMINAL_EXIT = f"{Cl.magenta}######\n要退出终端并返回程序菜单，请输入 'exit'\n######{Cl.reset}"
MSG_CERT_DOWNLOAD_COMPLETE = "证书下载链接：\n{}"

# ARGS
ARG_CLEAR = "删除应用程序数据"

# main menu
MAIN_MENU_TITLE = "{} 车菜单"
INSTALL_FREE = f"{Cl.green}免费安装{Cl.reset}"
INSTALL_FROM_FOLDER = "从apk文件夹安装所有apks"
INSTALL_HUR = "安装Headunit Reloaded (AndroidAuto) MOD"
INSTALL_KIT = "安装Autokit (CarPlay)"
CLEAR_CACHE = "清除启动器缓存"
SHOW_FREE_SPACE = "显示可用空间"
OPEN_SYSTEM_SETTINGS = "打开系统设置"
HIDE_ALL_APPS = "隐藏所有已安装的应用程序"
SHOW_ALL_APPS = "显示所有已安装的应用程序"
RENAME_CAR = "重命名车"
RESET_HEADUNIT = "{}重置主机（删除已安装的应用程序）{}"
DELETE_ALL_APPS = "删除所有已安装的应用程序"
SERVICE_MENU = "附加服务"
EXIT = "退出"
SELECT_MENU_ITEM = "选择一个菜单项: "

# Free install menu
FREE_TITLE = "免费安装"
FREE_DESCRIPTION = """选择您要安装的应用程序。如果应用程序已安装，
这意味着您的汽车已经支持。不要安装不需要的应用程序。
目前，无法卸载已安装的应用程序。"""

# reg menu
EMAIL = f"{Cl.green}邮箱:{Cl.reset} "
PASSWORD = f"{Cl.green}密码{Cl.reset}（密码不显示，输入后按回车）: "

# Warning from apk menu
INSTALL_FROM_APK_TITLE = """
并非所有应用程序都能在安装后运行。请选择适合您Android系统版本和处理器版本的APK文件。同时，请检查应用程序是否与Google服务绑定。
"""

# autokit submenu
CONTINUE = "继续"
RETURN_TO_MAIN_MENU = "返回主菜单"
KIT_MENU_DESCRIPTION = ("在某些设备上，没有购买特殊设备（carlinkit）无法通过Autokit连接。\n"
                        "不要安装，除非您确定！")
KIT_INSTALLING = "正在安装AutoKit..."

# open settings submenu
SETTINGS_TITLE = "设置"
SETTINGS_EXIT = "退出设置"
SETTINGS_DESCRIPTION = "按下 '1' 转到系统设置 或 '2' 关闭 Android 设置"
SETTINGS_SYSTEM = "访问系统设置"

# 服务菜单
SERVICE_TITLE = "服务菜单"
SERVICE_DESCRIPTION = "如果不理解这些步骤的目的，请不要执行这些步骤。"
SERVICE_PACKAGES_DELETE = f"{Cl.red}[root]{Cl.reset} 重置 packages.xml"
SERVICE_ADB_CONSOLE = "打开终端执行 adb 命令"
SERVICE_SAVE_CERT = "下载证书以进行手动签名"
SERVICE_DUMP = f"{Cl.red}[root]{Cl.reset} 转储分区"

# Dump menu title
DUMP_TITLE = "复制分区"
DUMP_DESCRIPTION = ("选择要保存到计算机的分区。此分区将保存\n"
                    "在 tools/dump 文件夹中。")
DUMP_MSG_START = "分区 {} 的复制已开始。此过程可能需要几分钟。请耐心等待。"

# hur
HUR_INSTALLING = "正在安装AndroidAuto模拟器..."

# payment
OPEN_BROWSER_DESCRIPTION = "在浏览器中打开URL以购买对一辆车的访问权限"
PAYMENT_WAIT = "等待付款确认..."
PAYMENT_SUCCESS = "{}付款成功。{} 现在您可以安装应用程序到主机。"

# car select menu
SELECT_CAR = "选择一辆车"

# Install from folder
INSTALL_FROM_FOLDER_MSG = "从'apk'文件夹安装apks..."

# rename car
RENAME_CAR_MSG = "输入新车名: "

# adb
DISABLE_VERITY_OFF = f"{Cl.red}您的设备上不可用disable-verity命令。"
DISABLE_VERITY_STATUS = "Verity状态: {} - "
ROOT_STATUS = "Root状态: {}"

# car
DISABLING_APKS = "禁用用户apks"
ENABLING_APKS = "启用用户apks"

# helper
PRESS_ANY_KEY = "按任意键继续..."
PRESS_ANY_KEY_TO_EXIT = "按任意键退出..."

# server
REG_SUCCESS = "注册成功"
REG_FAILED = "{}注册失败。请检查您的凭据。{}"
AUTH_SUCCESS = "认证成功！"
AUTH_FAILED = "{}认证失败。请检查您的凭据。{}"

USER_LICENSE_TITLE = "用户协议"
USER_LICENSE = f"""用户协议

1. 总则
本用户协议（以下简称“协议”）规定了使用一款可以在长安汽车主机上安装应用程序的软件的条款，以及启动隐藏应用程序、隐藏已安装的应用程序或重新显示它们的功能（以下简称“程序”）。使用该程序即表示您同意本协议的条款。

### 2. 使用目的
该程序仅为研究和演示长安汽车主机的隐藏功能而创建。开发者不对使用该程序引发的任何后果负责。

### 3. 付费使用
##  3.1. 该程序是付费的。付款是自愿的，并按照所提供的支付方式进行。付款不保证程序所有功能的持续运行，也不提供因功能不完整或不满意而退款的权利。
##  3.2. 开发者保留随时更改程序费用和付款条件的权利，且无需事先通知。

### 4. 限制与风险
##  4.1. 使用该程序可能会导致您的汽车主机保修失效。您承认，使用该程序的风险由您自行承担。
##  4.2. 开发者不对因使用该程序造成的任何损害负责，包括但不限于对软件、硬件、数据的损坏或其他损失。

### 5. 免责声明
##  5.1. 该程序的开发者与长安汽车公司或其子公司无关。所有与长安汽车相关的商标、标志和其他知识产权均归各自所有者所有。
##  5.2. 该程序按“原样”提供，开发者不对其功能或适用于特定目的作出任何明示或暗示的保证。

### 6. 协议变更
开发者保留随时更改本协议条款的权利。更改自更新版本的协议在网站或程序中发布之时起生效。

### 7. 联系方式
所有关于该程序使用的问题可以发送至电子邮箱 changan_install@humanbait.ru。

### 8. 适用法律
使用该程序即表示您确认已阅读、理解并同意本协议的条款。

最后更新日期：2024年9月8日
{Cl.green}Y: 同意 {Cl.reset}| {Cl.red}任意键: 关闭程序{Cl.reset}
"""
