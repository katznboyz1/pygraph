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
    graphYTitle = 'Y Axis Title'
    fontPath = None
    graphData = []

    #function to initialize the class
    def __init__(self, graphColorSheetPath, fontPath, width, height) -> None:

        #set the variable for the color sheet path
        self.graphColorSheetPath = graphColorSheetPath

        #load the color sheet
        if (self.loadColorSheet()):
            pass
        else:
            raise pygraphGraphicsException('For some reason loadColorSheet() returned false, this should never happen. Reinstalling the module should fix this.')

        #check that the font path is valid
        try:
            assert os.path.exists(fontPath)
        except AssertionError:
            raise FileNotFoundError('The font file located at "{}" was not found.'.format(fontPath))

        #set the font path
        self.fontPath = fontPath

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
            raise pygraphGraphicsException('The graph color sheet you attempted to load does not contain the key "backgroundColor", so it failed to load.')
        try:
            assert 'titleColors' in jsonData
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load does not contain the key "titleColors", so it failed to load.')
        try:
            assert type(jsonData['titleColors']) == dict
        except AssertionError:
            raise pygraphGraphicsException('The graph color sheet you attempted to load supplied a non dictionary value for "titleColors", so it failed to load.')

        #since it is valid then set the color data to this
        self.colorSheetData = jsonData

        #return true since this succeeded
        return True
    
    #function to add a value to the graph
    def addValue(self, valueTitle, valueMeasure) -> None:

        #convert the value title to a string
        valueTitle = str(valueTitle)

        #validate the value measure
        try:
            valueMeasure = int(valueMeasure)
        except ValueError:
            raise pygraphGraphicsException('The value measure that you supplied was not a valid integer. addValueToChart()\'s valueMeasure argument must be an integer.')
    
        #check that the value does not already exist
        try:
            assert not valueTitle in self.graphData
        except AssertionError:
            raise pygraphGraphicsException('The value title you supplied already exists. The graph can not have two entries with the same title. The value supplied was "{}".'.format(valueTitle))
        
        #store the values
        self.graphData.append([valueTitle, valueMeasure])

    #function to save the graph to an image file
    def save(self, path, barGraphTopPadding = 200, barGraphSidePadding = 100, barGraphBottomPadding = 200, drawTitles = True, drawBorders = True, maxDataPlotSize = float('inf'), bottomTitleTextSize = None) -> str:

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
        
        #if the user wants to draw the titles then draw them
        if (drawTitles):

            #get the title colors
            xAxisTitleColor = self.colorSheetData['titleColors']['xAxis']
            yAxisTitleColor = self.colorSheetData['titleColors']['yAxis']
            graphTitleColor = self.colorSheetData['titleColors']['graphTitle']

            #calculate the size of the y axis title
            yAxisTextFont = PIL.ImageFont.truetype(self.fontPath, int(barGraphSidePadding / 3))
            yAxisTextSize = self.graphImage['draw'].textsize(self.graphYTitle, yAxisTextFont)

            #rotate the image and draw the text
            self.graphImage['base'] = self.graphImage['base'].rotate(-90, expand = 1)
            self.graphImage['base'].save(path)
            self.graphImage['base'] = PIL.Image.open(path)
            self.graphImage['draw'] = PIL.ImageDraw.Draw(self.graphImage['base'])
            yAxisTextPosition = [int((self.graphImage['base'].size[0] - yAxisTextSize[0]) / 2), int((barGraphSidePadding - yAxisTextSize[1]) / 2)]
            self.graphImage['draw'].text(yAxisTextPosition, self.graphYTitle, yAxisTitleColor, font = yAxisTextFont)
            self.graphImage['base'].save(path)
            self.graphImage['base'] = PIL.Image.open(path)
            self.graphImage['base'] = self.graphImage['base'].rotate(90, expand = 1)
            self.graphImage['draw'] = PIL.ImageDraw.Draw(self.graphImage['base'])

            #calculate the size of the graph title
            graphTitleFont = PIL.ImageFont.truetype(self.fontPath, int(barGraphTopPadding / 3))
            graphTitleSize = self.graphImage['draw'].textsize(self.graphTitle, graphTitleFont)

            #draw the title text
            graphTitleTextPosition = [int((self.graphImage['base'].size[0] - graphTitleSize[0]) / 2), int((barGraphTopPadding - graphTitleSize[1]) / 2)]
            self.graphImage['draw'].text(graphTitleTextPosition, self.graphTitle, graphTitleColor, font = graphTitleFont)
        
        #calculate the data graphing info
        graphDataEntryWidth = int(barGraphSafeZoneBounds[1][0] - barGraphSafeZoneBounds[0][0])
        graphDataEntryHeight = int(barGraphSafeZoneBounds[1][1] - barGraphSafeZoneBounds[0][1])
        graphDataEntryPoints = len(self.graphData)
        self.graphData.reverse()
        colorStep = 0
        dataWidth = int(graphDataEntryWidth / graphDataEntryPoints)
        if (dataWidth > maxDataPlotSize):
            dataWidth = int(maxDataPlotSize)
        dataWidthHalf = int(dataWidth / 2)
        measures = []
        for each in self.graphData:
            measures.append(each[1])
        maxMeasure = max(measures)
        dataPositions = []

        #iterate through the data
        step = 0
        for plot in self.graphData:
            title = plot[0]
            measure = plot[1]
            currentGraphColor = self.colorSheetData['graphDataColors'][colorStep]
            xPosition = step * dataWidth
            height = int((measure / maxMeasure) * graphDataEntryHeight)

            #draw the rectangle
            self.graphImage['draw'].rectangle([
                int(barGraphSafeZoneBounds[0][0] + xPosition), int(barGraphSafeZoneBounds[1][1] - height), int(barGraphSafeZoneBounds[0][0] + xPosition + dataWidthHalf), int(barGraphSafeZoneBounds[1][1])
            ], fill = currentGraphColor, outline = currentGraphColor, width = 1)

            #save the position of the data [TITLE, X, Y, MEASURE]
            dataPositions.append([title, int(barGraphSafeZoneBounds[0][0] + xPosition + dataWidthHalf), int(barGraphSafeZoneBounds[1][1]), measure])

            #if the color step is greater than the data color length then reset it
            colorStep += 1
            if (colorStep >= len(self.colorSheetData['graphDataColors'])):
                colorStep = 0

            #increase the normal step
            step += 1
        
        #rotate the image sideways so that the text can be drawn for the plot titles
        self.graphImage['base'] = self.graphImage['base'].rotate(90, expand = 1)
        self.graphImage['base'].save(path)
        self.graphImage['base'] = PIL.Image.open(path)
        self.graphImage['draw'] = PIL.ImageDraw.Draw(self.graphImage['base'])

        #create a font for the bottom titles
        if (bottomTitleTextSize == None or bottomTitleTextSize < 0):
            bottomTitleTextSize = int(barGraphBottomPadding / 10)
        bottomTitleFont = PIL.ImageFont.truetype(self.fontPath, bottomTitleTextSize)

        #draw the title for each plot
        for index in dataPositions:
            position = [(index[2] + 5), self.graphImage['base'].size[1] - index[1]]
            self.graphImage['draw'].text(position, str(index[0]) + ' : ' + str(index[3]), self.colorSheetData['titleColors']['xAxis'], font = bottomTitleFont)

        #rotate the image back to normal so that it can be saved
        self.graphImage['base'] = self.graphImage['base'].rotate(-90, expand = 1)
        self.graphImage['base'].save(path)
        self.graphImage['base'] = PIL.Image.open(path)
        self.graphImage['draw'] = PIL.ImageDraw.Draw(self.graphImage['base'])

        #save the image
        self.graphImage['base'].save(path)

        #return the path to the image
        return path