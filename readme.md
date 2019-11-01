
# pygraph - A graph rendering module for python

  

 This isnt a professional project, I just made it because I got tired of making graphs manually, so I figured I could automate that, so its more of a *me* thing.

## Usage:
### Making bar graphs:

#### To create a graph, import pygraph and create a graph using the ***pygraph.graphics.createBlankBarGraph*** function. The arguments are listed here:

```graph = pygraph.graphics.createBlankBarGraph(graphColorSheetPath, fontPath, width, height)```

`graphColorSheetPath [STRING] (The path to the PYGCS file for this graph, if you dont know what this is, then see the readme inside the pygraph directory.)`

`fontPath [STRING] (The path to the truetype font file that will be used for drawing text to the graph - This must be a .ttf file, the program does not accept any others. Support for others will be coming soon.)`

`width [INTEGER] (The width of the rendered image.)`

`height [INTEGER] (The height of the rendered image.)`

#### To add values to the graph, use the ***graph.addValue*** function. The arguments are listed here:

```graph.addValue(valueTitle, valueMeasure)```

`valueTitle [STRING] (The title of the individual bar on the graph.)`

`valueMeasure [INTEGER] (The measure of the individual bar on the graph.)`

#### To edit the title of the whole graph, you can do:

```graph.graphTitle = "Graph Title"```

#### To edit the title of the Y axis, you can do:

```graph.graphYTitle = "Graph Y Axis Title"```

#### To save the graph, use the ***graph.save*** function. The arguments are listed here:

```graph.save(path)```

`path [STRING] (The path where you want to save the final result of the graph. The file extension must be a normal image format, like png, jpg, jpeg, gif, etc...)`

## Example code:

```
#import pygraph

import pygraph

  

#create a graph using the grayscale color sheet and the roboto medium font

graph = pygraph.graphics.createBlankBarGraph('./pygraph/grayscale.pygcs', './roboto-medium.ttf', 4000, 1500)

  

#add the values

graph.addValue('Day 1', 5)

graph.addValue('Day 2', 23)

graph.addValue('Day 3', 14)

graph.addValue('Day 4', 18)

graph.addValue('Day 5', 19)

graph.addValue('Day 6', 28)

graph.addValue('Day 7', 3)

  

#edit the titles

graph.graphTitle =  'Workers Joining Over First Week'

graph.graphYTitle =  'Workers'

  

#save the graph

graph.save('employment-graph.png')
```

## Example chart:

![](https://i.imgur.com/yW6DVOA.png?raw=true)
