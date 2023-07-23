from PIL import Image, ImageDraw

# 打开图片文件
im = Image.open('logo-prin.png')

# 将图片转为正方形，裁剪掉多余的部分
width, height = im.size
if width > height:
    delta = (width - height) / 2
    box = (delta, 0, width - delta, height)
else:
    delta = (height - width) / 2
    box = (0, delta, width, height - delta)
im = im.crop(box)

# 新建一个白色背景的圆形图片
size = im.size
mask = Image.new('L', size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, size[0], size[1]), fill=255)

# 将原始图片和掩码图片合并，裁剪出圆形图片
output = Image.new('RGBA', size, (255, 255, 255, 0))
output.paste(im, (0, 0), mask)
output.save('circle_image.png')