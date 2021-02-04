from PIL import Image

fundo = Image.open("moldura/Moldura_Central.png")
img = Image.open("img/frase.png").convert("RGBA")

# Imagem Central - largura 353 / altura: 1015
# Moldura - largura 1400 / altura: 1400

size_moldura = (1400, 1400)
size_img = (1353, 1015)

editFundo = fundo.resize(size_moldura)
editImg = img.resize(size_img)

print(f"SIZE: {editFundo.size}")
print(f"SIZE: {editImg.size}")

w1, h1 = editFundo.size
w2, h2 = editImg.size

if w1 > w2:
    x = int((w1 - w2) / 2)
    y = int((h1 - h2) / 2)
else:
    x = int((w2 - w1) / 2)
    y = int((h2 - h1) / 2)
    

print(f'X: {x} -  Y: {y}')

editFundo.paste(editImg, (x, y), editImg)
editFundo.show()
editFundo.save("editadas/edit1.png")
