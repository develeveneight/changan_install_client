from helpers.logger import Cl

border_element = f"{Cl.blue}-----------------------------{Cl.reset}"

APP_TITLE = (
    f"{border_element}\n"
    "Changan Install FW-{}\n"
    f"{border_element}"
)
INSTALL_WARNING_NO_ROOT = (
    f"{Cl.yellow}CAUTION: Installed applications cannot be uninstalled after installation!\n"
    f"If you want to reset your head unit, you need to do a factory reset via system settings.\n"
    f"{Cl.red}WARNING!!! A factory reset may delete the vehicle TUID! You will need to request\n"
    f"an authorized representative to restore it."
)

CERT_DELETE_WARNING = (
    f"{Cl.green}Signing is complete.\n"
    f"{border_element}"
    f"{Cl.red}Please do not delete the CERT folder. It is necessary for updating applications as new versions are released. \n"
    f"Make sure to create a backup copy of the CERT folder to ensure updates can be performed without issues.\n"
    f"{border_element}"
)
INSTALL_ALL_START = "Installing apks..."
INSTALL_ALL_END = "Install complete"
FIRMWARE_VERSION_SEARCH = "Searching Firmware version..."
FIRMWARE_VERSION_NOT_FOUND = f"{Cl.red}No car firmware version found."
BUY_ACCESS_MESSAGE = (
    f"\nYou must purchase access to install applications. Select the appropriate item from the menu.\n"
    f"Access is purchased for one vehicle")

# titles
WARNING = "!!!WARNING!!!"

# main
WAITING_DEVICE = "Waiting device..."
CONNECT_ERROR = (
    "{}Can't connect to device!{}\nCheck if the drivers are installed and the device is detected in Device "
    "Manager and reconnect again")
DEVICE_IS_CONNECT = "{}Device is online"
CAR_PREPARE = "Preparing car data. Wait please..."
CERT_PREPARE = "Preparing certificate. Wait please..."
MSG_DONE = f"[{Cl.green}Done{Cl.reset}]"
MSG_ACCESS_ERROR = f"{Cl.reset}[{Cl.red}Access error{Cl.reset}]"
MSG_CONNECTION_ERROR = f"{Cl.red}Connection error{Cl.reset}"
MSG_OK = f"[{Cl.green}OK{Cl.reset}]"
MSG_FALSE = f"[{Cl.red}False{Cl.reset}]"
MSG_USER_ERROR = f"[{Cl.red}This vehicle is linked to another user{Cl.reset}]"
MSG_UNINSTALL = "The application's data has been deleted. You can now remove the program folder."
MSG_TERMINAL_EXIT = f"{Cl.magenta}######\nTo exit the terminal and return to the program menu, type 'exit'\n######{Cl.reset}"
MSG_CERT_DOWNLOAD_COMPLETE = "Certificate download link:\n{}"

# ARGS
ARG_CLEAR = "Remove the application's data"

# main menu
MAIN_MENU_TITLE = "{} Car Menu"
INSTALL_FREE = f"{Cl.green}Free Installation{Cl.reset}"
INSTALL_FROM_FOLDER = "Install all apks from apk folder"
INSTALL_HUR = "Install Headunit Reloaded (AndroidAuto) MOD"
INSTALL_KIT = "Install Autokit (CarPlay)"
CLEAR_CACHE = "Clear cache for launchers"
SHOW_FREE_SPACE = "Show free space"
OPEN_SYSTEM_SETTINGS = "Open Android Settings"
HIDE_ALL_APPS = "Hide all installed apps"
SHOW_ALL_APPS = "Show all installed apps"
RENAME_CAR = "Rename car"
RESET_HEADUNIT = "{}Reset headunit (delete installed apps){}"
DELETE_ALL_APPS = "Delete all installed apps"
SERVICE_MENU = "Additional services"
EXIT = "Exit"
SELECT_MENU_ITEM = "Select a menu item: "

# Free install menu
FREE_TITLE = "Free Installation"
FREE_DESCRIPTION = """Select the application you want to install. If the application is installed,
it means your car is already supported. Do not install the application if you do not need it.
At this time, uninstalling installed applications is not available."""

# reg menu
EMAIL = f"{Cl.green}Email:{Cl.reset} "
PASSWORD = f"{Cl.green}Password{Cl.reset} (The password is not displayed. press Enter after entering it): "

# Warning from apk menu
INSTALL_FROM_APK_TITLE = """
Not all applications may run after installation. Choose APK files according to your Android system
version and processor version. Also, check if the application is tied to Google services.
"""


# autokit submenu
CONTINUE = "Continue"
RETURN_TO_MAIN_MENU = "Return to main menu"
KIT_MENU_DESCRIPTION = ("Connection via Autokit is not possible without purchasing a special device (carlinkit)\n"
                        "on some devices. Do not install unless you are sure!")
KIT_INSTALLING = "Installing AutoKit..."

# open settings submenu
SETTINGS_TITLE = "Settings"
SETTINGS_EXIT = "Exit from settings"
SETTINGS_DESCRIPTION = "Press '1' to go to system settings r '2' to close Android Settings"
SETTINGS_SYSTEM = "Open System Settings"

# Service menu
SERVICE_TITLE = "Service Menu"
SERVICE_DESCRIPTION = "Do not perform these steps if you do not understand their purpose."
SERVICE_PACKAGES_DELETE = f"{Cl.red}[root]{Cl.reset} Reset packages.xml"
SERVICE_ADB_CONSOLE = "Open terminal for executing adb commands"
SERVICE_SAVE_CERT = "Download the certificate for manual signing"
SERVICE_DUMP = f"{Cl.red}[root]{Cl.reset} Dump partitions"

# Dump menu title
DUMP_TITLE = "Copy partitions"
DUMP_DESCRIPTION = ("Select the partition you want to save on your computer. This partition will be saved\n"
                    "in the tools/dump folder.")
DUMP_MSG_START = "Copying partition {} has started. This process may take a few minutes. Please be patient."

# hur
HUR_INSTALLING = "Installing AndroidAuto Emulator..."

# payment
OPEN_BROWSER_DESCRIPTION = "Open URL in your browser for purchase access to 1 car"
PAYMENT_WAIT = "Waiting payment confirmation..."
PAYMENT_SUCCESS = "{}Payment succeeded.{} Now you can install apps to the Head unit."

# car select menu
SELECT_CAR = "Select a car"

# Install from folder
INSTALL_FROM_FOLDER_MSG = "Installing apk files from 'apk' folder..."

# rename car
RENAME_CAR_MSG = "Enter a new name of the car: "


# adb
DISABLE_VERITY_OFF = f"{Cl.red}disable-verity command is not available on your device."
DISABLE_VERITY_STATUS = "Verity status: {} - "
ROOT_STATUS = "Root status: {}"

# car
DISABLING_APKS = "Disabling user apks"
ENABLING_APKS = "Enabling user apks"

# helper
PRESS_ANY_KEY = "Press any key to continue..."
PRESS_ANY_KEY_TO_EXIT = "Press any key to exit..."

# server
REG_SUCCESS = "Successfully registered"
REG_FAILED = "{}Failed to register. Please check your credentials.{}"
AUTH_SUCCESS = "Successfully authenticated!"
AUTH_FAILED = "{}Failed to authenticate. Please check your credentials.{}"

USER_LICENSE_TITLE = "User Agreement"
USER_LICENSE = f"""User Agreement

1. General Provisions
This User Agreement (hereinafter referred to as the "Agreement") governs the terms of use for a program that allows the installation of applications on Changan car head units, as well as the ability to launch hidden applications, hide installed applications, or display them again (hereinafter referred to as the "Program"). By using the Program, you agree to the terms of this Agreement.

### 2. Purpose of Use
The Program is created solely for the research and demonstration of hidden features of Changan car head units. The developer is not responsible for any consequences arising from the use of the Program.

### 3. Paid Usage
##  3.1. The Program is paid. Payment is made voluntarily and is carried out in accordance with the proposed payment methods. Payment does not guarantee the uninterrupted operation of all features of the Program and does not grant the right to a refund for incomplete or unsatisfactory functionality.
##  3.2. The developer reserves the right to change the cost of the Program and the payment terms at any time without prior notice.

### 4. Limitations and Risks
##  4.1. Using the Program may void the warranty on your car's head unit. You acknowledge that using the Program is at your own risk.
##  4.2. The developer is not responsible for any damage caused as a result of using the Program, including but not limited to damage to software, hardware, data, or other losses.

### 5. Disclaimer
##  5.1. The developer of this Program is not affiliated with Changan Auto or its subsidiaries. All rights to trademarks, logos, and other intellectual property related to Changan cars belong to their respective owners.
##  5.2. The Program is provided "as is," and the developer makes no warranties, express or implied, regarding its functionality or suitability for specific purposes.

### 6. Changes to the Agreement
The developer reserves the right to change the terms of this Agreement at any time. Changes take effect from the moment the updated version of the Agreement is published on the website or in the Program.

### 7. Contact Information
All questions regarding the use of the Program can be sent to the email address changan_install@humanbait.ru.

### 8. Applicable Law
By using the Program, you confirm that you have read, understood, and agree to the terms of this Agreement.

Last updated: 09.08.2024
{Cl.green}Y: Agree {Cl.reset}| {Cl.red}Any key: Close the application {Cl.reset}
"""
