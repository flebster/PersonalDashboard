#--------
#PersonalDashboard
#Module 1 - RSS Reader
#--------

from pathlib import Path
PROJECT_FOLDER=Path(__file__).parent
FEEDS_FILE=PROJECT_FOLDER/"feeds.txt"
feeds = []
with FEEDS_FILE.open("r", encoding="utf-8") as file:
    for line in file:
            line = line.strip()
            
            if line == "":
                continue
                parts=line.split("|")
                feed={
                    "name": parts[0],
                    "url": parts[1],
                    "category": parts[2]
                }
                feeds.append(feed)
                
print("Feeds loaded:")

for feed in feeds:
    print(
        feed["name"],
        "-",
        feed["category"],
        "-",
        feed["url"]
    )
