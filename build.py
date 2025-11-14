import os
import re
import json

AUTHORS = ["anonymous"]

os.mkdir("./build") if not os.path.exists("./build") else None

status = os.system("rm -rf sprig && git clone https://github.com/hackclub/sprig --depth 1 --branch main")
if status != 0:
    print("[ERROR]: Failed to clone sprig repo")
    exit(1)

metadata = {}

for i in os.listdir("./sprig/games"):
    if os.path.isdir(f"./sprig/games/{i}"):
        continue
    with open(f"./sprig/games/{i}", encoding="utf-8", errors="ignore") as gameFile:
        content = gameFile.read()

        titlem = re.search(r"@title\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        title = titlem.group(1).strip() if titlem else None
        if title is None: continue

        authorm = re.search(r"@author\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        author = authorm.group(1).strip() if authorm else None
        if author is None: continue

        addedOnm = re.search(r"@addedOn\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        addedOn = addedOnm.group(1).strip() if addedOnm else None
        if addedOn is None: continue

        descriptionm = re.search(r"@description\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        description = descriptionm.group(1).strip() if descriptionm else None
        if description is None: continue

        if author.lower() in AUTHORS:
            print(f"[INFO]: Including game '{i}' by author '{author}'")
            os.mkdir("./build/games") if not os.path.exists("./build/games") else None
            with open(f"./build/games/{i}", "w", encoding="utf-8") as outFile:
                outFile.write(content)
            metadata[i] = {
                "title": title,
                "author": author,
                "addedOn": addedOn,
                "description": description
            }
            
with open("./build/metadata.json", "w", encoding="utf-8") as metaFile:
    json.dump(metadata, metaFile, indent=4)