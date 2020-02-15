import imageio

img = imageio.imread('mountains.jpeg')
proc = []

for i in range(200): #len(img)
    row = []
    for j in range(200):  #len(img[i])
        sum = 0;
        for k in range(3):
            sum += img[i][j][k]
        sum //= 3
        row.append(sum)
    proc.append(row)       

imageio.imwrite('mod.jpg', proc)

# print(proc)