import io, os
from numpy import random
from google.cloud import vision
from Pillow_Utility import draw_borders, Image
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"GoogleCloudDemo_ServiceAcct_Token.json"
client = vision.ImageAnnotatorClient()


img_list = os.listdir('./images')

#file_name = 'image_name.jpg'
file_name = img_list[0]
image_path = os.path.join('./images', file_name)
save_path = os.path.join('./test_images/')
static_path = os.path.join('./static/result_img/')


with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.object_localization(image=image)
localized_object_annotations = response.localized_object_annotations

pillow_image = Image.open(image_path)
df = pd.DataFrame(columns=['name', 'score'])

img_size = list(pillow_image.size)
width = img_size[0]
height = img_size[1]

ob = 0
for obj in localized_object_annotations:
    df = df.append(
        dict(
            name=obj.name,
            score=obj.score
        ),
        ignore_index=True)

    if (obj.name=='Mobile phone') : 
        vr = dict(ld_x=obj.bounding_poly.normalized_vertices[0].x * width,ld_y=obj.bounding_poly.normalized_vertices[0].y * height,
                  ru_x=obj.bounding_poly.normalized_vertices[2].x * width,ru_y=obj.bounding_poly.normalized_vertices[2].y * height)
        
        leftDown_x = int(vr['ld_x'])
        leftDown_y = int(vr['ld_y'])
        rightup_x = int(vr['ru_x'])
        rightup_y = int(vr['ru_y'])
        
        ob = ob + 1
        con = str(ob)
        
        im = Image.open('images/'+file_name)
        crp = im.crop((leftDown_x,leftDown_y,rightup_x,rightup_y))
        crp.show()
        
        crp.save(save_path+'img_'+con+'.jpg',format='JPEG')
        crp.save(static_path+'img_'+con+'.jpg',format='JPEG')
    #end if
    r, g, b = random.randint(150, 255), random.randint(
        150, 255), random.randint(150, 255)

    draw_borders(pillow_image, obj.bounding_poly, (r, g, b),
                 pillow_image.size, obj.name, obj.score)
#end for

#os.remove(image_path)



