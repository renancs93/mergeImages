import sys
import os
import time
import utilities.util as util
from PIL import Image, ImageOps, ExifTags
from tqdm import tqdm
from pillow_heif import register_heif_opener

# HEIC image extension support
register_heif_opener()

# Dimensão padrão das imagens (apenas de um dos lados)
BASE_HORIZ = 1365
BASE_VERT = 1200

SIZE_IMG_BACKGROUND = (1400, 1400)

def func_join_images(input_dir, img_fundo, output_dir):
    
    print('--- EXECUTANDO ---')
    
    # verifica se a pasta de destino existe, senão cria
    pastaOutput = "./"+output_dir
    if not os.path.exists(pastaOutput):
        print('-- Criando pasta de Output --')
        os.mkdir(pastaOutput)

    print(f'Salvando em: {os.path.abspath(pastaOutput)}')
    sucesso = 0

    # Definição medida da moldura
    size_moldura = SIZE_IMG_BACKGROUND # Tamanho de uma post do Instagram (Dafault)

    lista_arquivos = [nome for nome in os.listdir(input_dir) if util.is_valid_image(nome)]
    for nomeArq in tqdm(lista_arquivos, ascii=True, desc="Progresso"):
        
        # Get Itens recebidos por parametros
        fundo = Image.open(img_fundo)
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
    if(total_params >= 2 and total_params <= 3):
        time_start = time.time()
        if(total_params == 3):
            func_join_images(input_dir=parametros[0], img_fundo=parametros[1], output_dir=parametros[2])
        else:
            func_join_images(input_dir=parametros[0], img_fundo=parametros[1], output_dir='editadas')
        
        duraction = (time.time() - time_start)
        print(f'--- Tempo de Duração: {time.strftime("%H:%M:%S", time.gmtime(duraction))} ---')
    else:
        print('Parametros necessarios ao script: [diretorio de imagens] [img de fundo] [diretorio de destino --opcional]')