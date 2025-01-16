import sqlite3
import threading
import time
from datetime import datetime

import psutil


class DataBase(threading.Thread):
    """
    Класс для записи в базу данных. Выполняется в потоке
    """
    def __init__(self, period):
        super().__init__(daemon=True)
        self._stop_flag = threading.Event()
        self._progress = 0
        self._progress_lock = threading.Lock()
        self._period = int(period)

    def stop(self):
        """
        Метод вызывается снаружи потока и сигнализирует об остановке
        :return: Нечего
        """
        self._stop_flag.set()

    def get_progress(self):
        """
        Метод вызывается снаружи потока и показывает какие данные будут записаны в базу данных
        :return: уровень загруженности компьютера
        """
        with self._progress_lock:
            return self._progress

    def run(self):
        """
        Метод определяет уровень загруженности компьютера и записывает данные в БД
        :return: Нечего
        """
        self._progress = ''
        self._stop_flag.clear()

        while not self._stop_flag.is_set():
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            show_ram = f'{ram[1]}/{ram[0]}'
            rom = psutil.disk_usage('/')
            show_rom = f'{rom[2]}/{rom[0]}'
            time_now = str(datetime.now())
            time.sleep(self._period)
            with self._progress_lock:
                self._progress = (f'''ЦП: {cpu}
                \rОЗУ: {show_ram}
                \r ПЗУ: {show_rom}''')
                con = sqlite3.connect("computer_state.db")
                cursor = con.cursor()
                cursor.execute("""
                    create table if not exists state (
                       cpu FLOAT,
                       ram_free INTEGER,
                       ram_all INTEGER,
                       rom_free INTEGER,
                       rom_all INTEGER,
                       data_time VARCHAR(255));""")
                state_write = (cpu, ram[1], ram[0], rom[2], rom[0], time_now)
                command_sql = f"""INSERT INTO state (cpu, ram_free, ram_all, rom_free, rom_all, data_time)
                \rVALUES (?, ?, ?, ?, ?, ?)"""
                command_sql = command_sql.replace("\r", " ")
                cursor.execute(command_sql, state_write)
                con.commit()
