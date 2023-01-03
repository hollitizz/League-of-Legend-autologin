import json
import pyautogui
import pyperclip
import win32gui

from utils import encrypt, decrypt

class AccountManager:
    def __init__(self, password, encrypted):
        self.__password: str = password
        if not encrypted:
            try:
                with open("accounts.lal", "rb") as r_file:
                    datas = r_file.read()
            except:
                datas = json.dumps({})
            with open("accounts.lal", "wb") as w_file:
                w_file.write(encrypt(password, datas))
        with open("accounts.lal", "rb") as f:
            self.__accounts: dict = json.loads(decrypt(password, f.read()))

    def __getAccountCredentials(self, name):
        return {
            "username": self.__accounts[name]["username"],
            "password": self.__accounts[name]["password"]
        }

    def __save(self):
        with open("accounts.lal", "wb") as f:
            datas = json.dumps(self.__accounts, indent=4)
            f.write(encrypt(self.__password, datas))

    def __windowEnumerationHandler(self, hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    def __focusRiotClient(self):
        is_found = False
        top_windows = []
        win32gui.EnumWindows(self.__windowEnumerationHandler, top_windows)
        for i in top_windows:
            if "riot client" in i[1].lower():
                win32gui.ShowWindow(i[0],5)
                win32gui.SetForegroundWindow(i[0])
                is_found = True
                break
        if not is_found:
            raise Exception("Riot Client not found")

    def __copyPasteThis(self, str):
        pyperclip.copy(str)
        pyautogui.hotkey('ctrl', 'v')

    def __clearInput(self):
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')

    def addAccount(self, name, username, password, description = ""):
        self.__accounts[name] = {
            "description": description,
            "username": username,
            "password": password
        }
        self.__save()

    def removeAccount(self, name):
        del self.__accounts[name]
        self.__save()

    def getAccountsInfos(self):
        return [
            {
                "name": name,
                "description": self.__accounts[name]["description"]
            }
            for name in self.__accounts.keys()
        ]

    def login(self, name):
        credentials = self.__getAccountCredentials(name)
        try:
            self.__focusRiotClient()
        except:
            print("Riot Client not found")
            return
        pyautogui.moveTo(358, 365)
        pyautogui.leftClick()
        self.__clearInput()
        self.__copyPasteThis(credentials["username"])
        pyautogui.moveTo(358, 425)
        pyautogui.leftClick()
        self.__clearInput()
        self.__copyPasteThis(credentials["password"])
        pyautogui.press('enter')


if __name__ == "__main__":
    logger = AccountManager()