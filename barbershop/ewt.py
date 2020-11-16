from .models import Client
from datetime import datetime

class Estimate():
    estimate_time = ''
    time_display = ""
    
    def __init__(self, user):
        self.user = user

    def get_estimate(self):
        clients = self.user
        try:
            if clients.count() > 0:
                fmt = '%H:%M'
                client = clients[0]
                start_time = str(client.date)
                start_time = datetime.strptime(start_time, "%H:%M:%S.%f")
                time_now = str(datetime.now().time())
                time_now = datetime.strptime(time_now, "%H:%M:%S.%f")
                total_time = time_now - start_time
                estimate_time = datetime.strptime(
                    str(total_time), "%H:%M:%S.%f").strftime(fmt)
                estimate_time = estimate_time[1:]
                if estimate_time[0] != '0':
                    time_display = "Hour"
                else:
                    time_display = "Minutes"
            else:
                estimate_time = '0:00'
                time_display = "Minutes"
        except:
            estimate_time = '0:00'
            time_display = "Minutes"

        return [estimate_time, time_display]