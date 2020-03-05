
import numpy
from PIL import Image, BmpImagePlugin

img: BmpImagePlugin.BmpImageFile = Image.open(r"D:\Nadin hlam\lab2.bmp")
width, height = img.size
print(img.size)

pix = numpy.asarray(img)
# print(pix)

# вывод текущего изображения
# for x in range(width):
#     for y in range(height):
#         #print(f'x = {x}/{width}, y = {y}/{height}')
#         print(pix[y][x], end='')
#     print()

# создание пустого поля = карты лабиринта (заполнение его 0) для обозначения входа/выходы, стен, пустого места
lab = [[0 for i in range(width)] for i in range(height)]

# -2 - вход, -3 - выход, -1 - стена, 0 - свободное пространство. Заполнение lab обозначениями
entry = None
has_finish = False

for x in range(width):
    for y in range(height):
        pixel = pix[y][x]
        if pixel[1] >= 130 and pixel[0] < 100 and pixel[2] < 100:
            if not entry:
                lab[y][x] = -2
                entry = (x, y)
            else:
                lab[y][x] = -3
                has_finish = True
        elif pixel[1] < 200 and pixel[0] < 200 and pixel[2] < 200:
            lab[y][x] = -1

# если не отмечены точки входа и выхода
if not has_finish:
    print('нет двух зеленых точек!')
    exit()

# полученный заполненный lab
# for x in range(width):
#     for y in range(height):
#         print(lab[y][x], end='\t')
#     print()

# лист очереди
queue = [entry]
finish_point = None

# проверка точки, добавление значения
def check(x, y, source_xy):
    if x < 0 or y < 0 or x >= width or y >= height:
        return
    if lab[y][x] == 0:
        lab[y][x] = source_xy
        queue.append((x, y))
        return
    if lab[y][x] == -3:
        lab[y][x] = source_xy
        return x, y


while queue and not finish_point:
    point = queue.pop(0)
    x = point[0]
    y = point[1]
    finish_point = check(x-1, y, point) or finish_point
    finish_point = check(x+1, y, point) or finish_point
    finish_point = check(x, y-1, point) or finish_point
    finish_point = check(x, y+1, point) or finish_point

# печать заполненного лабиринта
# for x in range(width):
#     for y in range(height):
#         print(lab[y][x], end='\t')
#     print()

# если не найден выход
if not finish_point:
    print('Выхода нет')
    exit()

# рисование дороги домой
point = finish_point

while point != -2:
    x = point[0]
    y = point[1]
    point = lab[y][x]
    img.putpixel((x, y), (255, 0, 0))

img.save(r'D:\Nadin hlam\rez.bmp', 'bmp')
