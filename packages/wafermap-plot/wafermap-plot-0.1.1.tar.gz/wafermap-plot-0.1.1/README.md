The klarf-reader library is a python 3 lib that allow to parse and get klarf content as dataclass.

## Installing WaferMapPlot

To install wafermap-plot, if you already have Python, you can install with:

```
pip install wafermap-plot
```

## How to import WaferMapPlot

To access wafermap-plot ansd its functions import it in yout Python code like this:

```
from wafermap_plot.wafermap_plot import WaferMapPlot
```

## Reading the example code

To reader a plot a wafermap you just have to supply a list of defect points.

```
plot = WaferMapPlot.plot(defect_points=defect_points)
plot.show()
```
