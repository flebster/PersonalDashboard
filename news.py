#--------
#PersonalDashboard
#Module 1 - RSS Reader
#--------

from pathlib import Path
PROJECT_FOLDER=Path(_file_).parent
FEEDS_FILE=PROJECT_FOLDER / "feeds.txt"
feeds = []
with FEEDS_FILE.open("r", encoding="utf-8") as file:
    for line in file:
            line = line.strip()
            
            if line == "":
                continue
                
                feeds.append(line)
                
print("Feeds found:")

for feed in feeds:
    print(" '", feed)