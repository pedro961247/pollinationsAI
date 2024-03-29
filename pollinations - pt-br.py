import requests, os, time, random

print("Bem-vindo!")
print("")
print("              .__  .__  .__               __  .__                      ")
print("______   ____ |  | |  | |__| ____ _____ _/  |_|__| ____   ____   ______")
print("\____ \ /  _ \|  | |  | |  |/    \\\\__  \\\\   __\  |/  _ \ /    \ /  ___/")
print("|  |_> >  <_> )  |_|  |_|  |   |  \/ __ \|  | |  (  <_> )   |  \\\\___ \ ")
print("|   __/ \____/|____/____/__|___|  (____  /__| |__|\____/|___|  /____  >")
print("|__|                            \/     \/                    \/     \/ ")
print("")


while 1:
    print("(1): Sim.")
    print("(0): Não.")
    multdialog = input("Gostaria de fazer a função de criar multi-imagens?:")
    if multdialog in ["1","0"]:
        break

imagens = []
if multdialog == "0":
    imagens.append(input("Qual imagem gerar?:"))
elif multdialog == "1":
    loop = 1
    while 1:
        v = input(str(loop) + ": Qual imagem gerar? ('.' para sair):")
        if v == '.':
            break
        else:
            loop += 1
            imagens.append(v)

print("")
diretsave = input("Qual diretorio salvar?:")
if diretsave != "":
    diretsave = diretsave + "/"
print("")

# Pegar informações para criar a imagem
while 1:
    quantas = input("Quantas?:")
    if quantas.isdigit() and int(quantas) <= 10 and int(quantas) >= 1:
        break
    else:
        print("valor não é número!")
        print("ou")
        print("valor tem que ser entre 1 e 10")
print("")

tamx, tamy = None, None
while 1:
    print("padrão: 1000x1000")
    tamanho = input("tamanho? (x, y):")
    if not tamanho:
        tamanho = "1000, 1000"
    if ',' in tamanho:
        try:
            tamx, tamy = tamanho.replace(" ","").split(",")
            tamx, tamy = int(tamx), int(tamy)

            if tamx >= 16 or tamy >= 16:
                if tamx <= 2048 or tamy <= 2048:
                    print("tamanho ideal.")
                    break
                else:
                    print("tamanho maximo: 2048")
                    print(tamx, tamy)
            else:
                print("tamanho minimo: 16")
                print(tamx, tamy)
        except:
            print("valor desconhecido!")
            print(tamanho)
    else:
        print("valor desconhecido!")
        print(tamanho)
print("")

##########

# Função sair
def s():
    time.sleep(0.3)
    print("Saindo!")

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
    print("Fazendo "+rando()+str(quantas)+" \033[0mimagens de "+rando()+"'"+imag+"'\033[0m")

print("Para cancelar feche o programa")

tamx, tamy = tamy, tamx
for numimg, imag in enumerate(imagens):
    for i in range(0,int(quantas),1):
        if i == 0:
            print('https://pollinations.ai/prompt/'+imag+"?width="+str(tamx)+"&height="+str(tamy)+"&nofeed=true")
            response = requests.get('https://pollinations.ai/prompt/'+imag+"?width="+str(tamx)+"&height="+str(tamy)+"&nofeed=true")
        else:
            print('https://pollinations.ai/prompt/'+imag+"?width="+str(tamx)+"&height="+str(tamy)+"&seed="+str(i)+"&nofeed=true")
            response = requests.get('https://pollinations.ai/prompt/'+imag+"?width="+str(tamx)+"&height="+str(tamy)+"&seed="+str(i)+"&nofeed=true")

        if response.status_code == 502 or response.status_code == 200:
            
            print(rando() + "feito " + str(i + 1) + "/" + quantas + "\033[0m")
            if i == 0:
                nome = diretsave + imag + '.jpg'
            else:
                nome = diretsave + imag + str(i + 1) + '.jpg'
            try:
                f = open(nome, 'wb')
            except:
                print("Erro ao gerar imagens")
                input("clique ENTER para continuar")

            f.write(response.content)
            f.close()
            imagenscaminho.append(os.path.abspath(nome))
        else:
            print('Erro ao fazer o download da imagem!')
            print("erro:",response.status_code)
            s()
    print("------------------------------------------------------------------------------------------------------------")
    print("")
     
print("Feito com sucesso!")
s()
