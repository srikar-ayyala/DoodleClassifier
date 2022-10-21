import random
import math


class transformationSettings:
    def __init__(self):
        self.offset = [0, 0]
        self.scale = 1
        self.angle = 0
        self.noiseProbability = 0
        self.noiseStrength = 0


def Sample(u, v, oldimg, size):
    u += 0.5
    v += 0.5

    u = max(0, min(1, u))
    v = max(0, min(1, v))

    texX = u * (size - 1)
    texY = v * (size - 1)

    indexLeft = int(texX)
    indexBottom = int(texY)
    indexRight = min(indexLeft + 1, size - 1)
    indexTop = min(indexBottom + 1, size - 1)

    blendX = texX - indexLeft
    blendY = texY - indexBottom

    bottomLeft = oldimg[indexLeft][indexBottom]
    bottomRight = oldimg[indexRight][indexBottom]
    topLeft = oldimg[indexLeft][indexTop]
    topRight = oldimg[indexRight][indexTop]

    valueBottom = bottomLeft + (bottomRight - bottomLeft) * blendX
    valueTop = topLeft + (topRight - topLeft) * blendX
    value = valueBottom + (valueTop - valueBottom) * blendY
    return value


def randomizeSettings(image):
    sett = transformationSettings()
    sett.angle = (random.random() - 0.5) * 0.3
    sett.scale = (random.random() - 0.5) * 0.3 + 1
    sett.noiseProbability = min(random.random(), random.random()) * 0.15
    sett.noiseStrength = min(random.random(), random.random()) * 200

    boundMinX, boundMinY = len(image), len(image)
    boundMaxX, boundMaxY = 0, 0

    for y in range(len(image)):
        for x in range(len(image)):
            if image[x][y] > 0:
                boundMinX = min(boundMinX, x)
                boundMaxX = max(boundMaxX, x)
                boundMinY = min(boundMinY, y)
                boundMaxY = max(boundMaxY, y)

    offsetMinX = -boundMinX / len(image)
    offsetMaxX = (len(image) - boundMaxX) / len(image)
    offsetMinY = -boundMinY / len(image)
    offsetMaxY = (len(image) - boundMaxY) / len(image)

    randX, randY = random.random(), random.random()
    offsetX = offsetMinX * (1 - randX) + offsetMaxX * randX
    offsetY = offsetMinY * (1 - randY) + offsetMaxY * randX
    sett.offset = [offsetX, offsetY]

    return sett


def TransformImage(t):
    size = len(t)
    sett = randomizeSettings(t)
    f = []
    iHat = [math.cos(sett.angle) / sett.scale, math.sin(sett.angle) / sett.scale]
    kHat = [-iHat[1], iHat[0]]
    #     print('\n\n', i)
    for x in range(size):
        ftemp = []
        for y in range(size):
            u = x / (size - 1)
            v = y / (size - 1)
            uTransformed = iHat[0] * (u - 0.5) + kHat[0] * (v - 0.5) - sett.offset[0]
            vTransformed = iHat[1] * (u - 0.5) + kHat[1] * (v - 0.5) - sett.offset[1]
            pixelValue = Sample(uTransformed, vTransformed, t, size)
            noiseVal = 0
            if random.random() <= sett.noiseProbability:
                noiseVal = (random.random() - 0.5) * sett.noiseStrength
            pixelValue = max(0, min(255, (pixelValue + noiseVal)))
            ftemp.append(pixelValue)
        f.append(ftemp)

    return f

