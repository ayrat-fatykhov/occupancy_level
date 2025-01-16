import threading
import time

import psutil


class State(threading.Thread):
    """
    Класс для определения уровень загруженности компьютера. Выполняется в потоке
    """
    def __init__(self, period):
        super().__init__(daemon=True)
        self._period = int(period)
        self._stop_flag = threading.Event()
        self._com_state = 0

    def stop(self):
        """
        Метод вызывается снаружи потока и сигнализирует об остановке
        :return: None
        """
        self._stop_flag.set()

    def get_state(self):
        """
        Метод вызывается снаружи потока и показывает уровень загруженности компьютера
        :return: уровень загруженности компьютера
        """
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        show_ram = f'{ram[1]}/{ram[0]}'
        rom = psutil.disk_usage('/')
        show_rom = f'{rom[2]}/{rom[0]}'
        time.sleep(self._period)
        self._com_state = (f'''ЦП: {cpu}
                \rОЗУ: {show_ram}
                \rПЗУ: {show_rom}''')
        return self._com_state