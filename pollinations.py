import requests, os, time, random, re, json

def validPath(s):
    is_valid = bool(re.match(r'^[^<>:"/\\|?*]*$', s))
    cleaned_string = re.sub(r'^[^<>:"/\\|?*]*$', '', s)
    return [is_valid, cleaned_string]

def randomColor(w=-1):
    print("\033["+str(random.randint(31,37))+"m")
    
def msg():
    os.system("cls")
    randomColor(1)
    print("Welcome!")
    randomColor(2)
    print("              .__  .__  .__               __  .__                      ")
    print("______   ____ |  | |  | |__| ____ _____ _/  |_|__| ____   ____   ______")
    print("\____ \ /  _ \|  | |  | |  |/    \\\\__  \\\\   __\  |/  _ \ /    \ /  ___/")
    print("|  |_> >  <_> )  |_|  |_|  |   |  \/ __ \|  | |  (  <_> )   |  \\\\___ \ ")
    print("|   __/ \____/|____/____/__|___|  (____  /__| |__|\____/|___|  /____  >")
    print("|__|                            \/     \/                    \/     \/ ")

image_configurations = {
    "prompts":[],
    "dir2save":"",
    "countimgs":1,
    "sizeXY":[1080,1080]
}

randomColor(3)
print("\033[1m")
while True:
    msg()
    print(f"{'- (1): Image prompt:': <35}","|",end=" ")
    if len(image_configurations["prompts"]) >= 1:
        for n, v in enumerate(image_configurations["prompts"]):
            print('"'+str(v)+'"', end="   ")
        print("")
    else:
        print('""')

    print(f"{'- (2): Path to save image:': <35}","|",end=" ")
    if image_configurations["dir2save"].isspace() or image_configurations["dir2save"] == "":
        print("default (same path)")
    else:
        print(image_configurations["dir2save"])

    print(f"{'- (3): Amount of images:': <35}","|",end=" ")
    print(image_configurations["countimgs"])
    
    print(f"{'- (4): Pixel size of the images:': <35}","|",end=" ")
    print(image_configurations["sizeXY"][0], image_configurations["sizeXY"][1])
    print("")
    print("- (5): Create image")
    print("- (6): Exit")

    randomColor(4)
    userinput = input(" >: \033[0m")

    if userinput == "1":
        msg()
        print("Set prompt below (type '.' to exit and '<' to delete the last one).")
        while True:
            print(len(image_configurations["prompts"]), end="")
            _1 = input(" >: ")

            if _1 == ".":
                break
            elif _1 == "<":
                if len(image_configurations["prompts"]) == 0:
                    print("index out of range!")
                else:
                    image_configurations["prompts"].pop()
            elif not _1.isspace() and not _1 == "":
                if not _1 in image_configurations["prompts"]:
                    image_configurations["prompts"].append(_1)
                else:
                    print("this value already exists!")

        for n, v in enumerate(image_configurations["prompts"]):
            if not validPath(v)[0]:
                print("Corrupted prompt found!")
                print("your prompt cannot include: ^[<>:\"/\\|?*]$")
                print("correcting...")
                image_configurations["prompts"][n] = validPath(v)[1]
                print("done.")
                
    if userinput == "2":
        msg()
        print("Set path to save the image.")
        print("If the path is not found, a new one will be created.")
        while True:
            _1 = input(" >: ")
            if validPath(_1)[0]:
                image_configurations["dir2save"] = _1
                os.system("mkdir "+image_configurations["dir2save"])
                break
            else:
                print("Corrupted path found!")
                print("your path cannot include: ^[<>:\"/\\|?*]$")
                print("correcting...")
                image_configurations["dir2save"] = validPath(_1)[1]
                print("done.")

    if userinput == "3":
        msg()
        print("Put the number of images below")
        while True:
            _1 = input(" >: ")
            if _1.isdigit():
                if int(_1) >= 1 and int(_1) <= 50:
                    image_configurations["countimgs"] = int(_1)
                    break
                else:
                    print("It has to be a number between 1 and 50.")
                
    if userinput == "4":
        msg()
        print("Set the size of the image here.")
        print("Example: '720x720'")
        while True:
            _1 = input(" >: ").replace(" ","")
            if "x" in _1:
                tamx, tamy = _1.split("x")
                if tamx.isdigit() and tamy.isdigit():
                    tamx = int(tamx)
                    tamy = int(tamy)
                    image_configurations["sizeXY"] = [tamx, tamy]
                    break
            print("Invalid response.")
    
    response = ""
    tryagainerror = 0
    if userinput == "5":
        msg()
        if len(image_configurations["prompts"]):
            if image_configurations["countimgs"] >= 1 and image_configurations["countimgs"] <= 50:

                for n1, prompt in enumerate(image_configurations["prompts"]):
                    for n2 in range(0,image_configurations["countimgs"]):
                        tryagainerror = 0
                        while True:
                            try:
                                randomColor()
                                print("making",prompt)
                                response = requests.get((
                                    'https://pollinations.ai/prompt/'+prompt+
                                    "?width="+str(image_configurations["sizeXY"][0])+
                                    "&height="+str(image_configurations["sizeXY"][1])+
                                    "&seed="+str(n2)+
                                    "&nofeed=true"))
                                if response.status_code == 200:
                                    break
                            except Exception as ex:
                                print("\033[32m")
                                tryagainerror += 1
                                print('Error for downloading the image!')
                                print("Error:",response.status_code)
                                print(ex)
                                if tryagainerror >= 10:
                                    input("press enter to reset everything")
                                    break
                                print("trying again...")
                                time.sleep(0.2)
                        if (not type(response) == type("string")) and response.status_code == 200:
                            if len(prompt) >= 21:
                                nome = image_configurations["dir2save"] + ("/"*int(bool(len(image_configurations["dir2save"])))) + prompt[:10] + prompt[-10:] + (str(n2)*int(bool(n2))) + ".jpg"
                            else:
                                nome = image_configurations["dir2save"] + ("/"*int(bool(len(image_configurations["dir2save"])))) + prompt + (str(n2)*int(bool(n2))) + ".jpg"
                            tryagainerror = 0
                            while True:
                                print("creating file...")
                                try:
                                    file = open(nome, 'wb')
                                    file.write(response.content)
                                    file.close()
                                    randomColor()
                                    print("maked " + str(n2 + 1) + "/" + str(image_configurations["countimgs"]) + "\033[0m")
                                    break
                                except Exception as ex:
                                    print("\033[32m")
                                    tryagainerror += 1
                                    print("Error on create image:",ex)
                                    if tryagainerror >= 10:
                                        input("press enter to reset everything")
                                        break
                                    print("trying again...")
                                    time.sleep(0.2)
                        if tryagainerror >= 10:
                            break
                    if tryagainerror >= 10:
                        break
            else:
                print("the amount of images is missing!")
        else:
            print("prompt is missing!")

    if userinput == "6":
        randomColor()
        print("Thanks for use!")
        quit()

print("\033[32m")
print("sucessfuly!")
print("\033[0m")
