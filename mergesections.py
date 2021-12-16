import json
import os
import shutil

if os.path.isdir("outsections"):
    shutil.rmtree("outsections")
os.mkdir("outsections")
videos = {}
for secgroup in os.listdir("allsections"):
    secdir = os.path.join("allsections", secgroup)
    with open(os.path.join(secdir, "Scene.json")) as f:
        data = json.load(f)
    for video in data:
        videos[os.path.abspath(os.path.join(secdir, video["video"]))] = video

scenejson = []
for i, (k, v) in enumerate(videos.items()):
    v["video"] = f"section{i}.mp4"
    scenejson.append(v)
    shutil.copy(k, os.path.join("outsections", f"section{i}.mp4"))

with open("outsections/Scene.json", "w+") as f:
    json.dump(scenejson, f, indent=4)
