import sys
import os 
import glob
from utils import *

# ============================================================================
#------PARAM--------#
## Check this parameter before build!!!
SCALE_PERCENT = 10 ### size of image need to be reduced 

folderdir = "D:\\Personal_project\\image_test\\train_new_label_UNIMIB"
sampledir = "D:\\Personal_project\\image_test\\train_new_label_UNIMIB\\images"
imgoutputdir = "D:\\Personal_project\\image_test\\train_new_label_UNIMIB\\output"
txtoutputdir = "D:\\Personal_project\\image_test\\train_new_label_UNIMIB\\txt_output"

json_file_name  = 'new_annotation_UNIMIB_train.json' 
img_sample_name = '20151127_114556.jpg'

# ============================================================================
##Check the first image sample to obtain width, height
MAX_NUM_POLY_POINT = 100
# full_images = cv2.imread("D:\\Personal_project\\image_test\\train_new_label_UNIMIB\\images\\20151221_132555.jpg",-1)
full_images = cv2.imread((os.path.join(sampledir,img_sample_name)),-1)
height, width, _ = full_images.shape
w, h = width,height ;
HEIGHT = height
WIDTH = width

# ===============================================================================

##
with open(os.path.join(folderdir,json_file_name)) as json_file:
	data = json.load(json_file)
	image_id = getFromDict(data,["_via_image_id_list"])

	for i in range(len(image_id)):
		image_name = image_id[i] 
		print(image_id[i])
		regions = getFromDict(data,["_via_img_metadata",image_name,"regions"])

		shape_name = [0] * len(regions)
		num_poly = 0
		num_rect = 0

		for i in range(len(regions)):
			shape_name[i]= getFromDict(regions[i],["shape_attributes","name"])
			if shape_name[i] == "rect":
				num_rect+=1
			else:
				num_poly+=1

		rect = [Rectangle() for i in range(num_rect)]
		food_type = [0] * num_rect
		num_poly_point = [0] * num_poly
		rect_count = 0
		food_type_count = 0
		num_poly_point_count = 0
		for i in range(len(shape_name)):
			if shape_name[i] == "rect":
				rect[rect_count].x = getFromDict(regions[i],["shape_attributes","x"]) 
				rect[rect_count].y = getFromDict(regions[i],["shape_attributes","y"])
				rect[rect_count].width = getFromDict(regions[i],["shape_attributes","width"])
				rect[rect_count].height = getFromDict(regions[i],["shape_attributes","height"])
				rect_count +=1 
				food_type[food_type_count] = getFromDict(regions[i],["region_attributes","food_type"])
				food_type_count +=1
				# print(food_type[food_type_count-1])
			elif shape_name[i] == "polygon":
				num_poly_point[num_poly_point_count] = len(getFromDict(regions[i],["shape_attributes","all_points_x"]))
				num_poly_point_count +=1		
		poly_point = [Point(0,0) for i in range(MAX_NUM_POLY_POINT)]  

		# print(num_poly_point[1])
		i=0;k=0	
		polies = []	
		point_count = 0
		order_poly_count = 0 
		# print(shape_same)
		for i in range(len(shape_name)):
			a_poly = []
			# print(i)
			if shape_name[i] == "rect":
				continue 
			elif shape_name[i] == "polygon":
				for k in range(num_poly_point[order_poly_count]):
					poly_point[point_count].x = int(getFromDict(regions[i],["shape_attributes","all_points_x"])[k])
					poly_point[point_count].y = int(getFromDict(regions[i],["shape_attributes","all_points_y"])[k])
					a_poly.append(poly_point[point_count]);
					point_count+=1					
				polies.append(list(a_poly)) 
				a_poly.clear()
				order_poly_count+=1
		poly_point.clear()

		new_image = np.zeros((HEIGHT,WIDTH,3),np.uint8)

		i = 0;
		for i in range(len(rect)):

			new_image = cv2.rectangle(new_image,(rect[i].x,rect[i].y),(rect[i].x+rect[i].width,rect[i].y+rect[i].height),selectFoodColor(food_type[i]),-1)
			

		i = 0; 
		pd = [PolygonDrawer("Polygon") for i in range(num_poly) ]

		i = 0;j = 0;
		for i in range(len(polies)):
			for j in range(len(polies[i])):
				pd[i].input_points(polies[i][j].x,polies[i][j].y)
		for i in range(len(polies)):
			new_image = pd[i].run(new_image)

		## save output into jpg
		file_name = "output_%s.jpg" % image_name
		cv2.imwrite(os.path.join(imgoutputdir,file_name),new_image)

		## save output into txt 

		width = int(new_image.shape[1] * SCALE_PERCENT / 100)
		height = int(new_image.shape[0] * SCALE_PERCENT / 100)
		dim = (width, height)

		resized_image = cv2.resize(new_image, dim, interpolation = cv2.INTER_AREA)
		gray_resized_image = cv2.cvtColor(resized_image,cv2.COLOR_BGR2GRAY)

		txt_file_name = "output_%s.txt" % image_name
		# np.savetxt(os.path.join(txtoutputdir,txt_file_name),gray_resized_image, fmt='%u',delimiter =' ')
		np.savetxt(os.path.join(txtoutputdir,txt_file_name),gray_resized_image, fmt='%u')

print("Task successful!")
