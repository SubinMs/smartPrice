from PIL import Image,ImageDraw,ImageFont


def draw_borders(pillow_image,bounding,color,image_size,caption='',confidence_score=0):

    width, height = image_size
    draw = ImageDraw.Draw(pillow_image)
    draw.polygon([
        bounding.normalized_vertices[0].x * width,
        bounding.normalized_vertices[0].y * height,
        bounding.normalized_vertices[1].x * width,
        bounding.normalized_vertices[1].y * height,
        bounding.normalized_vertices[2].x * width ,
        bounding.normalized_vertices[2].y * height,
        bounding.normalized_vertices[3].x * width,
        bounding.normalized_vertices[3].y * height
    ],fill=None, outline=color)
    
    return pillow_image
