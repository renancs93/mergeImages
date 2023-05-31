from PIL import ImageOps, ExifTags

def is_valid_image(filename):
    list_allowed_extensions = [".png", ".jpg", ".jpeg", ".heic"]
    if filename.lower().endswith(tuple(list_allowed_extensions)):
        return True
    return False    

def is_vertical_image(foto):
    largura, altura = get_image_dimensions(foto)
    if altura >= largura:
        return True
    return False

def get_image_dimensions(foto):
    data = ImageOps.exif_transpose(foto)
    return data.size

def need_rotate(image):
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