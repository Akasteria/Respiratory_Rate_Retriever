from enum import Enum
import numpy
import matplotlib
from matplotlib.colors import ListedColormap
class UIColor(Enum):
    EMPTY = (0,0,0) # black
    NORMAL = (0.1,0.3,0.4) # blue
    WARNING = (0.4,0.4,0.1) # Yellow
    OKAY = (0.1,0.4,0.3) # Green
    ERROR = (0.4,0.2,0.2) # Red
class ColorDescription(Enum):
    EMPTY = 'No Data'
    NORMAL = 'Normal'
    WARNING = 'Elevated'
    OKAY = 'Normal+Exercising'
    ERROR = 'Elevated+Exercising'
def ColorToDescription(color):
    for enum in UIColor:
        if (enum.value == color):
            return ColorDescription[enum.name].value
    raise ValueError('No matching UI color')
def EnumToDescription(enum):
    return ColorDescription[enum.name].value
def ColorMap():
    cMapName = 'RRR cmap' # The 4 colors 0 = missing data (Black), 1 = normal (Light blue), 2 = abnormal (Light Yellow), 3 = exercising (Green)
    colorMap = ListedColormap(UIColors(), name = cMapName)
    bounds = numpy.arange(len(UIColors())+1)
    normal = matplotlib.colors.BoundaryNorm(bounds, colorMap.N)
    return normal, colorMap
def UIColors(i = -1):
    ls = []
    for uiColor in UIColor:
        ls.append(uiColor.value)
    if (i == -1):
        return ls
    return ls[i]
def BrightUIColors(i = -1):
    ls = []
    for uiColor in UIColor:
        newColor = (uiColor.value[0] * 2, uiColor.value[1] * 2,uiColor.value[2] * 2)
        ls.append(newColor)
    if (i == -1):
        return ls
    return ls[i]
def StyledText(text,color,size,font):
    newColor = (color[0] * 255,color[1] * 255,color[2] * 255)
    strColor = str(newColor)
    string = '<p style="color:rgb' + strColor + ';font-family:'+ font + ';font-size:' + str(size) + 'px;">'+ text + '</p>'
    return string
if __name__ == '__main__':
    pass