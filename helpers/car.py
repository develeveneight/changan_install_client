import os
import time

from helpers.adb import Adb
from helpers.logger import Cl
from helpers import helper

adb = Adb()


class Changan:
    def __init__(self):
        self.emulator = True
        self.customs_path = '/data/_customs/'  # TODO: archived. Delete
        self.app_path = '/system/app'  # TODO: archived. Delete
        self.apk_path = 'apk'
        self.apk_data_file = "installed_apks.json"  # TODO: archived. Delete
        self.signed_apks_path = f"{self.apk_path}/signed"  # TODO: archived. Delete
        self.decompiled_apks_path = f"{self.apk_path}/decompiled"  # TODO: archived. Delete
        self.lang = helper.set_language()

    @staticmethod
    def get_apks(headunit_uid: bool = False, user_apps: bool = True) -> list:
        # TODO: Get installed apps from server
        """
        Get all packages from HU
        :param headunit_uid:
        :param user_apps:
        :return:
        """
        if not headunit_uid:
            # get all apps from HU
            apk_data_raw_list = adb.shell(['pm', 'list', 'packages', '-f']).split('\n')
            if user_apps:
                apps_raw = [user_package for user_package in apk_data_raw_list
                            if len(user_package.split('/')) > 1 and user_package.split('/')[1] == "data"]
            else:
                apps_raw = [user_package for user_package in apk_data_raw_list
                            if len(user_package.split('/')) > 1]

            # print(user_apps_raw)
            app_data = []
            for user_app in apps_raw:
                user_app_data_raw = user_app.split('apk')
                user_app_path = user_app_data_raw[0].split(":")[1] + "apk"
                user_app_package_name = user_app_data_raw[1][1:]
                app_data.append((user_app_path, user_app_package_name))
            return app_data

    @staticmethod
    def get_disabled_apks() -> list:
        """
        Get all disabled apks from HU
        :return:
        """
        disabled_apks_list_raw = adb.shell(['pm', 'list', 'packages', '-d', '-f']).split('\n')
        user_apps_raw = [user_package for user_package in disabled_apks_list_raw
                         if len(user_package.split('/')) > 1 and user_package.split('/')[1] == "data"]
        # print(user_apps_raw)
        app_data = []
        for user_app in user_apps_raw:
            user_app_data_raw = user_app.split('apk')
            user_app_path = user_app_data_raw[0].split(":")[1] + "apk"
            user_app_package_name = user_app_data_raw[1][1:]
            app_data.append((user_app_path, user_app_package_name))
        return app_data

    def disable_apks(self, user_apks: dict | None = None):
        """
        Disable apks in HU
        :param user_apks:
        :return:
        """
        print(self.lang.DISABLING_APKS)
        if user_apks:
            for user_apk in user_apks:
                adb.shell(['pm', 'disable-user', user_apk['package_name']])
        else:
            user_apks = self.get_apks()
            for user_apk in user_apks:
                adb.shell(['pm', 'disable-user', user_apk[1]])
        print(self.lang.MSG_DONE)
        time.sleep(2)

    def enable_apks(self):
        """
        Enable all apks in HU
        :return:
        """
        print(self.lang.ENABLING_APKS)
        user_apks = self.get_disabled_apks()
        for user_apk in user_apks:
            adb.shell(['pm', 'enable', user_apk[1]])
        print(self.lang.MSG_DONE)
        time.sleep(2)

    def get_apk_list(self):
        """
        Get all apk files in "apk" folder
        :return:
        """
        items = os.listdir(self.apk_path)
        apk_file_list = [file_name for file_name in items if
                         os.path.isfile(os.path.join(self.apk_path, file_name)) and file_name != '.gitignore']
        return apk_file_list

    @staticmethod
    def show_free_space():
        """
        Show free space in HU with color alerts
        :return:
        """
        result = adb.shell(['df', '-h']).split('\n')

        # delete title row
        result = result[1:]

        # Create dict with full parameters
        space_data = {}
        for line in result:
            if line:
                params_list = line.split()

                if ('/' == params_list[-1] or '/data' == params_list[-1] or 'user_data' == params_list[-1] or
                    'emulated' in params_list[-1]):

                    color = Cl.reset
                    if int(params_list[4].replace("%", "")) > 70:
                        color = Cl.yellow
                    if int(params_list[4].replace("%", "")) > 80:
                        color = Cl.red

                    mount = ""
                    if params_list[-1] == "/":
                        params_list[-1] = "Root"
                    if params_list[-1] == "/user_data":
                        params_list[-1] = "User Data"
                    if params_list[-1] == "/data":
                        params_list[-1] = "Data"
                    if "emulated" in params_list[-1]:
                        params_list[-1] = "Internal Emulated"

                    print(f"{Cl.blue}{params_list[-1]}{Cl.reset} size {params_list[1]} | "
                          f"free {params_list[3]} | used {color}{params_list[4]}")
        helper.continue_on_any_key()

    def clear_launcher_data(self):
        """
        Clear launcher data and cache
        :return:
        """
        apks = self.get_apks(user_apps=False)
        for apk in apks:
            # print(apk[1])
            if 'launcher' in apk[1]:
                adb.shell(['pm', 'clear', apk[1]])

    @staticmethod
    def get_partitions_data() -> list:
        """
        Get partitions data from HU
        :return: [{'name','path'},]
        """
        partitions_str = adb.shell(['ls', '-lR', '/dev/block/'], debug=False).split('total 0')
        partitions_list = partitions_str[-2]
        partitions_list = partitions_list.split('\n')

        partitions_data = []
        for partition_raw in partitions_list:
            data = partition_raw.split(" ")
            if len(data) > 3:
                partitions_data.append(
                    {
                        'name': data[7],
                        'path': data[-1],
                    }
                )
        return partitions_data

    def dump_partitions(self, name: str, path):
        """
        Dump partitions data to disk
        :param name: path for saving dump
        :param path: partition path
        :return:
        """
        print(self.lang.DUMP_MSG_START.format(path))
        adb.execute(['pull', path, name])
        print(self.lang.MSG_DONE)
        helper.continue_on_any_key()


if __name__ == '__main__':
    ch = Changan()
    adb.adb_path = "../tools/adb.exe"

    # print(ch.get_partitions_data())
    # adb.execute(['pull', '/dev/block/sda', './'])
    ch.dump_partitions('sda1', '/dev/block/sda')
