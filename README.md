# Merge Images
Script em Python de junção de Images

O projeto contém um script (script_mergeImage.py), que permite você definir uma imagem de fundo padrão e passar um repositório contendo várias imagens, será gerado uma nova imagem editada para cada item encontrado no repositório listado.

Obs: A medida final da moldura está adequada para postagem do Instagram (1400 x 1400)

## Abaixo um exemplo do comando para executar:

Modelo: 
<code>
  python script_mergeImage.py [diretorio de imagens] [img de fundo] [img fundo secundaria vertical --opcional]
</code>

Exemplo
<code>
  python.exe script_mergeImage.py images/ moldura/Fundo_Logo.png moldura/Fundo_LogoVert.png
</code>

## Resultado:

<kbd align="center">
  <img src="https://github.com/renancs93/mergeImages/blob/master/screenshots/897d27fc262f890552a3f404ff2b4c28_orig.png" width="50%" title="imagem original">
</kbd>
<kbd align="center">
  <img src="https://github.com/renancs93/mergeImages/blob/master/screenshots/897d27fc262f890552a3f404ff2b4c28.png" width="50%" title="imagem editada">
</kbd>
