#--------
#PersonalDashboard
#Module 1 - RSS Reader
#--------

from pathlib import Path
PROJECT_FOLDER=Path(__file__).parent
FEEDS_FILE=PROJECT_FOLDER/"feeds.txt"
print("Project folder:", PROJECT_FOLDER)
print("Feeds File:", FEEDS_FILE)
print("Exists?:", FEEDS_FILE.exists())
feeds = []
with FEEDS_FILE.open("r", encoding="utf-8") as file:
    for line in file:
            line = line.strip()
            print("Line Read:",repr(linea))
            if line == "":
                continue
                parts=line.split("|")
                feed={
                    "name": parts[0],
                    "url": parts[1],
                    "category": parts[2]
                }
               print("Adding:",feed)
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
