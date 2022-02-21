# find how to not get an error on the paddleocr to debug better
from paddleocr import PaddleOCR,draw_ocr
import cv2
# import xlsxwriter
import os
import shutil
from tkinter import *
from tkinter import filedialog

##########################################################################

script_path = os.path.abspath(os.curdir)

##########################################################################

# creating main root
root = Tk()
root.geometry("350x150")
root.iconbitmap("C:/Users/chris/anaconda3/envs/docs38/anonymous.ico")
root.title("Text rocognition")

##########################################################################

# this function asks the user for the file location
def selectingFromFolder():
    # promts used for location where files are stored
    userPath = filedialog.askdirectory()
    global img_path
    global folder_path
    img_path = userPath
    folder_path = userPath


# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
def hide(im0, c1, c2):
    xmax = int(c2[0])
    xmin = int(c1[0])
    ymin = int(c1[1])
    ymax = int(c2[1])
    # cv2.rectangle(im0, (xmin, ymin),(xmax, ymax), (0, 0, 0), -1)
    im0[ymin:ymax, xmin:xmax] = [255, 255, 255] #replacing color
    return im0



# get names of files from a folder
# get all file names from img source location
img_list = os.listdir(img_path)

# this where the images are
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
img_path = 'WhatsApp_Image_2022-02-16_at_5.58.10_PM-1.jpeg'
result = ocr.ocr(img_path, cls=True)
res = []
for line in result:
    print(line)
    res.append([line[0][0], line[0][2]])
    
# draw result
from PIL import Image, ImageFont
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
# print(boxes[0][0][0])
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='arial.ttf')
# print(type(im_show))
im_show = Image.fromarray(im_show)
# print(type(im_show))
im_show.save('result.jpg')
im = Image.open(r"result.jpg")
im.show()


# print(res)
# print(len(res))
# Key of dictionary depending upon result.jpg
key = []
for i in range(len(res)):
    key.append(i+1)

# print(key)
#Dictiornary of bounding boxes from image
res_dict = dict(zip(key, res))
print(res_dict)
# number = take_input()
# print(number)
# um_box = number.split()
# print(num_box)
img = cv2.imread(img_path)

# removed this block
######################
# for numbers in num_box:
#    coordinates = res_dict[int(numbers)]
#    print(coordinates)
#    coord1 = coordinates[0]
#    coord2 = coordinates[1]
#    final_img = hide(img, coord1, coord2)

#cv2.imwrite("hided.jpg", final_img)




# create gui with Tkinter

##########################################################################
#creating GUI widgets
scriptDescript = Label(root, text="This script reads all images in a folder \n for barcodes and outputs them in a specified folder")
label_1 = Label(root, text="Folder: ", padx=10, pady=15)
folderSelect = Button(root, text="Select", width=10, borderwidth=3, command=selectingFromFolder)
runScript = Button(root, text="Run script", width=10, borderwidth=3, command=runMainScript)

scriptDescript.grid(row=0, column=0, columnspan=2)
label_1.grid(row=1, column=0)
folderSelect.grid(row=1, column=1)
runScript.grid(row=2, column=1)


##########################################################################
root.mainloop()

quit()

### A DECISION FOR SOMETING IS A DECISION AGAINST SOMETHING ELSE
### 4.669