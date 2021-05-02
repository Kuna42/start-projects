# this is an example

#
# Dieses Beispiel enthält vorschläge für Formatierung
# (und geht über das Niveau des start-projects hinaus).
# Dieser Code kann als inspiration dienen um sich den
# Aufbau eines Programms in Python vorzustellen.
#
# Nutzt bitte Methoden und führt dann zum Schluss diese
# in dieser if Abfrage ausführen:
# if __name__ == "__main__":
#     methode()
# Wenn euer Programm (Methoden) dann in diesem if
# ausgeführt, dann kann man euer Programm auch wie eine
# Bibliothek mit in einen anderen Code einbinden.
#
# Haltet die globalen Variablen so gering wie möglich,
# also bei diesem Code sind es nur __author__ und
# __version__ die global sind.
#

##########
# import

import os

import sqlite3

import time

import getpass

import re

import platform


##########
# global variable

# __name__ = "Calendar"  # sollte nicht verwendet werden, da
#                        # diese Variable Systemrelevant ist
__version__ = "0.0.1"
__author__ = "Kuna42"


###############
# Crypt
class Crypt:
    def __init__(self, chunks: int = 64):
        self.chunks = chunks
        self.info_size = 16

    def get_key(self, password: str) -> bytes:
        return password.encode()

    def encrypted(self, file_path, key: bytes, file_path_new: str = None):
        if not file_path_new:
            file_path_new = file_path + ".crypt"
        file_size = str(os.path.getsize(file_path)).zfill(self.info_size)
        file_info = "info".zfill(self.info_size)

        with open(file_path, mode="rb") as file_clear:
            with open(file_path_new, mode="wb") as file_chiffre:
                # write file size in clear format
                file_chiffre.write(file_size.encode())
                # write info in clear bytes clear
                file_chiffre.write(file_info.encode())
                while True:
                    file_bytes = file_clear.read(self.chunks)
                    if not file_bytes:
                        break
                    elif len(file_bytes) - self.chunks:
                        file_bytes += b' ' * (self.chunks - len(file_bytes))
                    crypt_bytes = file_bytes###here
                    ###need to be crypt
                    # write the encrypted bytes (chunk) on the new file
                    file_chiffre.write(crypt_bytes)

    def decrypted(self, file_path, key: bytes, file_path_new: str = None):
        if not file_path_new:
            file_path_new = file_path + ".crypt"

        with open(file_path, mode="rb") as file_chiffre:
            with open(file_path_new, mode="wb") as file_clear:
                file_size = int(file_chiffre.read(self.info_size).decode())
                file_info = str(file_chiffre.read(self.info_size))
                while True:
                    crypt_bytes = file_chiffre.read(self.chunks)
                    if not crypt_bytes:
                        break
                    ###need to decrypted it
                    file_bytes = crypt_bytes
                    ###
                    file_clear.write(file_bytes)

                # if os.path.getsize(file_path_new) != int(file_size):
                file_clear.truncate(file_size)


###############
# calendar
class Calendar:
    class PasswordError(Exception):
        pass  # should it be here? or not in the class calendar ?

    class Meeting:
        def __init__(self, date: str, head: str, text: str = "", remember_time=b'0'):
            self.date = date
            self.head = head
            self.text = text
            self.remember_time = remember_time  #this is not used

    def __init__(self):
        self.__password_key = b''
        self.__file_path = ""
        self.__file_path_original = ""
        self.__file_path_decrypted = f"/tmp/calendar-{__name__}-{__version__}/"  # for linux
        self.__file_name = ""
        self.allowed_path = ("home", "tmp", "media", "mnt")

        self.crypt = Crypt(chunks=1 * 1024)

        # creating the path in tmp
        if not os.path.exists(self.__file_path_decrypted):
            os.mkdir(self.__file_path_decrypted)

    def __del__(self):
        try:
            self.close()
        except PermissionError:
            pass
        os.rmdir(self.__file_path_decrypted)
        self.print("Successful closed.")

    def lock(self):
        if not self.__file_path[:5] == "/tmp/":  # for linux
            raise PermissionError("Wrong path of the temporary file.")
        if os.path.exists(self.__file_path):
            os.remove(self.__file_path)

    def close(self):
        self.lock()
        self.__password_key = b''
        self.__file_path = ""
        self.__file_path_original = ""
        self.__file_name = ""

    def unlock(self):
        self.crypt.decrypted(file_path=self.__file_path_original,
                             file_path_new=self.__file_path,
                             key=b'')
        if not self.__password_key:
            raise self.PasswordError("Wrong password. Try again.")

    def open(self, file_path: str):
        if (file_path[0] == "/") and not (file_path.split("/")[1] in self.allowed_path):
            raise PermissionError(f"You can not open a file in a system path. "
                                  f"You can only open a file in {self.allowed_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError("You can not open a not existing file.")

        if self.__file_path:
            __key = self.__password_key
            self.close()
            self.__password_key = __key
            del __key

        self.__file_path_original = file_path
        self.__file_name = file_path.split("/")[-1]
        self.__file_path = self.__file_path_decrypted + self.__file_name

        self.unlock()

    def create(self, file_path: str):
        if (file_path[0] == "/") and not (file_path.split("/")[1] in self.allowed_path):
            raise PermissionError(f"You can not open a file in a system path. "
                                  f"Only in {self.allowed_path}.")
        if os.path.exists(file_path):
            raise FileExistsError("You can not overwrite a file.")
        self.__file_path_original = file_path
        self.__file_name = file_path.split("/")[-1]
        self.__file_path = self.__file_path_decrypted + self.__file_name

        sql_instruction = "CREATE TABLE IF NOT EXISTS calendar (" \
                          "id                   INTEGER PRIMARY KEY AUTOINCREMENT," \
                          "date                 DATE," \
                          "head                 VARCHAR(20)," \
                          "text                 TEXT," \
                          "remember_time        INTEGER  );"

        with sqlite3.connect(self.__file_path) as calendar_db:
            calendar_db_cursor = calendar_db.cursor()
            calendar_db_cursor.execute(sql_instruction)
            calendar_db.commit()

        self.crypt.encrypted(file_path=self.__file_path,
                             file_path_new=self.__file_path_original,
                             key=b'')

    def read(self, date: str = None, meeting_head: str = None) -> [Meeting]:
        """
        the meeting head may not have this character [ " ]
        :param date: can be "today" or "tomorrow" or a specific date
        :param meeting_head: the head of the meeting can be searched
        :return:
        """
        if not self.__file_path:
            raise FileNotFoundError("No file is selected.")

        search = ""
        if date:
            if date == "today":
                datetime = time.localtime()
                date = f"{datetime.tm_year}-{datetime.tm_mon}-{datetime.tm_mday}"
            elif not re.findall(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}", date):
                raise ValueError("The date must be like '2020-12-31'.")
            search = f"WHERE date = \"{date}\""
        elif meeting_head:
            search = f"WHERE head LIKE \"{meeting_head}\" "
        sql_instruction = f"SELECT date, head, text, remember_time " \
                          f"FROM calendar " \
                          f"{search} ORDER BY date DESC;"
        with sqlite3.connect(self.__file_path) as calendar_db:
            calendar_db_cursor = calendar_db.cursor()
            calendar_db_cursor.execute(sql_instruction)
            data_raw = calendar_db_cursor.fetchall()
        data = []
        for meeting in data_raw:
            data.append(self.Meeting(
                date=meeting[0],
                head=meeting[1],
                text=meeting[2],
                remember_time=meeting[3]
            ))
        return data

    def write(self, data: Meeting, delete=False):
        """
        the data may not contain the character [ " ]
        :param data:
        :param delete:
        :return:
        """
        if not self.__file_path:
            raise FileNotFoundError("No file is selected.")

        sql_instruction = "INSERT OR IGNORE INTO calendar " \
                          "(date, head, text, remember_time) " \
                          "VALUES(?, ?, ?, ?);"
        data = (data.date, data.head, data.text, data.remember_time)

        if delete:
            sql_instruction = f"DELETE FROM calendar " \
                              f"WHERE date = \"{data[0]}\" " \
                              f"AND head = \"{data[1]}\";"

        with sqlite3.connect(self.__file_path) as calendar_db:
            calendar_db_cursor = calendar_db.cursor()
            if delete:
                calendar_db_cursor.execute(sql_instruction)
            else:
                calendar_db_cursor.execute(sql_instruction, data)

    def save(self):
        if not self.__file_path:
            raise FileNotFoundError("No file is selected.")

        self.crypt.encrypted(file_path=self.__file_path,
                             file_path_new=self.__file_path_original,
                             key=b'')

    @staticmethod
    def print(text, end="\n"):
        print(text, end=end)

    @staticmethod
    def input(secret=False) -> str:
        if secret:
            return getpass.getpass()
        else:
            return input()

    def reminder(self):  # for linux
        today = self.read(date="today")
        for meeting in today:
            # could add f"-i icon.png " when a icon should be added
            command = f"notify-send " \
                      f"-t 0 " \
                      f"-u low " \
                      f"\"{meeting.head}\" " \
                      f"\"{meeting.text}\" "
            os.system(command)

    def _commands(self, command):
        if not command:
            pass

        elif command[:4] == "open":
            file_path = command[4:].strip()
            if not os.path.exists(file_path):
                raise FileNotFoundError("This File does not exist.")
            self.__password_key = self.crypt.get_key(self.input(secret=True))
            self.open(file_path)
            self.print(f"Open file: {self.__file_path}")

        elif command[:6] == "create":
            self.create(command[6:].strip())
            self.print("File was created.")

        elif command[:5] == "close":
            self.close()
            self.print("File closed.")

        elif command[:4] == "save":
            self.save()
            self.print("File was saved.")

        elif command[:3] == "add":
            data = ["date: ", "head: ", "text: ", "remember time: "]
            for i in range(len(data)):
                self.print(data[i], end="")
                data[i] = self.input()
            self.write(self.Meeting(
                date=data[0],
                head=data[1],
                text=data[2],
                remember_time=b''  ##
            ))
            self.print("Added to file.")

        elif command[:3] == "del":
            data = ["date: ", "head: "]
            for i in range(len(data)):
                self.print(data[i], end="")
                data[i] = self.input()
            data = self.Meeting(
                date=data[0],
                head=data[1]
            )
            if self.read(data.date, data.head):
                self.write(delete=True,
                           data=data)
                self.print("Delete meeting.")
            else:
                self.print("Meeting not found.")

        elif command[:4] == "look":
            data = ["date: ", "head: "]
            meetings = []
            for i in range(len(data)):
                self.print(data[i], end="")
                data[i] = self.input()
            if not data[0] and not data[1]:
                meetings = self.read()
            elif data[0] and not data[1]:
                meetings = self.read(date=data[0])
            elif not data[0] and data[1]:
                meetings = self.read(meeting_head=data[1])
            elif data[0] and data[1]:
                meetings = self.read(date=data[0],
                                     meeting_head=data[1])
            for meeting in meetings:
                self.print(f"-----Meeting-----\n"
                           f"date: {meeting.date}\n"
                           f"head: {meeting.head}\n"
                           f"text: {meeting.text}\n"
                           f"-----------------")

        elif command[:4] == "help":
            self.print(
                "   Commands:\n"
                "-help\n"
                "-info\n"
                "-open [file_path]\n"
                "-create [file_path]\n"
                "-close\n"
                "-save\n"
                "-add\n"
                "-del\n"
            )
        elif command[:4] == "info":
            self.print(
                f"Name: Calendar\n"
                f"Version: {__version__}\n"
                f"Written by {__author__}\n"
                f"Works on: Linux\n"
                f"Your OS: {platform.uname().system}"
            )

        else:
            self.print("use help")
            self.reminder() if self.__file_path else None

    def show(self):
        while True:
            self.print(f"{self.__file_name}>", end="")
            command = self.input()
            if command == "exit":
                break
            try:
                self._commands(command)
            except FileNotFoundError as text:
                self.print(text)
            except FileExistsError as text:
                self.print(text)
            except ValueError as text:
                self.print(text)


####################
#
if __name__ == "__main__":
    calendar = Calendar()
    calendar.show()
