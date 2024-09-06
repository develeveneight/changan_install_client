import os.path
import subprocess
import time
from dotenv import load_dotenv

from helpers import helper
from helpers.logger import Cl, log
from sys import exit

load_dotenv()
INSTALL_METHOD = os.getenv("INSTALL_METHOD")
ADB_PASSWORD = os.getenv("ADB_PASSWORD")


# TODO: Add docstring dor methods
class Adb:
    def __init__(self):
        self.adb_status = False
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.adb_path = os.path.join('adb')
        self.lang = helper.set_language()

    def set_adb_path(self, path):
        current_path = os.environ.get('PATH', '')
        os.environ['PATH'] = f'{current_path};{path}'

    def execute(self, command: list | str, debug=False):
        args_list = [str(self.adb_path)]
        # args_list = ['adb.exe']
        if isinstance(command, list):
            args_list.extend(command)
        else:
            args_list.append(command)
        try:
            if INSTALL_METHOD == "adb":
                result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = result.stdout, result.stderr
            else:
                cmd = f'echo adb{ADB_PASSWORD} | {self.adb_path} '
                if isinstance(command, list):
                    for el in command:
                        cmd += f"{el} "
                else:
                    cmd += command
                # print(cmd)
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if debug:
                print(result)
            if result.returncode == 0:
                # print(result.stdout)
                return result.stdout
            else:
                # print(result.stderr)
                return False
        except Exception as e:
            print(e)
            return False

    def shell(self, command: list | str, debug=False):
        args_list = ['shell']
        if isinstance(command, list):
            args_list.extend(command)
        else:
            args_list.append(command)
        return self.execute(args_list, debug=debug)

    def push(self, _from, _to):
        if _to[0] != "/":
            print("[_to]:Wrong path start. Must start from /")
            exit()

        args_list = ['push', _from, _to]
        return self.execute(args_list)

    def create_symlink(self, current_path, destination_path):
        args_list = ['ln -s']
        args_list.extend([current_path, destination_path])
        self.shell(args_list)

    def wait_device(self):
        helper.clear_screen()
        timer = 0
        device_id = None
        print(self.lang.WAITING_DEVICE)

        while not device_id:
            device_id = self.device_id(self.execute(['devices']))
            helper.clear_screen()
            if 0 < timer < 30:
                print(f"{self.lang.WAITING_DEVICE}({timer})")
            elif timer >= 30:
                log(self.lang.CONNECT_ERROR.format(Cl.red, Cl.reset))
                helper.exit_on_any_key()
            timer += 1
            time.sleep(1)
        log(self.lang.DEVICE_IS_CONNECT.format(Cl.green))
        time.sleep(1)

    def check_connect(self):
        device_id = self.device_id(self.execute(['devices']))
        if not device_id:
            print("Connect lost`")
            helper.exit_on_any_key()

    @staticmethod
    def device_id(stdout):
        stdout = stdout.split("\n")
        # print(stdout)
        if not stdout[1]:
            return False
        else:
            device_id = stdout[1].split("\t")[0]
            return device_id

    def path_exists(self, path):
        stdout = self.shell(['ls', '-la', path])
        if stdout is False:
            return False
        # if "No such file or directory" in stdout:
        #     return False
        return True

    def get_system_app(self, size_limit=1000):
        system_apps_data = {}
        stdout = self.shell(['ls', '-la', '/system/app'])
        apps_list = stdout.split("\n")[3:-1]
        for app_data in apps_list:
            # print(app_data)
            app_name = app_data.split()[-1]
            app_folder_path = f'system/app/{app_name}'
            # check app size
            app_folder_data = self.shell(['ls', '-l', app_folder_path])
            total_size = app_folder_data.split('\n')[0].replace('total ', '')
            if int(total_size) <= size_limit:
                # return full app_path
                print(f'{Cl.black}Get system app  {app_name}.apk{Cl.reset}')
                return f'/system/app/{app_name}/{app_name}.apk'

    def search_package(self, package_name):
        app_list = []
        stdout = adb.shell(['pm', 'list', 'packages']).split("\n")
        for line in stdout:
            if package_name in line:
                return True
        return False

    def verity_status(self, stdout):
        stdout = stdout.split("\n")
        if (
            stdout[0] == "disable-verity only works for userdebug builds" or
            stdout[0] == "Failed to read fstab"
        ):
            log(self.lang.DISABLE_VERITY_OFF)
        else:
            log(self.lang.DISABLE_VERITY_STATUS + self.lang.MSG_OK)

    def root_status(self, stdout):
        # TODO: replace strings by lang package variables
        stdout = stdout.split("\n")
        if stdout[0] == "adbd is already running as root":
            log(f"Root: - [{Cl.green}OK{Cl.reset}]")
            return True
        elif stdout[0] == "restarting adbd as root":
            log(self.lang.ROOT_STATUS.format(self.lang.MSG_DONE))
            log(f"Root: - [{Cl.green}OK{Cl.reset}]")
            return True
        else:
            log(self.lang.ROOT_STATUS.format(self.lang.MSG_FALSE))
            return False


if __name__ == '__main__':
    adb = Adb()
    # adb.get_system_app()

    adb_directory = os.path.join(adb.root_path, '..', 'tools')
    adb.set_adb_path(adb_directory)
    # print(adb_directory)
    # current_path = os.environ.get('PATH', '')
    # os.environ['PATH'] = f'{current_path};{adb_directory}'

    print(adb.shell('ls -la /'))
