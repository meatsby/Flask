# %%
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

start_date = input("시작일을 입력해주세요.")# "2021-10-11"
end_date = input("종료일을 입력해주세요.")# "2021-10-11"

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

events = sorted(zip(ename, etime), key=lambda x : x[1], reverse=True)

if len(events) > 6:
    extra = 0
    for i in range(5, len(events)):
        extra += events[i][1]
    events = events[:5] + [("기타", extra)]

# Pie Chart 설정
en = [events[i][0] for i in range(len(events))]
et = [events[i][1] for i in range(len(events))]
colors = ['#ffadad', '#ffd6a5', '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff']

def custom_autopct(pct):
    return "%.1fH" % (pct*0.24) if (pct*0.24) >= 1.5 else ""

fig = plt.figure(figsize=(8, 8))
fig.set_facecolor("white")
ax = fig.add_subplot()

wedgeprops={
    "width":0.6,
    "edgecolor":"w",
    "linewidth":2
}
ax.pie(
    et,
    labels=en,
    autopct=custom_autopct,
    startangle=90,
    counterclock=False,
    colors=colors,
    wedgeprops=wedgeprops,
    pctdistance=0.7
)
plt.title(
    label=start_date if start_date == end_date else start_date + " ~ " + end_date,
    y=0.99,
    fontdict={
        "fontsize":23
    }
)
plt.legend(loc=(1, 0.75))
plt.show()

# %%
