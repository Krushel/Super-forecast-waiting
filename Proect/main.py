import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic, QtTest, QtCore
from PyQt5.QtCore import QThread, QTimer
import weather
import time
import datetime
from weather import DAYS


#Маленькая хитрость для открытия приложения.
H_show = [
    200, 600,
]
H_hide = [
    200, 600,
]

# Класс который обращается к библиотеке(weather) ко второму файлу
class WeatherData(QThread):
    req = weather.today()
    temp = req['temp']
    feels = req['feels']
    pres = req['pressure']
    speed = str(req['wind']['speed'])
    city = req['city']
    type = req['dis']

    week = weather.week()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while True:
            try:
                req = weather.today()
            except:
                req['temp'] =self.temp
                req['feels'] = self.feels
                req['pressure'] = self.pres
                req['wind']['speed'] = self.pres
                req['city'] = self.city
                req['dis'] =self.type

            #на неделю.
            try:
                req_week = weather.week()
                self.week = req_week
            except:
                self.week = DAYS
            self.temp = req['temp']
            self.feels = req['feels']
            self.pres = req['pressure']
            self.speed = str(req['wind']['speed'])
            self.city = req['city']
            self.type = req['dis']
            time.sleep(2)

#Класс который будет открываться
class App(QWidget):
    show_more = True
    tic = False
    def __init__(self, app):
        QWidget.__init__(self)
        self.weather = WeatherData()
        self.weather.start()
        self.app = app
        self.set()
        self.setData()
        self.setMore()
        self.timer = QTimer()
        self.timer.timeout.connect(self.setData)
        self.timer.start(1000)

    # Запуск юишки
    def set(self):
        self.w_root = uic.loadUi('untitled.ui')
        self.w_root.l_type.clicked.connect(self.setHeight)
        self.w_root.show()

    #устанавливаем обновление значений на сегодня.
    def setData(self):
        self.w_root.label_1.setText(str(self.weather.temp) + "°C")
        self.w_root.l_feel_2.setText(self.weather.feels)
        self.w_root.l_pres.setText(self.weather.pres)
        self.w_root.l_wind.setText(self.weather.speed + "м/с")
        self.w_root.l_city.setText(self.weather.city)
        self.w_root.label_3.setText(self.weather.type)

        # день недели.
        today = DAYS[datetime.datetime.today().weekday()]
        self.w_root.label.setText(today['title'])
        color = today['color']
        self.w_root.label.setStyleSheet(f"color:{color}")
        #время.
        if self.tic:
            now = datetime.datetime.today().strftime("%H:%M:%S")
            self.tic = False
        else:
            now = datetime.datetime.today().strftime("%H %M %S")
            self.tic = True
        self.w_root.label_2.setText(now)
    # Открытие приложения по кнопке
    def setHeight(self):
        if self.w_root.height() >= 600:
            self.show_more = False
        if self.show_more:
            for i in H_hide:
                if self.w_root.height() > i:
                    continue
            self.w_root.resize(210, i)
            self.w_root.l_type.move(210, i-110)
            self.w_root.label.move(210, i+10)
            self.w_root.label_2.move(210, i-210)
            time.sleep(.02)
            self.show_more = False
        else:
            for i in reversed(H_show):
                self.w_root.resize(210, i)
                self.w_root.l_type.move(110, i-110)
                self.w_root.label.move(210,i+10)
                self.w_root.label_2.move(210, i-210)
                time.sleep(.02)
            self.show_more = True
        App.show_more = self.show_more


      # Дни недели на следущию неделю
    def setMore(self):
        for i in self.weather.week:
            w_day = uic.loadUi('day.ui')
            w_day.l_title.setText(i['title'])
            w_day.l_temp.setText(str(round(i['temp']))+ "°C")
            w_day.l_type.setText(i['type'])
            self.w_root.box.addWidget(w_day)



# Открытие приложения в диспетчере устройств + закрытие приложения через крестик
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ap = App(app)
    app.exec_()