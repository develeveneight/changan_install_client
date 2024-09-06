import argparse
import base64
import os
import platform
import shutil
import subprocess
from os.path import join, exists
import time

from helpers.car import Changan
from helpers.logger import Cl, log
from helpers.menus import ClientMenu
from helpers.adb import Adb
from helpers.server import Certificate, Car, Apk, Job, Payment, User, ServerInfo
from helpers import helper
from sys import exit

adb = Adb()
certificate = Certificate()
apk = Apk()
car = Car()
job = Job()
payment = Payment()
user = User()
server_info = ServerInfo()


class Client:
    """
    Changan Install client app Main Class
    """

    def __init__(self):
        self.menu = ClientMenu()
        self.system_app_list = [('/system/priv-app', 'Dialer.apk'), ('/system/app', 'Bluetooth'),
                                ('/system/priv-app', 'SettingsProvider')]
        # TODO: check android version via getprop
        self.changan = Changan()
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.temp_path = join(self.root_path, 'temp')
        self.headunit_uid = None
        if platform.system() == 'Windows':
            self.settings_path = os.path.join(os.getenv('LOCALAPPDATA'), 'changan_install')
        elif platform.system() == 'Linux':
            self.settings_path = os.path.join(os.getenv('HOME'), '.changan_install')
        self.token_path = os.path.join(self.settings_path, 'token')
        self.eula_path = os.path.join(self.settings_path, 'EULA')
        self.token = None
        self.user = {}
        self.cars = {}
        self.lang = helper.set_language()
        self.app_init()
        self.internal_path = "/storage/emulated/0"
        if platform.system() == "Windows":
            self.tools_path = join(self.root_path.replace("\\tmp", ""), 'tools')
            adb.set_adb_path(self.tools_path)

    def app_init(self):
        """
        Simple checks
        :return:
        """
        if os.getenv('SERVER_API_URL') == "" or os.getenv('SERVER_PUBLIC_URL') == "" or os.getenv('LANG') == "":
            print(".env ERROR")
            helper.exit_on_any_key()
        url_checked = server_info.check_url()
        if url_checked != 200:
            print("URL ERROR")
            helper.exit_on_any_key()
        if not os.path.exists('tools'):
            print(os.path.exists(join(self.root_path, 'tools')))
            print("tools folder does not exist")
            helper.exit_on_any_key()
        if not os.path.exists('apk'):
            print("apk folder does not exist")
            helper.exit_on_any_key()

    def gen_eula_file(self):
        """
        EULA agreement file create
        :return:
        """
        if not os.path.exists(self.eula_path):
            with open(self.eula_path, 'w') as f:
                f.write("0")

    def eula_status(self):
        """
        Read EULA status from EULA settings file
        :return:
        """
        if os.path.exists(self.eula_path):
            with open(self.eula_path, 'r') as f:
                return int(f.readline().strip())
        else:
            return 0

    def update_eula_status(self, status: int):
        """
        Update EULA status in EULA settings file
        :param status: (int) status of EULA agreement 0 - false, 1 - true
        :return:
        """
        with open(self.eula_path, 'w') as f:
            f.write(str(status))

    def show_eula(self):
        """
        Show EULA on the screen
        :return:
        """
        if self.eula_status() == 0:
            choice = self.menu.create(
                self.lang.USER_LICENSE_TITLE,
                {},
                description=self.lang.USER_LICENSE
            )
            if choice not in ['Y', 'y']:
                exit()
            else:
                self.update_eula_status(1)

    def load_local_credentials(self):
        """
        Load local credentials from token file
        :return:
        """
        if os.path.exists(self.token_path):
            with open(self.token_path, 'r') as f:
                line = f.readline().strip()
                credentials = line.split(":")
                self.token = credentials[2]
                return {
                    'email': credentials[0],
                    'password': credentials[1],
                    'token': credentials[2]
                }
        else:
            print(f"Token file not found. Can't load credentials.")
            return None

    def save_local_credentials(self, email: str, password: str, token=None):
        """
        Save credentials to local file
        :param email: User email
        :param password: password
        :param token: server access token
        :return:
        """
        with open(self.token_path, 'w') as f:
            f.write(f"{email}:{password}:{token}")

    def prepare_folders(self):
        """
        Create folders for local settings
        :return:
        """
        if not os.path.exists(self.settings_path):
            # print(self.settings_path)
            os.makedirs(self.settings_path)

    def pull_app_from_hu(self, tmp_path: str) -> str | bool:
        """
        Pull system app from HU
        :param tmp_path: temp path for pulling
        :return: (str | bool) Name of the system apk file, or False if not found with client filters
        """
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)

        for system_app in self.system_app_list:
            # Check if exists
            log(f"Finding {system_app[1]}")
            app_path = f'{system_app[0]}/{system_app[1]}'
            if adb.path_exists(app_path):
                if system_app[1] == "Dialer.apk":
                    adb.execute(['pull', f'{system_app[0]}/{system_app[1]}', tmp_path])
                    return system_app[1]
                else:
                    adb.execute(['pull', f'{system_app[0]}/{system_app[1]}/{system_app[1]}.apk', tmp_path])
                    return system_app[1] + '.apk'
            # else:
            #     # cannot find system apps from system_app_list
            #     print("Necessary system files not found")
            #     helper.exit_on_any_key()
            else:
                log(f"Finding small system app...")
                # get first app with <= 5mb size
                little_system_app = adb.get_system_app()
                if little_system_app:
                    adb.execute(['pull', little_system_app, tmp_path], debug=False)
                    return little_system_app.split("/")[-1]

        # cannot find system apps
        print("Necessary system files not found")
        helper.exit_on_any_key()
        return False

    @staticmethod
    def get_headunit_uid() -> str:
        """
        Generate Headunit UID
        :return: (str) Headunit UID
        """
        serial_number = adb.shell(['getprop', 'ro.serialno']).strip()
        device_id = adb.device_id(adb.execute(['devices']))
        headunit_uid_str = serial_number + device_id
        encoded_bytes = base64.b64encode(headunit_uid_str.encode("utf-8"))
        return encoded_bytes.decode("utf-8")

    def car_identify(self):
        """
        Create car identity row in DB [id, hu_uid, root, etc.]
        :return:
        """
        print(self.lang.CAR_PREPARE)
        # Car exists in db check
        self.headunit_uid = self.get_headunit_uid()
        car_exists = car.get_car_by_headunit_uid(self.headunit_uid)
        car_data = {}

        if not car_exists:
            # Create Car data dictionary

            # Get unique uid for car
            car_data['headunit_uid'] = self.headunit_uid

            # Root status
            car_data['root'] = 1 if adb.root_status(adb.execute('root')) else 0

            # Send car data to server
            car.save_car_data(car_data)

    def certificate_prepare(self):
        """
        Prepare certificate for signing.
        - Get parameters from system app certificate
        - Upload on the server
        - Waiting for certificate to be generated on the server side
        :return:
        """
        print(self.lang.CERT_PREPARE)
        cert_data = certificate.get_parameters(self.headunit_uid)
        if not cert_data:
            if not exists(self.temp_path):
                os.mkdir(self.temp_path)

            # pull system app
            system_cert_app = self.pull_app_from_hu(self.temp_path)

            if system_cert_app:
                log(f"Uploading {system_cert_app}...")

                system_app_path = join(self.temp_path, system_cert_app)
                if os.path.exists(system_app_path):
                    with open(system_app_path, "rb") as system_app:
                        # upload system app for watcher work
                        response = certificate.upload_system_app(self.headunit_uid, system_app)
                        print(response['msg']) if 'msg' in response else None
                        if response['error'] == 1:
                            helper.exit_on_any_key()
                else:
                    print("Error pulling system app from Headunit")
                    helper.exit_on_any_key()

                # Check certificate status
                log(f"Waiting for creating certificate...")
                cert_creating = True
                while cert_creating:
                    certificate_data = certificate.get_parameters(self.headunit_uid)
                    if certificate_data:
                        cert_creating = False
                    time.sleep(1)

                # Delete temp folder
                if os.path.exists(self.temp_path):
                    shutil.rmtree(self.temp_path)
        print(f"[{Cl.green}OK{Cl.reset}]")

    def car_menu(self, car_data: dict):
        """
        Main Menu
        :param car_data: saved car data from DB [id, cert_id, serial_id, user_id, hu_uid, etc.]
        :return:
        """
        root = bool(car_data['root'])
        description = ""
        menu_items = {}
        if not car_data['uid']:
            menu_items["B"] = f"{Cl.yellow}Buy access{Cl.reset}"
            menu_items["0"] = self.lang.INSTALL_FREE

        menu_items.update({
            "1": self.lang.INSTALL_FROM_FOLDER,
            "2": self.lang.INSTALL_HUR,
            "3": self.lang.INSTALL_KIT,
            "4": self.lang.CLEAR_CACHE,
            "5": self.lang.SHOW_FREE_SPACE,
            "6": self.lang.OPEN_SYSTEM_SETTINGS,
            "H": self.lang.HIDE_ALL_APPS,
            "S": self.lang.SHOW_ALL_APPS,
            'R': self.lang.RENAME_CAR,
            '00': self.lang.SERVICE_MENU
        })
        if not root:
            description += self.lang.INSTALL_WARNING_NO_ROOT
        else:
            pass
        if not car_data['uid']:
            description += self.lang.BUY_ACCESS_MESSAGE
        menu_items["X"] = self.lang.EXIT

        choice = self.menu.create(
            self.lang.MAIN_MENU_TITLE.format(car_data['name']),
            description=description,
            menu_items=menu_items
        )
        helper.clear_screen()
        adb.check_connect()
        if choice in ["B", "b"] and not car_data['uid']:
            # Buy access
            self.buy_access(car_data['headunit_uid'])
        elif choice in ["R", "r"]:
            # Rename car
            self.rename_car(car_data['headunit_uid'])
        elif choice in ["H", "h"] and self.changan.get_apks():
            # Hide apks
            installed_apks = apk.get_installed_apk(self.headunit_uid)
            self.changan.disable_apks(installed_apks)
        elif choice in ["S", "s"] and self.changan.get_disabled_apks():
            # Show disabled apks
            self.changan.enable_apks()
        elif choice in ["X", "x"]:
            exit()

        elif choice == "0":
            choice = self.menu.create(
                self.lang.FREE_TITLE,
                {
                    "1": "X-plore",
                    "0": self.lang.RETURN_TO_MAIN_MENU
                },
                description=self.lang.FREE_DESCRIPTION
            )
            if choice == "1":
                self.install_apk('xplore')
            elif choice == "0":
                pass

        elif choice == "1":
            # install from apk folder
            choice = self.menu.create(
                self.lang.WARNING,
                {
                    "1": self.lang.CONTINUE,
                    "2": self.lang.RETURN_TO_MAIN_MENU
                },
                description=self.lang.INSTALL_FROM_APK_TITLE,
                title_color=Cl.red
            )
            if choice == "1":
                self.install_from_apk_folder(car_data['headunit_uid'])
            elif choice == "2":
                pass

        elif choice == "2":
            print(self.lang.HUR_INSTALLING)
            self.install_apk('hur')

        elif choice == "3":
            choice = self.menu.create(
                self.lang.WARNING,
                {
                    "1": self.lang.CONTINUE,
                    "2": self.lang.RETURN_TO_MAIN_MENU
                },
                description=self.lang.KIT_MENU_DESCRIPTION,
                title_color=Cl.red
            )
            if choice == "1":
                print(self.lang.KIT_INSTALLING)
                # Install AutoKit
                self.install_apk('kit')
            elif choice == "2":
                pass

        elif choice == "4":
            self.changan.clear_launcher_data()
        elif choice == "5":
            self.changan.show_free_space()
        elif choice == "6":
            adb.shell(['am', 'start', '-a', 'android.settings.SETTINGS'])
            choice = self.menu.create(
                self.lang.SETTINGS_TITLE,
                {
                    '1': self.lang.SETTINGS_SYSTEM,
                    '2': self.lang.SETTINGS_EXIT
                },
                description=self.lang.SETTINGS_DESCRIPTION,
            )
            if choice == "2":
                adb.shell(['input', 'keyevent', 'KEYCODE_HOME'])
            elif choice == "1":
                adb.shell(['am', 'start', '-n', 'com.android.settings/.Settings\$SystemDashboardActivity'])
                choice = self.menu.create(
                    self.lang.SETTINGS_TITLE,
                    {
                        '1': self.lang.SETTINGS_EXIT
                    },
                )
                if choice == "1":
                    adb.shell(['input', 'keyevent', 'KEYCODE_HOME'])
        elif choice == "00":
            # TODO: Make new method with Service Menu
            menu_item = {'1': self.lang.SERVICE_PACKAGES_DELETE}
            if platform.system() == "Windows":
                menu_item['2'] = self.lang.SERVICE_ADB_CONSOLE.format("PowerShell")
            elif platform.system() == "Linux":
                menu_item['2'] = self.lang.SERVICE_ADB_CONSOLE.format(os.getenv('LINUX_TERMINAL_APP', 'gnome-terminal'))
            menu_item['3'] = self.lang.SERVICE_SAVE_CERT
            if car_data['root'] == 1:
                menu_item['4'] = self.lang.SERVICE_DUMP
            menu_item['0'] = self.lang.RETURN_TO_MAIN_MENU
            choice = self.menu.create(
                self.lang.SERVICE_TITLE,
                menu_item,
                description=self.lang.SERVICE_DESCRIPTION,
                title_color=Cl.red
            )
            # TODO: filter menu elements by root or not
            if choice == "1":
                self.reset_packages(car_data)
            elif choice == "2":
                print(self.lang.MSG_TERMINAL_EXIT)
                if platform.system() == "Windows":
                    subprocess.Popen(
                        ["powershell", "-NoExit", "-Command", "Start-Process", "powershell", "-ArgumentList",
                         "'-NoExit'"])
                elif platform.system() == "Linux":
                    subprocess.Popen([os.getenv('LINUX_TERMINAL_APP', 'gnome-terminal'), '--', 'bash', '-c', 'bash'])
            elif choice == "3":
                os_prop = adb.shell(['getprop', 'ro.build.display.id'])
                version_date = adb.shell(['getprop', 'ro.build.version.incremental'])
                cert_url = certificate.download(self.headunit_uid, os_prop, version_date)
                helper.clear_screen()
                print(self.lang.MSG_CERT_DOWNLOAD_COMPLETE.format(cert_url))
                helper.continue_on_any_key()
            elif choice == "4" and car_data['root'] == 1:
                self.dump_menu()

        helper.clear_screen()
        car_data = car.get_car_by_headunit_uid(self.headunit_uid)
        self.car_menu(car_data)

    def dump_menu(self):
        """
        Dump Menu
        :return:
        """
        dump_path = join(self.tools_path, 'dump')
        if not os.path.exists(dump_path):
            os.mkdir(dump_path)

        helper.clear_screen()
        partitions: list = self.changan.get_partitions_data()
        partition_menu = {}
        for idx, partition in enumerate(partitions):
            partition_menu[idx] = partition['name']
        partition_menu['X'] = self.lang.RETURN_TO_MAIN_MENU
        choice = self.menu.create(
            self.lang.DUMP_TITLE,
            partition_menu,
            self.lang.DUMP_DESCRIPTION
        )
        for idx, partition in enumerate(partitions):
            if choice == str(idx):
                partition_path = join(dump_path, partition['name'])
                self.changan.dump_partitions(partition_path, partition['path'])
        if choice in ["X", "x"]:
            self.car_menu(car.get_car_by_headunit_uid(self.headunit_uid))
        self.dump_menu()

    def buy_access(self, headunit_uid: str):
        """
        Payment Service
        :param headunit_uid: unique uid from car_data
        :return:
        """
        payment_data = payment.create_payment(headunit_uid)
        payment_id = payment_data['id']
        print(self.lang.OPEN_BROWSER_DESCRIPTION)
        payment_url = payment_data['confirmation']['confirmation_url']
        print(payment_url)
        print(self.lang.PAYMENT_WAIT)

        payment_succeeded = False
        while not payment_succeeded:
            # Waiting for payment
            payment_status_data = payment.get_payment_status(self.user['id'], payment_id)
            if payment_status_data:
                payment_status = payment_status_data['status']
                payment_succeeded = True if payment_status == 'succeeded' else False
            time.sleep(5)
        else:
            print(self.lang.PAYMENT_SUCCESS.format(Cl.green, Cl.reset))
            helper.continue_on_any_key()

    def car_select(self):
        # TODO: archived method
        if self.cars:
            if len(self.cars) > 1:
                # have more than one car
                car_items = {}
                # Show car menu
                for car_item in self.cars:
                    car_items[car_item['id']] = car_item['name']
                choice = self.menu.create(self.lang.SELECT_CAR, car_items)

                cars_count = len(self.cars)
                # create menu for a selected car
                self.car_menu(self.cars[int(choice) - 1])

                # for car_number in range(1, cars_count + 1):
                #     self.car_menu(self.cars[car_number - 1])
            else:
                # one car only. Show car menu for specific car
                self.car_menu(self.cars[0])

    def universal_install(self, temp_path: str):
        """
        Main install method
        :param temp_path: apk path
        :return:
        """
        adb_password = os.getenv("ADB_PASSWORD")
        install_method = os.getenv("INSTALL_METHOD")
        if install_method == "adb":
            # adb install
            print("ADB install")
            adb.execute(['install', temp_path])
        elif install_method == "pm":
            print('SHELL install')
            # get apk_name
            apk_name = temp_path.split('\\')[-1]
            full_internal_apk_path = f"{self.internal_path}/{apk_name}"
            # pm install
            adb.execute(['push', temp_path, self.internal_path])
            if adb_password != "":
                adb.shell(f'adb{adb_password}')
            adb.shell(['pm', 'install', full_internal_apk_path])
            adb.shell(['rm', full_internal_apk_path])

    def install_from_apk_folder(self, headunit_uid: str):
        """
        Install from "apk" folder
        :param headunit_uid: unique uid from car_data
        :return:
        """
        print(self.lang.INSTALL_FROM_FOLDER_MSG)
        # Get list with apk files path
        apk_path_list = [os.path.join(self.changan.apk_path, file_path) for file_path in self.changan.get_apk_list()]

        # Upload apk files to server
        job_response = apk.upload(apk_path_list, headunit_uid)

        # check new job to sign apks
        if not job_response:
            print(self.lang.MSG_ACCESS_ERROR.format(Cl.red, Cl.reset))
            helper.continue_on_any_key()
        else:
            job_id = job_response['id']
            job_status = 0
            while job_status == 0:
                job_data = job.get(job_id)
                job_status = job_data['status']
                time.sleep(5)

            apk_name_list = self.changan.get_apk_list()
            public_url = os.getenv('SERVER_PUBLIC_URL')
            for apk_name in apk_name_list:
                # Download
                full_url = f"{public_url}/{headunit_uid}/signed/{apk_name}"
                temp_signed_path = join(job.settings_path, apk_name)
                helper.download_file(full_url, temp_signed_path)

                # Install
                # Get user package list before install
                apk_data_list = self.changan.get_apks()
                self.universal_install(temp_signed_path)
                new_apk_data_list = self.changan.get_apks()
                installed_apk_data = list(set(new_apk_data_list) - set(apk_data_list))

                # Save apk data to db
                if installed_apk_data:
                    apk.save_data(installed_apk_data[0][1], installed_apk_data[0][0], self.headunit_uid)

                # Remove temp folders and files
                os.remove(temp_signed_path)

                print(self.lang.MSG_DONE)
                time.sleep(2)

    def install_apk(self, apk_name: str):
        """
        Install concrete app from menu
        :param apk_name: apk name in server short format
        :return:
        """
        job_response = apk.install(self.headunit_uid, apk_name)
        if not job_response:
            print(self.lang.MSG_ACCESS_ERROR)
            helper.continue_on_any_key()
            # self.car_menu(car.get_car_by_headunit_uid(self.headunit_uid))
        else:
            # print(job_response)
            job_id = job_response['id']
            job_status = 0
            while job_status == 0:
                job_data = job.get(job_id)
                job_status = job_data['status']
                time.sleep(5)

            # Download
            public_url = os.getenv('SERVER_PUBLIC_URL')
            full_url = f"{public_url}/{self.headunit_uid}/signed/{apk_name}.apk"
            temp_signed_path = join(job.settings_path, f"{apk_name}.apk")
            helper.download_file(full_url, temp_signed_path)

            # Install
            # Get user package list before install
            apk_data_list = self.changan.get_apks()
            # adb.execute(['install', temp_signed_path])
            self.universal_install(temp_signed_path)
            new_apk_data_list = self.changan.get_apks()
            installed_apk_data = list(set(new_apk_data_list) - set(apk_data_list))

            # Save apk data to db
            if installed_apk_data:
                apk.save_data(installed_apk_data[0][1], installed_apk_data[0][0], self.headunit_uid)

            # Remove
            os.remove(temp_signed_path)
            print(self.lang.MSG_DONE)
            time.sleep(2)

    def rename_car(self, headunit_uid: str):
        """
        Rename Car in Main Menu Title
        :param headunit_uid: unique uid from car_data
        :return:
        """
        name = input(self.lang.RENAME_CAR_MSG)
        if name == "":
            self.rename_car(headunit_uid)
        car.rename(headunit_uid, name)

    def reset_packages(self, car_data: dict):
        """
        Delete packages.xml for resetting install information
        :param car_data: car_data from DB [id, cert_id, serial_id, user_id, etc.]
        :return:
        """
        if car_data['root'] == 1:
            adb.shell(['rm', '-rf', '/data/system/packages.xml'])
            print(self.lang.MSG_OK)
            time.sleep(2)
        else:
            # magisk_installed = adb.search_package('com.topjohnwu.magisk')
            # if magisk_installed:
            #     adb.shell(['su'])
            #     print("Accept root on the HU screen")
            #     time.sleep(2)
            #     adb.shell(['remount'])
            #     adb.shell(['su', '-c', '"rm /data/system/packages.xml"'])
            print("Root needed")
            helper.continue_on_any_key()

    def signup(self, email: str, password: str):
        """
        Sign up new user
        :param email: email
        :param password: password
        :return:
        """
        user_data = user.registration(email, password)
        self.save_local_credentials(email, password, user_data['token'])
        return user_data

    def auth(self):
        """
        Auth user
        :return:
        """
        credentials = self.load_local_credentials()
        if not credentials:
            email, password = self.menu.reg_auth_menu()
            # Sign up
            user_data = user.authenticate(email, password)
            if 'error' in user_data:
                user_data = self.signup(email, password)
            self.save_local_credentials(email, password, user_data['token'])
        else:
            # Sign in
            user_data = user.authenticate(credentials['email'], credentials['password'])
            if 'error' in user_data:
                # Sign up
                user_data = self.signup(credentials['email'], credentials['password'])
            else:
                self.save_local_credentials(credentials['email'], credentials['password'], user_data['token'])
        return user_data

    def uninstall(self):
        """
        Clear app garbage before deleting the app
        :return:
        """
        shutil.rmtree(self.settings_path)
        print(self.lang.MSG_UNINSTALL)
        helper.exit_on_any_key()

    def start(self):
        """App start method"""
        self.prepare_folders()
        self.show_eula()
        adb.wait_device()
        helper.clear_screen()

        # Authorization
        user_data = self.auth()

        # Prepare models
        self.token = user_data['token']
        certificate.set_token(self.token)
        apk.set_token(self.token)
        car.set_token(self.token)
        job.set_token(self.token)
        payment.set_token(self.token)

        self.user = user_data['user']
        if self.user:
            # Sign is OK
            self.car_identify()
            self.certificate_prepare()
            self.cars = car.get_cars(self.user['id'])

            if not self.user:
                print(self.lang.MSG_CONNECTION_ERROR)
                helper.exit_on_any_key()

            # show car list or menu if onw car owned
            # self.car_select()

            # Load car menu
            car_data = car.get_car_by_headunit_uid(self.headunit_uid)
            self.car_menu(car_data)
        else:
            helper.exit_on_any_key()


if __name__ == '__main__':
    client = Client()
    parser = argparse.ArgumentParser()
    parser.add_argument('-clear', action='store_true', help=client.lang.ARG_CLEAR)
    args = parser.parse_args()

    if args.clear:
        client.uninstall()
    else:

        client.start()
