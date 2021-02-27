from enum import Enum
import numpy
import matplotlib
from matplotlib.colors import ListedColormap
class UIColor(Enum):
    EMPTY = (0,0,0) # black
    NORMAL = (0.1,0.3,0.4) # blue
    OKAY = (0.4,0.4,0.1) # Green
    WARNING = (0.1,0.4,0.3) # Yellow
def ColorMap():
    cMapName = 'RRR cmap' # The 4 colors 0 = missing data (Black), 1 = normal (Light blue), 2 = abnormal (Light Yellow), 3 = exercising (Green)
    colorMap = ListedColormap(UIColors(), name = cMapName)
    bounds = numpy.arange(len(UIColors())+1)
    normal = matplotlib.colors.BoundaryNorm(bounds, colorMap.N)
    return normal, colorMap
def UIColors():
    ls = []
    for uiColor in UIColor:
        ls.append(uiColor.value)
    return ls
def BrightUIColors():
    ls = []
    for uiColor in UIColor:
        newColor = (uiColor.value[0] * 2, uiColor.value[1] * 2,uiColor.value[2] * 2)
        ls.append(newColor)
    return ls
def StyledText(text,color,size,font):
    newColor = (color[0] * 255,color[1] * 255,color[2] * 255)
    strColor = str(newColor)
    string = '<p style="color:rgb' + strColor + ';font-family:'+ font + ';font-size:' + str(size) + 'px;">'+ text + '</p>'
    return string