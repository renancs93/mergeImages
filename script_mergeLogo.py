import sys
import os
import time
from PIL import Image, ImageOps, ExifTags
from tqdm import tqdm
from pillow_heif import register_heif_opener

# HEIC image extension support
register_heif_opener()

# Dimensão padrão das imagens (apenas de um dos lados)
BASE_HORIZ = 1200
BASE_VERT = 1365
BASE_MARGEM = 5

SIZE_IMG_LOGO = (150, 150)

# TopLeft | TopRight | BottomLeft | BottomRight
LIST_POSITIONS = ['TL', 'TR', 'BL', 'BR']

def func_eh_imagem(nome_arquivo):
    ext_permitidas = [".png", ".jpg", ".jpeg", ".heic"]
    if nome_arquivo.lower().endswith(tuple(ext_permitidas)):
        return True
    return False    

def isImageVertical(foto):
    largura, altura = getDimensionsImg(foto)
    if altura >= largura:
        return True
    return False

def getDimensionsImg(foto):
    data = ImageOps.exif_transpose(foto)
    return data.size

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


def func_join_images(input_dir,  output_dir, img_logo, logo_position):
    
    print('--- EXECUTANDO ---')
    
    # verifica se a pasta de destino existe, senão cria
    pastaOutput = "./"+output_dir
    if not os.path.exists(pastaOutput):
        print('-- criando pasta de Output --')
        os.mkdir(pastaOutput)

    sucesso = 0

    # Definição medida do logo
    size_logo = SIZE_IMG_LOGO

    lista_arquivos = [nome for nome in os.listdir(input_dir) if func_eh_imagem(nome)]
    for nomeArq in tqdm(lista_arquivos, ascii=True, desc="Progresso"):
        
        # Get Itens recebidos por parametros
        logo = Image.open(img_logo)
        img = Image.open(os.path.join(input_dir, nomeArq)).convert("RGBA")

        # Verificar se a foto precisa ser girada
        img = needRotate(img)

        # Calculo das dimenções pela proporção (Foto Horizontal)
        ww, hh = getDimensionsImg(img)
        wpercent = (BASE_HORIZ/float(ww))
        hsize = int((float(hh)*float(wpercent)))
        
        # Definição das medidas da imagem
        size_img = (BASE_HORIZ, hsize) # Default Horizontal
        
        if isImageVertical(img): 
            # Calculo das dimenções pela proporção (Foto Vertical)
            hpercent = (BASE_VERT/float(hh))
            wsize = int((float(ww)*float(hpercent)))
            size_img = (wsize, BASE_VERT) # Default Vertical
            
        # Redimensionamento das imagens
        editLogo = logo.resize(size_logo)
        editImg = img.resize(size_img, Image.ANTIALIAS) ## Default

        # Extração das medidas das imagens
        w1, h1 = editLogo.size
        w2, h2 = editImg.size

        # Posição Padrão Logo (BottomRight)
        x = int((w2 - w1) - BASE_MARGEM)
        y = int((h2 - h1) - BASE_MARGEM)
        # Posicionamento do Logo
        if logo_position in LIST_POSITIONS:
            if logo_position == 'BR':
                x = int((w2 - w1) - BASE_MARGEM)
                y = int((h2 - h1) - BASE_MARGEM)
            if logo_position == 'BL':
                x = int(BASE_MARGEM)
                y = int((h2 - h1) - BASE_MARGEM)
            if logo_position == 'TL':
                x = int(BASE_MARGEM)
                y = int(BASE_MARGEM)
            if logo_position == 'TR':
                x = int((w2 - w1) - BASE_MARGEM)
                y = int(BASE_MARGEM)

        # Junção do Logo com a imagem principal
        editImg.paste(editLogo, (x, y), editLogo)
        
        nome_sem_ext = os.path.splitext(nomeArq)[0]

        editImg.save(os.path.join(output_dir, nome_sem_ext + '.png'))
        sucesso += 1

    print(f'--- FINALIZADO ---')
    print(f'--- Total de imagens editadas: {sucesso} ---')


if __name__ == "__main__":

    parametros = sys.argv[1:]
    total_params = len(parametros)
    if(total_params >= 2):
        time_start = time.time()
        if(total_params == 3):
            func_join_images(parametros[0], 'editadas', parametros[1], parametros[2].upper())
        else:
            func_join_images(parametros[0], 'editadas', parametros[1], None)
        duraction = (time.time() - time_start)
        print(f'--- Tempo de Duração: {time.strftime("%H:%M:%S", time.gmtime(duraction))} ---')
    else:
        print('Parametros necessarios ao script: [diretorio de imagens] [img do logo] [posicao logo --opcional (tl, tr, bl, br) TopLeft | TopRight | BottomLeft | BottomRight]')
