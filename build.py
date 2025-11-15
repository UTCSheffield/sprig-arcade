import os
import re
import json
import shutil

AUTHORS = ["anonymous"]

status = os.system("rm -rf ./build")
if status != 0:
    print("[ERROR]: Failed to clean build dir")
    exit(1)

os.mkdir("./build") if not os.path.exists("./build") else None
os.mkdir("./build/img") if not os.path.exists("./build/img") else None

status = os.system("rm -rf sprig && git clone https://github.com/hackclub/sprig --depth 1 --branch main")
if status != 0:
    print("[ERROR]: Failed to clone sprig repo")
    exit(1)

metadata = {}

shutil.copytree("./css", "./build/css") 
shutil.copytree("./scripts", "./build/scripts")

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
            
            game_file_basename = i.replace(".js","")
            img_file_path = f"./sprig/games/img/{game_file_basename}.png"
            dest = f"./build/img/{game_file_basename}.png"
            
            has_img = False
            if os.path.exists(img_file_path):
                print("copyfile", img_file_path, dest)
                shutil.copyfile(img_file_path, dest)
                has_img = True
            

            metadata[i] = {
                "title": title,
                "game_file_basename": game_file_basename,
                "has_img": has_img,
                "author": author,
                "addedOn": addedOn,
                "description": description
            }
            
with open("./build/metadata.json", "w", encoding="utf-8") as metaFile:
    json.dump(metadata, metaFile, indent=4)