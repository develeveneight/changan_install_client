from getpass import getpass

from helpers.server import User
from helpers import helper
from helpers.logger import Cl, log

user = User()


class ClientMenu:
    def __init__(self):
        self.lang = helper.set_language()

    @staticmethod
    def munit(hotkey, message):
        return print(f"{Cl.magenta}{hotkey}{Cl.reset} | {message}")

    # @staticmethod
    # def auth_menu(credentials: dict):
    #     user_data = user.authenticate(credentials[0], credentials[1])
    #     if 'error' in user_data:
    #         return user_data['message']
    #     else:
    #         return user_data

    def reg_auth_menu(self):
        # TODO reformat auth menu
        email = input(self.lang.EMAIL)
        password = getpass(self.lang.PASSWORD)
        return email, password

        # return user.registration(email, password)

    # def no_vehicle_access(self):
    #     helper.clear_screen()
    #     print(f"{Cl.yellow}You don't have access to install apps in any vehicle")
    #     self.munit(1, "Get access to installation for 1 vehicle")
    #     self.munit(0, "Exit")
    #     return input("Select a menu item: ")

    # def buy_car_access_menu(self):
    #     helper.clear_screen()
    #     print(f"{Cl.yellow}You don't have access to install apps in any vehicle")

    # def main_23(self):
    #     helper.clear_screen()
    #     print(en.APP_TITLE.format("2023 (no root)"))
    #     print(en.INSTALL_WARNING_23)
    #
    #     print(f"{Cl.magenta}(1){Cl.reset} Prepare environment")
    #
    #     choice = input("\nSelect a menu item: ")
    #     helper.clear_screen()
    #     return choice

    def create(self, title: str, menu_items: dict, description: str = None, title_color=Cl.magenta):
        """
        Menu creation method
        :param title: Title of the menu
        :param menu_items: items in dict type "0": menu item, where 0 - key for activating
        :param description: description of the menu
        :param title_color: for changing color of the title
        :return: user choice
        """
        # calculate title length
        title_len = len(title)
        offset_len = 30
        line_len = offset_len + title_len
        offset = " " * int(offset_len / 2)
        new_title = offset + title + offset
        title_line = "-" * int(line_len)

        helper.clear_screen()
        print(f"{title_color}{title_line}")
        print(f"{new_title}")
        print(f"{title_line}{Cl.reset}")
        if description:
            print(f"{description}")
            print(title_line)
        menu_offset = 3
        for key, value in menu_items.items():
            fixed_offset = menu_offset - int(len(str(key)))
            print(f"{Cl.magenta}{key}{Cl.reset}{' ' * fixed_offset}#  {value}")
        choice = input(self.lang.SELECT_MENU_ITEM)
        return choice


if __name__ == '__main__':
    menu = ClientMenu()
    menu.create("Test menu", menu_items={"1": "item 1"})
