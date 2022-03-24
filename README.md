# Merge Images

Script em Python de junção de Images

O projeto contém um script (script_mergeImage.py), que permite você definir uma imagem de fundo padrão e passar um repositório contendo várias imagens, será gerado uma nova imagem editada para cada item encontrado no repositório listado.

Obs: O script contém variáveis com dimensões padrões da imagem de fundo (SIZE_IMG_BACKGROUND) e tamanhos base para imagens horizontal (BASE_HORIZ) e vertical (BASE_VERT), se for necessário atualize de acordo com a necessidade.

- Requisitos:
  - Python
  - Pillow (pip install Pillow)
  - tqdm (pip install tqdm)

## Exemplo de comando para executar:

Modelo:
<code>
python script_mergeImage.py [diretorio de imagens] [img de fundo] [img fundo secundaria vertical --opcional]
</code>

Exemplo
<code>
python script_mergeImage.py imagens/ moldura/Fundo_Logo2.png
</code>

## Resultados:
<div align="center">
  Imagem Original:
  <div>
    <img src="https://github.com/renancs93/mergeImages/blob/master/screenshots/897d27fc262f890552a3f404ff2b4c28_orig.png" width="50%" title="imagem original">
  </div>
  <hr>
  Imagem Editada:
  <div>
    <img src="https://github.com/renancs93/mergeImages/blob/master/screenshots/897d27fc262f890552a3f404ff2b4c28.png" width="50%" title="imagem editada">
  </div>
</div>
