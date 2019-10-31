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
    graphImage = {'base':None,'draw':None}
    graphBarsMax = None
    graphTitle = 'Title'
    graphXTitle = 'X Axis Title'

    #function to initialize the class
    def __init__(self, graphColorSheetPath, width, height) -> None:

        #set the variable for the color sheet path
        self.graphColorSheetPath = graphColorSheetPath

        #load the color sheet
        if (self.loadColorSheet()):
            pass
        else:
            raise pygraphGraphicsException('For some reason loadColorSheet() returned false, this should never happen. Reinstalling the module should fix this.')

        #set the variables
        self.graphImage['base'] = PIL.Image.new('RGBA', [width, height], self.colorSheetData['backgroundColor'])
        self.graphImage['draw'] = PIL.ImageDraw.Draw(self.graphImage['base'])

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
            assert "graphDataColors" in jsonData
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load doesnt contain the key "graphDataColors", so it failed to load.')
        try:
            assert type(jsonData['graphDataColors']) == list
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load had a non list value for "graphDataColors", so it failed to load.')
        try:
            assert len(jsonData['graphDataColors']) >= 1
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load had a list with no values for "graphDataColors", so it failed to load.')
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
            assert 'backgroundColor' in jsonData
        except AssertionError:
            raise pygraphGraphicsException('THe graph color sheet you attempted to load does not contain the key "backgroundColor", so it failed to load.')

        #since it is valid then set the color data to this
        self.colorSheetData = jsonData

        #return true since this succeeded
        return True
    
    #function to save the graph to an image file
    def save(self, path, barGraphTopPadding = 200, barGraphSidePadding = 100, barGraphBottomPadding = 100, drawTitles = True, drawBorders = True) -> str:

        #convert the path to a string just in case
        path = str(path)

        #calculate the zone where the graphs should be is
        barGraphSafeZoneBounds = [
            [int(barGraphSidePadding), int(barGraphTopPadding)],
            [int(self.graphImage['base'].size[0] - barGraphSidePadding), int(self.graphImage['base'].size[1] - barGraphTopPadding)]
        ]

        #if the user wants to draw the borders then draw them
        if (drawBorders):

            #get the border color
            borderColor = self.colorSheetData['borderColor']

            #draw the borders
            self.graphImage['draw'].line([
                (*barGraphSafeZoneBounds[0]),
                (int(barGraphSafeZoneBounds[0][0]), int(barGraphSafeZoneBounds[1][1])),
                (*barGraphSafeZoneBounds[1])
            ], fill = borderColor, width = 2)

        #save the image
        self.graphImage['base'].save(path)

        #return the path to the image
        return path