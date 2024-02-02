import os
import subprocess

xtra_cmds = ["os_builder", "$(AOS pcd INSTALL)$", "fix cmdline", "pcd ", "color DEF"]
pcd_cmds = ["get-update", "get-package", "remove-package"]
defCOLOR = "7"

def aol(cmd):
    import asm
    asm.AOL_run(file=cmd)

class Operator():
    def __init__(self, *args):
        self.error = ""
        self.run_line()

    def get_pcd_output(self, cmd):
        exit = input("These commands can have serious consequences on your system if used improperly. Do you wish to continue?(yes/no): ")
        if exit == "yes":
            buffer_ = False
            match = False
            target_str = ""
            idx = 0
            while not buffer_:
                if not cmd[idx] == " ":
                    target_str += cmd[idx]
                else:
                    buffer_ = True
                    break
                idx += 1
            if target_str in pcd_cmds:
                match = True
            else:
                match = False
            if cmd in pcd_cmds or match:
                if "get-update" in cmd:
                    subprocess.check_call(["sudo", "apt-get", "update"])
                    self.run_line()
                elif "get-package" in cmd:
                    cmd = cmd.replace("get-package ", "")
                    subprocess.check_call(["pip", "install", cmd])
                    self.run_line()
                elif "remove-package" in cmd:
                    cmd = cmd.replace("remove-package ", "")
                    subprocess.check_call(["pip", "uninstall", cmd])
                    self.run_line()
                else:
                    print(f"'pcd {cmd}' is not recognized as an internal or external command")
                    self.run_line()
            elif cmd == "exit":
                print("Exiting...")
                self.run_line()
            else:
                print(f"'pcd {cmd}' is not recognized as an internal or external command")
                self.run_line()
        elif exit == "no":
            print("Exiting...")
            self.run_line()
        else:
            print("Unable to execute command \n Exiting...")
            self.run_line()

    def get_output(self, cmd):
        try:
            if cmd in xtra_cmds or "pcd " in cmd:
                if "pcd " in cmd and not "pcd INSTALL":
                    cmd = cmd.replace("pcd ", "")
                    self.get_pcd_output(cmd)
                elif cmd == "os_builder":
                    print("OS builder is not available!")
                    self.run_line()
                elif cmd == "$(AOS pcd INSTALL)$":
                    print("PCD is not currently available!")
                    self.run_line()
                elif "color DEF" in cmd:
                    subprocess.check_call(["color", defCOLOR])
                    self.run_line()
                elif "aol " in cmd:
                    aol(cmd.replace("aol ", ""))
                elif cmd == "fix cmdline":
                    if os.path.exists("./onwork.txt"):
                        os.remove("./onwork.txt")
                        print("Cmdline Fixed")
                        self.run_line()
                    else:
                        print("No Problem Detected!")
                        self.run_line()
            elif not cmd in xtra_cmds:
                if not "cd " in cmd:
                    subprocess.run(cmd, shell=True)
                if cmd != "exit" and not "cd " in cmd:
                    self.run_line()
                elif "cd " in cmd:
                    cmd = cmd.replace("cd ", "")
                    os.chdir(cmd)
                    self.run_line()
                else:
                    exit()
        except Exception as e:
            self.error = str(e)
            print(self.error)

    def run_line(self, dir=""):
        dir=os.getcwd()
        print(dir)
        line = input("$aos -> ")
        self.get_output(line)

def run():
    Operator()

run()