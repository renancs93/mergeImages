import sys
import os
import time
from PIL import Image, ImageOps, ExifTags
from tqdm import tqdm

def func_eh_imagem(nome_arquivo):
    ext_permitidas = [".png", ".jpg"]
    if nome_arquivo.lower().endswith(tuple(ext_permitidas)):
        return True
    return False    

def isImageVertical(foto):
    data = ImageOps.exif_transpose(foto)
    largura, altura = data.size
    
    # print(largura, altura)

    if altura > largura:
        return True
    return False

def needRotate(image):
    try:
        image = ImageOps.exif_transpose(image)
        
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        
        exif = image.getexif()
        
        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)

        return image
    except (AttributeError, KeyError, IndexError):
        # print("Foto sem EXIF Data")
        return image


def func_join_images(input_dir,  output_dir, img_fundo, img_fundo_secundaria):
    
    print('--- EXECUTANDO ---')
    
    # verifica se a pasta de destino existe, senão cria
    pastaOutput = "./"+output_dir
    if not os.path.exists(pastaOutput):
        print('-- criando pasta de Output --')
        os.mkdir(pastaOutput)

    sucesso = 0

    # Definição medida da moldura
    size_moldura = (1400, 1400) # Tamanho de uma post do Instagram (Dafault)
    # size_moldura = (1080, 1080) # Tamanho de uma post do Instagram (Reduzido)

    lista_arquivos = [nome for nome in os.listdir(input_dir) if func_eh_imagem(nome)]
    for nomeArq in tqdm(lista_arquivos, ascii=True, desc="Progresso"):
        
        # Get Itens recebidos por parametros
        fundo = Image.open(img_fundo)
        img = Image.open(os.path.join(input_dir, nomeArq)).convert("RGBA")
        
        # Definição das medidas da imagem
        size_img = (1365, 1022) # Default
        # size_img = (1053, 593) # Imagem original HEIC (iPhone)
        if img_fundo_secundaria is not None and isImageVertical(img):
            size_img = (900, 1273) # Default
            # size_img = (554, 985) # Imagem original HEIC (iPhone)
            fundo = Image.open(img_fundo_secundaria)

            # if 'Fundo_Logo.png' in img_fundo:
            #     fundo = Image.open(img_fundo.replace('Fundo_Logo.png', 'Fundo_LogoVert.png'))
            #     size_img = (878, 1168) # Imagem Vertical
            #     # size_img = (723, 1284) # Imagem Vertical 2
            # else:
            #     size_img = (900, 1273) # Imagem Vertical Expandida

        # Verificar se a foto precisa ser girada
        img = needRotate(img)

        # Redimensionamento das imagens
        editFundo = fundo.resize(size_moldura)
        editImg = img.resize(size_img, Image.ANTIALIAS) ## Default

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
        # print(f'Editado Imagem >> {nome_sem_ext}')
        sucesso += 1

    print(f'--- FINALIZADO ---')
    print(f'--- Total de imagens editadas: {sucesso} ---')


if __name__ == "__main__":

    parametros = sys.argv[1:]
    total_params = len(parametros)
    if(total_params >= 2):
        time_start = time.time()
        if(total_params == 3):
            func_join_images(parametros[0], 'editadas', parametros[1], parametros[2])
        else:
            func_join_images(parametros[0], 'editadas', parametros[1], None)
        duraction = (time.time() - time_start)
        print(f'--- Tempo de Duração: {time.strftime("%H:%M:%S", time.gmtime(duraction))} ---')
    else:
        print('Paramentros necessários ao script: [diretorio de imagens] [img de fundo] [-- opcional img de fundo secundaria]')
