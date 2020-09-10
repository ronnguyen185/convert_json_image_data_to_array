import numpy as np
import cv2
import json
from functools import reduce
from PIL import Image
import operator


POLY_FILLED_COLOR = (255,128,0)

FOOD_COLOR = [(255,255,255), ##default color
			(51,153,255),(102,225,255), (153, 153, 255), (102,255,178),(0,128,255),
			(0,255,255),(255,255,0),(0,102,0),(153,0,76),
			(0,153,76),(0,153,153),(128,128,128)]

food_name = ['pasta_sugo_pesce','scaloppine','patate/pure_prosciutto','pasta_sugo_vegetariano','carote',
			'salmone_(da_menu_sembra_spada_in_realta)','polpette_di_carne','zucchine_umido','pizza',
			'insalata_mista','torta_salata_3','cavolfiore']

# ============================================================================
class PolygonDrawer(object):
    def __init__(self, window_name):
        self.window_name = window_name # Name for our window

        self.done = False # Flag signalling we're done
        self.current = (0, 0) # Current position, so we can draw the line-in-progress
        self.points = [] # List of points defining our polygon

    def input_points(self, x, y):
        self.current = (x, y)
        # print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
        self.points.append((x, y))
        self.done = True


    def run(self,my_frame):
        # Let's create our working window and set a mouse callback to handle events
        cv2.namedWindow(self.window_name, flags=cv2.WINDOW_AUTOSIZE)
        self.my_frame = my_frame
        while(not self.done):
            if (len(self.points) > 0):
                # Draw all the current polygon segments
                cv2.polylines(self.my_frame, np.array([self.points]), False, POLY_FILLED_COLOR, 1)

        # of a filled polygon
        if (len(self.points) > 0):
            cv2.fillPoly(self.my_frame, np.array([self.points]), POLY_FILLED_COLOR)
        return self.my_frame

# ============================================================================

class Rectangle:
	def __init(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __repr__(self):
	    return "(" + str(self.x) + "," + str(self.y) + ")"

class Polygon:
	def __init__(self, *args):
		self.points = args
	def __repr__(self):
		return 'Polygon(' + ', '.join(map(lambda p: str(p), self.points)) + ')'

#============================================================================
def getFromDict(dataDict, mapList):
	return reduce(operator.getitem,mapList, dataDict)

def setInDict(dataDict, mapList, value):
	getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

def selectFoodColor(food_name):
	return {
		'pasta_sugo_pesce' : FOOD_COLOR[1],
		'scaloppine' : FOOD_COLOR[2],
		'patate/pure_prosciutto' : FOOD_COLOR[3],
		'pasta_sugo_vegetariano' : FOOD_COLOR[4],
		'carote' : FOOD_COLOR[5],
		'da_menu_sembra_spada_in_realta' : FOOD_COLOR[6],
		'polpette_di_carne' : FOOD_COLOR[7],
		'zucchine_umido' : FOOD_COLOR[8],
		'pizza' : FOOD_COLOR[9],
		'insalata_mista' : FOOD_COLOR[10],
		'torta_salata_3' : FOOD_COLOR[11],
		'cavolfiore' : FOOD_COLOR[12],
	}.get(food_name,FOOD_COLOR[0])

def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
    img.save( outfilename )