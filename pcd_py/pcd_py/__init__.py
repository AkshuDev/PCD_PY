import os
import pcd
import time

class run_cmdline():
    def __init__(self, cmd):
        self.cmd = cmd
        if "get changes" in self.cmd.lower():
            self.line = self.cmd.replace("get changes ", "")
            if "dir" in self.line:
                self.line = self.line.replace("dir ", "")
                self.get_changes_dir()
        elif "make sfolder" in self.cmd.lower():
            self.line = self.cmd.replace("make sfolder ", "")
            self.password = ""
            start_index = 0

            while True:
                start_paren_index = self.line.find('(', start_index)
                if start_paren_index == -1:
                    break

                end_paren_index = self.line.find(')', start_paren_index)
                if end_paren_index == -1:
                    break

                extracted_str = self.line[start_paren_index:end_paren_index + 1]
                self.password += extracted_str

                start_index = end_paren_index + 1

            # Remove the parentheses and password from the path
            self.path = self.line.replace(self.password, "").replace("(", "").replace(")", "")

            self.make_sfolder()
        elif "add files sfolder" in self.cmd.lower():
            self.line = self.cmd.replace("add files db ", "")
            self.add_db_type = self.line[self.line.rfind(" ") + 1:]

            self.add_files_sfolder()
        elif "aos cmdline" in self.cmd.lower():
            import aos_cmdline
        elif "create os bootloader" in self.cmd.lower():
            self.line = self.cmd.replace("create os bootloader ", "")
            self.create_bootloader()
        elif "read file" in self.cmd.lower():
            self.line = self.cmd.replace("read file ", "")
            self.read_file()
        elif "write file" in self.cmd.lower():
            self.line = self.cmd.replace("write file ", "")
            self.write_file()
        elif "delete file" in self.cmd.lower():
            self.line = self.cmd.replace("delete file ", "")
            self.delete_file()
        elif "append file" in self.cmd.lower():
            self.line = self.cmd.replace("append file ", "")
            self.append_file()
        elif "make dir" in self.cmd.lower():
            path = self.cmd.replace("make dir ", "")
            try:
                os.mkdir(path)
            except Exception as e:
                print(e)
        elif "make dirs" in self.cmd.lower():
            path = self.cmd.replace("make dirs ", "")
            try:
                os.makedirs(path)
            except Exception as e:
                print(e)
        elif "dir file check" in self.cmd.lower():
            self.line = self.cmd.replace("dir file check ", "")
            self.Dir_file_check()
        elif "pcd" in self.cmd.lower():
            self.line = self.cmd.replace("pcd ", "")
            pcd.Pcd_line("--script --format: .ppcd").run(self.line)
        elif "os" in self.cmd.lower():
            self.line = self.cmd.replace("os ", "")
            self.OS(self.line)

    def read_file(self, *args):
        path = self.line
        if os.path.exists(path) and os.path.isfile(path):
            try:
                with open(path, "r") as file:
                    file.seek(0)
                    return file.read()
            except Exception:
                raise IOError
        elif not os.path.exists(path):
            raise FileNotFoundError
        elif not os.path.isfile(path):
            raise IsADirectoryError
        else:
            raise PermissionError

    def write_file(self, *args):
        path = self.line[:self.line.rfind(" ") + 1]
        content = self.line[self.line.rfind(" ") + 1:]
        if os.path.exists(path) and os.path.isfile(path):
            try:
                with open(path, "w") as file:
                    file.seek(0)
                    file.write(content)
                    return None
            except Exception:
                raise IOError
        elif not os.path.exists(path):
            raise FileNotFoundError
        elif not os.path.isfile(path):
            raise IsADirectoryError
        else:
            raise PermissionError

    def delete_file(self, *args):
        path = self.line
        if os.path.exists(path) and os.path.isfile(path):
            try:
                os.remove(path)
                return None
            except Exception:
                raise IOError
        elif not os.path.exists(path):
            raise FileNotFoundError
        elif not os.path.isfile(path):
            raise IsADirectoryError
        else:
            raise PermissionError

    def append_file(self, *args):
        path = self.line[:self.line.rfind(" ") + 1]
        content = self.line[self.line.rfind(" ") + 1:]
        try:
            with open(path, "a+") as file:
                file.write(content)
                return None
        except Exception:
            raise IOError

    def get_changes_dir(self, *args):
        pass

    def OS(self, cmd="get-os", *args):
        cmd = cmd.lower()
        if cmd == "get-os":
            self.Check_Module("platform", "install")
            import platform
            os_name = platform.system()
            if os_name == "":
                return None
            return os_name


    def Access(self, mode="-w", path="", User_File="all", *args):
        mode = mode.lower()
        modes_avail = ["-r", "-w", "-r/w", "-w/r", "+r/w", "+w/r", "+r", "+w"]
        username = User_File
        if username == "all" or username == "*":
            username = ""
        elif username == "":
            username = ""
        try:
            if mode == "-r/w" or mode == "-w/r":
                os.system(f"icacls \"{path}\" /deny {username}:(RX)")
            elif mode == "-w":
                os.system(f"icacls \"{path}\" /deny {username}:(X)")
            elif mode == "-r":
                os.system(f"icacls \"{path}\" /deny {username}:(R)")
            elif mode == "+r":
                os.system(f"icacls \"{path}\" /grant {username}:(R)")
            elif mode == "+w":
                os.system(f"icacls \"{path}\" /grant {username}:(X)")
            elif mode == "+r/w" or mode == "+w/r":
                os.system(f"icacls \"{path}\" /grant {username}:(RX)")
            else:
                raise "Sorry mode is not identified. Modes available - \n {modes_avail}"

        except Exception:
            raise "Error in Changing Permission! Try running the script in Administrative Mode."

    def make_sfolder(self, *args):
        self.Check_Module("win32api", "secureFolder")
        self.Check_Module("win32gui", "secureFolder")
        self.Check_Module("win32con", "secureFolder")
        self.Check_Module("shutil", "secureFolder")
        self.Check_Module("ctypes", "secureFolder")
        self.Check_Module("platform", "secureFolder")

        import win32api
        import win32gui
        import win32con
        import shutil
        import ctypes
        import platform

        if platform.system() == "Windows":
            try:
                # Check if the script is running with administrative privileges on Windows
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    print("Sorry, but you require Admin Access to run this script")
            except:
                return False
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            # Check if the script is running as the root user on Unix-like systems
            if not os.geteuid() == 0:
                print("Sorry, but you requre Admin Access to run this script.")
        else:
            # Unsupported platform
            print("Sorry, This OS is not supported on Secure Folders.")

        print("Creating PPCD SFolder...")
        print("Initiallizing...")

        mfolder = os.path.join(os.path.join(os.path.relpath(__file__), ".."), "SFolders")
        sf_name = os.path.basename(self.path)

        os.mkdir(os.path.join(mfolder, sf_name))

        sf_dir = os.path.join(mfolder, sf_name)
        print(sf_dir)

        print("Setting Access ...")

        self.Access("-r/w", sf_dir)
        self.Access("+r/w", sf_dir, os.path.join(os.path.join(__file__, ".."), ".."))

        print("Access is set!")

        icon_path = r'C:\\Windows\\system32\\imageres.dll'
        p_dir = os.path.dirname(self.path)
        locker_path = os.path.join(sf_dir, f"security_{sf_name}.py")
        locker_exePath = os.path.join(sf_dir, f'security_{sf_name}.exe')
        lockerSpec_path = f".\\security_{sf_name}.spec"
        lockerNEWspec_Path = os.path.join(sf_dir, f"security_{sf_name}.spec")

        os.mkdir(self.path)

        BatchFile = f"""
        @echo off
        start /min {locker_exePath}
        """
        SecurityFile = f"""
import os
import hashlib

def hash_password(password):
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def lock_folder(folder_path, password_hash):

    # Create a lock file within the folder to simulate locking
    lock_file_path = os.path.join(folder_path, 'lock.txt')

    # Write the hashed password to the lock file
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write(password_hash)

def unlock_folder(folder_path, entered_password):
    # Read the hashed password from the lock file
    lock_file_path = os.path.join(folder_path, 'lock')

    with open(lock_file_path, 'r') as lock_file:
        stored_password_hash = lock_file.read().strip()

    # Hash the entered password for comparison
    entered_password_hash = hash_password(entered_password)

    # Check if the entered password hash matches the stored password hash
    if entered_password_hash == stored_password_hash:
        return True
    else:
        return False

# Example usage
folder_path = '{self.path}'
password = '{self.password}'

# Hash the password
password_hash = hash_password(password)

# Lock the folder
lock_folder(folder_path, password_hash)

# Simulate unlocking with a correct password
entered_password = input("Enter the password to unlock the folder: ")
if unlock_folder(folder_path, entered_password):
    print("Folder unlocked successfully")
else:
    print("Incorrect password. Access denied.")
"""
        print("Initallization of Security File Completed")

        with open(locker_path, "w") as file:
            print("Writing Security file...")
            file.write(SecurityFile)
            print("Security File Written")
            file.close()
            print("Closing Security File")

        os.system(f"pyinstaller --onefile --distpath={os.path.join(p_dir, 'dist')} --workpath={os.path.join(p_dir, 'build')} {locker_path}")
        print("Security File Convertion Completed")
        print('Running Backend...')
        time.sleep(2) #Time Pause
        shutil.rmtree(os.path.join(p_dir, "build"))
        os.rename(lockerSpec_path, lockerNEWspec_Path)
        os.system(f"attrib +h {os.path.join(p_dir, 'dist')}")
        os.system(f"attrib +h {lockerNEWspec_Path}")
        os.remove(locker_path)

        batch_file_path = os.path.join(p_dir, f"{sf_name}.bat")
        with open(batch_file_path, "w") as batch_file:
            batch_file.write(BatchFile)

        desktop_ini_path = os.path.join(self.path, 'desktop.ini')

        with open(desktop_ini_path, 'w') as ini_file:
            ini_file.write('[.ShellClassInfo]\n')
            ini_file.write(f'IconResource={icon_path},2\n')
            ini_file.write('IconFile=%SystemRoot%\\system32\\SHELL32.dll\n')

        try:
            os.rename(desktop_ini_path, desktop_ini_path + '.bak')
            os.rename(desktop_ini_path + '.bak', desktop_ini_path)
            print("Desktop.ini renamed successfully.")
            os.system("copy /b ")
            time.sleep(5)
            win32gui.SendMessageTimeout(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, "Desktop", win32con.SMTO_NORMAL, 1000)
        except OSError as e:
            print(f"Error renaming desktop.ini: {e}")

        # Refresh the folder to apply the changes
        print(f"Your Secure Folder is Ready to Lock the Folder open up the Secure Folder, And to unlock it open the Secure Folder and type the password.")

    def add_files_sfolder(self, *args):
        pass

    def Check_Module(self, moduleName:str, flag:str=""):
        try:
            __import__(moduleName)
            print(f"The module '{moduleName}' is available.")
            return True
        except ImportError:
            print(f"{moduleName} module is not installed.")
            if flag == "secureFolder":
                install_pywin32 = input(f"Do you want to install {moduleName}? (y/n): ").lower()
                if install_pywin32 == 'y':
                    os.system(f"pip install {moduleName}")
                    print(f"{moduleName} installed successfully.")
                else:
                    print(f"{moduleName} is required for creating a Secure Folder. Exiting.")
                    exit()
            elif flag == "Install":
                install_pywin32 = input(f"Do you want to install {moduleName}? (y/n): ").lower()
                if install_pywin32 == 'y':
                    os.system(f"pip install {moduleName}")
                    print(f"{moduleName} installed successfully.")
                else:
                    return False

            if flag == None:
                return False
    def create_bootloader(self, *args):
        if os.path.exists(self.line):
            try:
                with open(os.path.join(self.line, "bootloader.asm"), "a+") as bootloader_file:
                    with open("./bootloader.asm", "r") as BLRead:
                        BLRead.seek(0)
                        bootloader_file.write(BLRead.read())
            except Exception as e:
                print(f"Error PCD 001: \n {e}")
                print("Please check your run command")
        else:
            print("Error PCD 002: No Such File or Directory")

    def Dir_file_check(self, *args):
        dir = self.line
        files = []
        if os.path.exists(dir):
            for file in os.listdir(dir):
                if "." in file:
                    files.append(file)
                else:
                    pass
            for i in files:
                if os.path.isfile(file):
                    print(f"{i} is a file")
                else:
                    print(f"{i} is not a file")
        else:
            print("Invalid Path")
            exit()

class EXTRA_cmds():
    def make_sfolder(path_of_directory, name, password):
        cmd = f"make sfolder {os.path.join(path_of_directory, name)}({password})"
        run_cmdline(cmd)
    def add_files_in_sfolder(sfolder_dir, path_of_file="", type="str", content="", name=""):
        if type == "str":
            cmd = f"add files sfolder {type} ({content}) ->{name}<- {sfolder_dir}"
            run_cmdline(cmd)
        elif type == "file":
            cmd = f"add files sfolder {type} ->{path_of_file}<- {sfolder_dir}"
            run_cmdline(cmd)
        else:
            print("No Such Type only (str and file) supported")
    def aos_cmdline(*args):
        run_cmdline("aos cmdline")
    def create_os_bootloader(path):
        cmd = f"create os bootloader {path}"
        run_cmdline(cmd)
    def read_file(path):
        cmd = f"read file {path}"
        run_cmdline(cmd)
    def write_file(path, content):
        cmd = f"write file {path} {content}"
        run_cmdline(cmd)
    def delete_file(path):
        cmd = f"delete file {path}"
        run_cmdline(cmd)
    def append_file(path, content):
        cmd = f"append file {path} {content}"
        run_cmdline(cmd)
    def make_dir(path):
        cmd = f"make dir {path}"
        run_cmdline(cmd)
    def make_dirs(path):
        cmd = f"make dirs {path}"
        run_cmdline(cmd)
    def dir_file_check(path):
        cmd = f"dir file check {path}"
        run_cmdline(cmd)
    def pcd(query):
        run_cmdline("pcd "+query)

EXTRA_cmds.make_sfolder("..\\..\\Tester", "HelloBois", "BabaBlackSheep")