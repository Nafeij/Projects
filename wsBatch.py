import io
import os

try:
    import simplejson as json
except ImportError:
    import json

if __name__ == '__main__':
    root = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\War on the " \
           "Sea\\WarOnTheSea_Data\\StreamingAssets\\override\\unit\\air"
    pnames = []
    i = 0
    for r, d, f in os.walk(root):
        for file in f:
            if '_model.txt' in file:
                # pnames.append(os.path.join(r, file))
                with open(os.path.join(r, file), 'r+') as j:
                    off = False
                    j.seek(3)
                    try:
                        data = json.loads(j.readline())
                    except:
                        off = True
                        j.seek(0)
                        data = json.loads(j.readline())
                    post = j.readline()

                    if len(data["fixedGunData"]) > 0:
                        fixedDataJson = json.loads(data["fixedGunData"][0])
                        fixedDataJson["damage"] = [float(round(i)) for i in fixedDataJson["damage"]]
                        data["fixedGunData"][0] = json.dumps(fixedDataJson)

                    if len(data["aaaGunsData"]) > 0:
                        aaDataJson = json.loads(data["aaaGunsData"][0])
                        if not "sizes" in aaDataJson or len(aaDataJson["sizes"]) == 0:
                            nTurrets = len(aaDataJson["particleRef"])
                            aaDataJson["sizes"] = [1.0] * nTurrets
                            aaDataJson["rate"] = [4] * nTurrets
                            aaDataJson["range"] = [200] * nTurrets
                        else:
                            aaDataJson["sizes"] = [float(round(i)) for i in aaDataJson["sizes"]]
                        data["aaaGunsData"][0] = json.dumps(aaDataJson)

                    j.seek(0 if off else 3)
                    j.write((json.dumps(data) + "\n" + post).replace(" ", ""))
                    j.truncate()
                    # print(j.name)
                    j.close()
                    
'''
            if '_data.txt' in file:
                with open(os.path.join(r, file), 'r+') as j:
                    j.seek(0)
                    lines = j.readlines()
                    newlines = []
                    isDB, edited = False, False
                    for line in lines:
                        line = line.replace('锘縶','{')
                        try:
                            data = json.loads(line)
                        except:
                            print(f"JSON error: {line} in {j.name}")
                            break
                        if "unitSubtypeString" in data:
                            isDB = data["unitSubtypeString"] == "Dive_Bomber"
                            if data["dive"] != 20.0:
                                data["dive"] = 20.0
                                edited = True
                        if not "customAttack" in data:
                            edited = True
                            if "unitSubtypeString" in data:
                                data.update({"customAttack": False, "attackRange": [30, 50], "levelHeight": [15, 15],
                                             "levelRange": [100, 100], "levelLead": [1.5, 1.5], "levelOffset": [4, 4]})
                            elif data["weaponTypeString"] == "Aerial_Torpedo":
                                data.update({"customAttack": False, "attackHeight": [4, 4], "attackRange": [1, 1],
                                             "additionalLeadTime": [28, 28], "offset": [8, 8]})
                            elif data["weaponTypeString"] == "Rocket":
                                data.update({"customAttack": False, "attackHeight": [15, 15], "attackRange": [90, 90],
                                             "additionalLeadTime": [3, 3], "offset": [4, 4]})
                            elif data["weaponTypeString"] == "Bomb" or data[
                                "weaponTypeString"] == "Aerial_Depth_Charge":
                                data.update({"customAttack": False, "levelHeight": [0, 0], "levelRange": [2, 2],
                                             "levelLead": [0, 0], "levelOffset": [7, 7], "skipHeight": [6, 6],
                                             "skipRange": [50, 70], "skipLead": [5, 5], "skipOffset": [7, 7]})
                                if isDB:
                                    data.update({"attackHeight": [85, 85], "attackRange": [120, 120],
                                             "additionalLeadTime": [25, 25], "offset": [3, 3],
                                             "diveDropHeight": [32, 38], "speed": [-1], "diveLead": [4, 4],
                                             "diveOffset": [3, 3]})
                            else:
                                print(f"Unknown weapon type {data['weaponTypeString']} in {j.name}")
                        newlines.append(json.dumps(data).replace(" ", ""))
                    if edited:
                        j.seek(3)
                        for line in newlines:
                            j.write(f"{line}\n")
                        j.truncate()
                        print(j.name)
                    j.close()'''
