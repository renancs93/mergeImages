import sys
import os
from PIL import Image

def func_eh_imagem(nome_arquivo):
    if nome_arquivo.endswith('png') or nome_arquivo.endswith('jpg'):
        return True
    return False    

def isImageVertical(foto):
    largura, altura = foto.size
    if altura > largura:
        return True
    return False

def func_join_images(img_fundo, input_dir, output_dir):
    print('--- EXECUTANDO ---')

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
            fundo = Image.open(img_fundo.replace('Fundo_Logo.png', 'Fundo_LogoVert.png'))
            size_img = (878, 1168) # Imagem Vertical
            # # Para ajustes de fotos verticais
            # angle = 270
            # Image.rotate(angle, resample=0, expand=0, center=None, translate=None, fillcolor=None)[source]
            # img = img.rotate(angle, 1, 1)

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
        print(f'Editado Imagem >> {nomeArq}')
        sucesso += 1

    print(f'--- FINALIZADO ---')
    print(f'--- Total de imagens editadas: {sucesso} ---')


if __name__ == "__main__":

    parametros = sys.argv[1:]

    if(len(parametros) >= 2):
        func_join_images(parametros[0], parametros[1], 'editadas')
    else:
        print('Paramentros necessários ao script: [img de fundo] [diretorio de imagens]')
