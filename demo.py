#%%
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["font.size"] = 15
matplotlib.rcParams["axes.unicode_minus"] = False
from pprint import pprint
from Google import *

CLIENT_SECRET_FILE = "credentials.json"
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
response = service.calendarList().list().execute()

start_date = "2021-10-11"
end_date = "2021-10-17"

ename = []
etime = []

calendars = response.get("items")

for c in calendars[1:8]:
    calendar_id = c["id"]
    time_min = start_date + 'T00:00:00+09:00'
    time_max = end_date + 'T23:59:59+09:00'
    is_single_events = True
    orderby = 'startTime'

    events_result = service.events().list(calendarId = calendar_id,
                                        timeMin = time_min,
                                        timeMax = time_max,
                                        singleEvents = is_single_events,
                                        orderBy = orderby
                                        ).execute()

    evts = events_result.get("items")
    evt = [c["summary"]]
    for e in evts:
        if "dateTime" in e["start"]:
            start_time = datetime.datetime.fromisoformat(e["start"]["dateTime"][:19])
            end_time = datetime.datetime.fromisoformat(e["end"]["dateTime"][:19])
            hrs = (end_time - start_time).seconds / 3600
            evt.append((e["summary"], hrs))

    for k, v in evt[1:]:
        if k not in ename:
            ename.append(k)
            etime.append(v)
        elif k in ename:
            etime[ename.index(k)] += v

print(ename)
print(etime)

wedgeprops={"width":0.8}
plt.pie(etime, labels=ename, autopct="%.1f%%", startangle=90, counterclock=False, wedgeprops=wedgeprops)
plt.legend(loc=(1.2, 0.3))
plt.show()

# %%
