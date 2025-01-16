import threading
import time


class Timer(threading.Thread):
    """
    Класс для определения количества времени. Выполняется в потоке
    """
    def __init__(self):
        super().__init__(daemon=True)
        self._stop_flag = threading.Event()
        self._time = 0
        self._timer_lock = threading.Lock()

    def stop(self):
        """
        Метод вызывается снаружи потока и сигнализирует об остановке
        :return: Нечего
        """
        self._stop_flag.set()

    def get_sec(self):
        """
        Метод вызывается снаружи потока и показывает какое количество времени прошло с начала операции
        :return: Пройденное время
        """
        with self._timer_lock:
            minute = self._time // 60
            sec_in_minute = minute * 60
            second = self._time - sec_in_minute
            if second < 10:
                return f'{minute}:0{second}'
            else:
                return f'{minute}:{second}'

    def run(self):
        """
        Запускает отсчет времени
        :return: Нечего
        """
        self._time = 0
        self._stop_flag.clear()
        while not self._stop_flag.is_set():
            time.sleep(1)
            with self._timer_lock:
                self._time += 1
