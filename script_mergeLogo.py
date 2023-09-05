import sys
import os
import time
import utilities.util as util
from PIL import Image
from tqdm import tqdm
from pillow_heif import register_heif_opener

# HEIC image extension support
register_heif_opener()

# Dimensão padrão das imagens (apenas de um dos lados)
BASE_HORIZ = 1080
BASE_VERT = 1350
BASE_MARGEM = 5

SIZE_IMG_LOGO = (120, 120)
SIZE_IMG_LOGO_V = (180, 180)

# LeftTop | LeftBottom | RightBottom | RightTop
LIST_POSITIONS = ['LT', 'LB', 'RB', 'RT']

def func_merge_images(input_dir, img_logo, logo_position, output_dir):
    
    print('--- EXECUTANDO ---')
    
    # verifica se a pasta de destino existe, senão cria
    pastaOutput = "./"+output_dir
    if not os.path.exists(pastaOutput):
        print('-- Criando pasta de Output --')
        os.mkdir(pastaOutput)

    print(f'Salvando em: {os.path.abspath(pastaOutput)}')
    sucesso = 0

    # Definição medida do logo
    size_logo = SIZE_IMG_LOGO

    lista_arquivos = [nome for nome in os.listdir(input_dir) if util.is_valid_image(nome)]
    for nomeArq in tqdm(lista_arquivos, ascii=True, desc="Progresso"):
        
        # Get Itens recebidos por parametros
        logo = Image.open(img_logo)
        img = Image.open(os.path.join(input_dir, nomeArq)).convert("RGBA")

        # Verificar se a foto precisa ser girada
        img = util.need_rotate(img)

        # Calculo das dimenções pela proporção (Foto Horizontal)
        ww, hh = util.get_image_dimensions(img)
        wpercent = (BASE_HORIZ/float(ww))
        hsize = int((float(hh)*float(wpercent)))
        
        # Definição das medidas da imagem
        size_img = (BASE_HORIZ, hsize) # Default Horizontal
        
        if util.is_vertical_image(img): 
            # Calculo das dimenções pela proporção (Foto Vertical)
            hpercent = (BASE_VERT/float(hh))
            wsize = int((float(ww)*float(hpercent)))
            size_img = (wsize, BASE_VERT) # Default Vertical
            size_logo = SIZE_IMG_LOGO_V
            
        # Redimensionamento das imagens
        editLogo = logo.resize(size_logo, Image.ANTIALIAS)
        editImg = img.resize(size_img, Image.ANTIALIAS) ## Default

        # Extração das medidas das imagens
        w1, h1 = editLogo.size
        w2, h2 = editImg.size

        # Posição Padrão Logo (RB)
        x = int((w2 - w1) - BASE_MARGEM)
        y = int((h2 - h1) - BASE_MARGEM)
        # Posicionamento do Logo
        if logo_position in LIST_POSITIONS:
            if logo_position == 'RB':
                x = int((w2 - w1) - BASE_MARGEM)
                y = int((h2 - h1) - BASE_MARGEM)
            elif logo_position == 'RT':
                x = int((w2 - w1) - BASE_MARGEM)
                y = int(BASE_MARGEM)
            elif logo_position == 'LB':
                x = int(BASE_MARGEM)
                y = int((h2 - h1) - BASE_MARGEM)
            elif logo_position == 'LT':
                x = int(BASE_MARGEM)
                y = int(BASE_MARGEM)

        # Junção do Logo com a imagem principal
        editImg.paste(editLogo, (x, y), editLogo)
        
        nome_sem_ext = os.path.splitext(nomeArq)[0]

        editImg.save(os.path.join(output_dir, nome_sem_ext + '.png'))
        sucesso += 1

    print(f'--- FINALIZADO ---')
    print(f'--- Total de imagens editadas: {sucesso} ---')


if __name__ == "__main__":

    params = sys.argv[1:]
    total_params = len(params)
    if(total_params >= 2 and total_params <= 4):
        time_start = time.time()
        if(total_params == 2):
            func_merge_images(input_dir=params[0], img_logo=params[1], logo_position=None, output_dir='editadas')
        elif(total_params == 3):
            func_merge_images(input_dir=params[0], img_logo=params[1], logo_position=params[2].upper(), output_dir='editadas')
        elif(total_params == 4):
            func_merge_images(input_dir=params[0], img_logo=params[1], logo_position=params[2].upper(), output_dir=params[3])

        stop_watch = (time.time() - time_start)
        print(f'--- Tempo de Duração: {time.strftime("%H:%M:%S", time.gmtime(stop_watch))} ---')
    else:
        print('Parametros do script: [dir de input] [img do logo] [posicao logo --opcional (LT, LB, RB, RT)] [dir de output --opcional]')
