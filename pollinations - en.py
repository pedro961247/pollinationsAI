import requests, os, time, random

print("Welcome!")
print("")
print("              .__  .__  .__               __  .__                      ")
print("______   ____ |  | |  | |__| ____ _____ _/  |_|__| ____   ____   ______")
print("\____ \ /  _ \|  | |  | |  |/    \\\\__  \\\\   __\  |/  _ \ /    \ /  ___/")
print("|  |_> >  <_> )  |_|  |_|  |   |  \/ __ \|  | |  (  <_> )   |  \\\\___ \ ")
print("|   __/ \____/|____/____/__|___|  (____  /__| |__|\____/|___|  /____  >")
print("|__|                            \/     \/                    \/     \/ ")
print("")


while 1:
    print("(1): Yes.")
    print("(0): No.")
    multdialog = input("Would you like to do the function of creating multi-images?:")
    if multdialog in ["1","0"]:
        break

imagens = []
if multdialog == "0":
    imagens.append(input("Which image to generate??:"))
elif multdialog == "1":
    loop = 1
    while 1:
        v = input(str(loop) + ": Which image to generate?? ('.' to exit):")
        if v == '.':
            break
        else:
            loop += 1
            imagens.append(v)

print("")
diretsave = input("Which directory to save?:")
if diretsave != "":
    diretsave = diretsave + "/"
print("")

# Pegar informações para criar a imagem
while 1:
    quantas = input("How many images?:")
    if quantas.isdigit() and int(quantas) <= 10 and int(quantas) >= 1:
        break
    else:
        print("value its not a number!")
        print("or")
        print("The value must be between 1 and 10")
print("")

tamx, tamy = None, None
while 1:
    print("default: 1000x1000")
    tamanho = input("size? (x, y):")
    if not tamanho:
        tamanho = "1000, 1000"
    if ',' in tamanho:
        try:
            tamx, tamy = tamanho.replace(" ","").split(",")
            tamx, tamy = int(tamx), int(tamy)

            if tamx >= 16 or tamy >= 16:
                if tamx <= 2048 or tamy <= 2048:
                    print("Ideal size.")
                    break
                else:
                    print("max size: 2048")
                    print(tamx, tamy)
            else:
                print("min size: 16")
                print(tamx, tamy)
        except:
            print("unknown value!")
            print(tamanho)
    else:
        print("unknown value!")
        print(tamanho)
print("")

##########

# Função sair
def s():
    time.sleep(0.3)
    print("Exiting!")

# Função para colocar cor aleatoria nos textos
def rando():
    r = random.randint(1,4)
    if r == 1:
        return "\033[31m"
    if r == 2:
        return "\033[32m"
    if r == 3:
        return "\033[33m"
    if r == 4:
        return "\033[34m"

imagenscaminho = []

for numimg, imag in enumerate(imagens):
    print("making "+rando()+str(quantas)+" \033[0mimages of "+rando()+"'"+imag+"'\033[0m")

print("for cancel, close the program")

tamx, tamy = tamy, tamx
for numimg, imag in enumerate(imagens):
    for i in range(0,int(quantas),1):
        if i == 0:
            response = requests.get('https://pollinations.ai/prompt/'+imag+"?width="+str(tamx)+"&height="+str(tamy)+"&nofeed=true")
        else:
            response = requests.get('https://pollinations.ai/prompt/'+imag+"?width="+str(tamx)+"&height="+str(tamy)+"&seed="+str(i)+"&nofeed=true")

        if response.status_code == 502 or response.status_code == 200:
            
            print(rando() + "maked " + str(i + 1) + "/" + quantas + "\033[0m")
            if i == 0:
                nome = diretsave + imag + '.jpg'
            else:
                nome = diretsave + imag + str(i + 1) + '.jpg'
            try:
                f = open(nome, 'wb')
            except:
                print("Error on generate image")
                input("click ENTER for continue")

            f.write(response.content)
            f.close()
            imagenscaminho.append(os.path.abspath(nome))
        else:
            print('Error for downloading the image!')
            print("Error:",response.status_code)
            s()
    print("------------------------------------------------------------------------------------------------------------")
    print("")
     
print("sucessfuly!")
s()
