#TODO
#add line graphs

#import statements
import PIL.Image, PIL.ImageFont, PIL.ImageDraw, os, json

#main error cclass
class pygraphGraphicsException(Exception):
    module = 'graphics.py'

#main class for a bar graph
class createBlankBarGraph(object):

    #variables
    graphColorSheetPath = None
    colorSheetData = None
    graphImage = None

    #function to initialize the class
    def __init__(self, graphColorSheetPath) -> None:

        #set the variable for the color sheet path
        self.graphColorSheetPath = graphColorSheetPath

        #load the color sheet
        if (self.loadColorSheet()):
            pass
        else:
            raise pygraphGraphicsException('For some reason loadColorSheet() returned false, this should never happen. Reinstalling the module should fix this.')
    
    #function to load the color sheet
    def loadColorSheet(self) -> bool:

        #validify that the path to the color sheet exists
        try:
            assert os.path.exists(self.graphColorSheetPath)
        except AssertionError:
            raise FileNotFoundError('The graph color sheet located at "{}" was not found.'.format(self.graphColorSheetPath))

        #load the json data
        jsonData = json.loads(str(open(self.graphColorSheetPath).read()))

        #validify the json data (oooo yea dont we love memory eating try catches)
        try:
            assert "linearGraphColors" in jsonData
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load doesnt contain the key "linearGraphColors", so it failed to load.')
        try:
            assert type(jsonData['linearGraphColors']) == list
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load had a non list value for "linearGraphColors", so it failed to load.')
        try:
            assert len(jsonData['linearGraphColors']) >= 1
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load had a list with no values for "linearGraphColors", so it failed to load.')
        try:
            assert "textSizeForCoordinates" in jsonData
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load does not contain the key "textSizeForCoordinates", so it failed to load.')
        try:
            assert type(jsonData['textSizeForCoordinates']) == int
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load supplied a non integer value for "textSizeForCoordinates", so it failed to load.')
        try:
            assert jsonData['textSizeForCoordinates'] >= 0
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load supplied an integer value less than zero for "textSizeForCoordinates", so it failed to load.')
        try:
            assert jsonData['textSizeForCoordinates'] != float('inf')
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load supplied infinity as the value for "textSizeForCoordinates", so it failed to load.')
        try:
            assert "textSizeForTitles" in jsonData
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load does not contain the key "textSizeForTitles", so it failed to load.')
        try:
            assert type(jsonData['textSizeForTitles']) == int
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load supplied a non integer value for "textSizeForCoodinates", so it failed to load.')
        try:
            assert jsonData['textSizeForTitles'] >= 0
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load supplied an integer value less than zero for "textSizeForTitles", so it failed to load.')
        try:
            assert jsonData['textSizeForTitles'] != float('inf')
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load supplied infinity as the value for "textSizeForCoordinates", so it failed to load.')
        try:
            assert backgroundColor in jsonData
        except AssertionError:
            raise pygraphGraphicsException('THe graph color sheet you attempted to load does not contain the key "backgroundColor", so it failed to load.')

        #since it is valid then set the color data to this
        self.colorSheetData = jsonData

        #return true since this succeeded
        return True