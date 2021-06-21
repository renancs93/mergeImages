import sys
import os
from PIL import Image

def func_eh_imagem(nome_arquivo):
    ext_permitidas = [".png", ".jpg"]
    if nome_arquivo.endswith(tuple(ext_permitidas)):
        return True
    return False    

def isImageVertical(foto):
    largura, altura = foto.size
    if altura > largura:
        return True
    return False

def func_join_images(img_fundo, input_dir, output_dir):
    
    print('--- EXECUTANDO ---')

    # verifica se a pasta de destino existe, senão cria
    pastaOutput = "./"+output_dir
    if not os.path.exists(pastaOutput):
        print('-- criando pasta de Output --')
        os.mkdir(pastaOutput)

    sucesso = 0

    # Definição medida da moldura
    size_moldura = (1400, 1400) # Tamanho de uma post do Instagram

    lista_arquivos = [nome for nome in os.listdir(input_dir) if func_eh_imagem(nome)]
    for nomeArq in lista_arquivos:
        
        # Get Itens recebidos por parametros
        fundo = Image.open(img_fundo)
        img = Image.open(os.path.join(input_dir, nomeArq)).convert("RGBA")
        
        # Definição das medidas da imagem
        # size_img = (1126, 844) # Imagem Horizontal
        size_img = (1365, 1022) # Imagem Horizontal 2
        if isImageVertical(img):
            if 'Fundo_Logo.png' in img_fundo:
                fundo = Image.open(img_fundo.replace('Fundo_Logo.png', 'Fundo_LogoVert.png'))
                size_img = (878, 1168) # Imagem Vertical
            else:
                size_img = (900, 1273) # Imagem Vertical Expandida

        # Redimensionamento das imagens
        editFundo = fundo.resize(size_moldura)
        editImg = img.resize(size_img, Image.ANTIALIAS)

        # Calculo para centralização da imagem principal com o fundo
        w1, h1 = editFundo.size
        w2, h2 = editImg.size

        if w1 > w2:
            x = int((w1 - w2) / 2)
            y = int((h1 - h2) / 2)
        else:
            x = int((w2 - w1) / 2)
            y = int((h2 - h1) / 2)

        # # Junção da imagem principal sobre a imagem de fundo
        editFundo.paste(editImg, (x, y), editImg)
        # # editFundo.show()

        nome_sem_ext = os.path.splitext(nomeArq)[0]

        editFundo.save(os.path.join(output_dir, nome_sem_ext + '.png'))
        print(f'Editado Imagem >> {nome_sem_ext}')
        sucesso += 1

    print(f'--- FINALIZADO ---')
    print(f'--- Total de imagens editadas: {sucesso} ---')


if __name__ == "__main__":

    parametros = sys.argv[1:]

    if(len(parametros) >= 2):
        func_join_images(parametros[0], parametros[1], 'editadas')
    else:
        print('Paramentros necessários ao script: [img de fundo] [diretorio de imagens]')
