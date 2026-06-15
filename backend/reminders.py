from datetime import datetime
from plyer import notification
import threading
import time

def reminder_worker(task, time_str):
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == time_str:
            notification.notify(
                title="Reminder",
                message=task,
                timeout=10
            )
            break
        time.sleep(20)

def set_reminder(task, time_str):
    t = threading.Thread(target=reminder_worker, args=(task, time_str))
    t.daemon = True
    t.start()
