import tkinter as tk

from src.database import DataBase
from src.state import State
from src.timer import Timer


class ComputerStatistics(tk.Toplevel):
    """
    Класс определяет параметры окна с уровнем загруженности компьютера
    """
    def __init__(self, parent, period):
        super().__init__(parent)
        self.title("Уровень загруженности")
        self.geometry('400x300')
        self._period = period
        self._operation = None
        self._sec = None
        self._com_state = None

        self._com_state_now = tk.StringVar()
        self._state_al = tk.Label(self, textvariable=self._com_state_now)
        self._state_al.pack()

        self._progress = tk.StringVar()
        self._state = tk.Label(self, textvariable=self._progress)
        self._state.pack()

        self._button = tk.Button(self, text='Start', command=self._start_stop)  # кнопка пуск/стоп
        self._button.pack()

        self._sec_count = tk.StringVar()
        self._timer = tk.Label(self, textvariable=self._sec_count)
        self._timer.pack()

        self.after(500, self._check_progress)

    def _check_progress(self):
        """
        Показывает уровень загруженности компьютера и, при включении записи в БД, продолжительность записи в окне
        :return: Нечего
        """
        if self._operation is not None:
            progress = self._operation.get_progress()
            self._progress.set(progress)
            sec_count = self._sec.get_sec()
            self._sec_count.set(sec_count)
            if not self._operation.is_alive():
                self._progress.set('')
                self._button.config(text='Start')
                self._operation = None
                self._sec_count.set('')
                self._sec_count = None
        else:
            self._com_state = State(self._period)
            state_now = self._com_state.get_state()
            self._com_state_now.set(state_now)

        self.after(500, self._check_progress)

    def _start_stop(self):
        """
        Запускает или останавливает запись уровня загруженности компьютера в БД и отображение времени
        :return: Нечего
        """
        if self._operation is None:
            self._operation = DataBase(self._period)
            self._progress.set('')
            self._button.config(text='Stop')
            self._operation.start()

            self._sec = Timer()
            self._sec_count.set('')
            self._sec.start()

            self._com_state_now.set('')
            self._com_state.stop()

        else:
            self._operation.stop()
            self._operation.join()
            self._progress.set('')
            self._button.config(text='Start')
            self._operation = None

            self._sec.stop()
            self._sec.join()
            self._sec_count.set('')
            self._sec = None

            self._com_state.start()
            self._com_state_now.set('')
            self._com_state = None


class App(tk.Tk):
    """
    Запрашивает частоту отображения уровня загруженности компьютера в окне
    """
    def __init__(self):
        super().__init__()
        self.title("Уровень загруженности")
        self.geometry('400x300')
        self.period_label = tk.Label(text='Задайте частоту обновления значений, сек.')
        self.period_label.pack()
        self.period = tk.Entry()
        self.period.pack()
        self.btn = tk.Button(self, text='Поехали', command=self.open_state)
        self.btn.pack()

    def open_state(self):
        """
        Открывает окно с параметрами уровня загруженности компьютера
        :return: Нечего
        """
        state = ComputerStatistics(self, self.period.get())
        state.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
