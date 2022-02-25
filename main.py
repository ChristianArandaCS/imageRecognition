# python 3.7.5
# This script will extract information from images in selected folder
from paddleocr import PaddleOCR,draw_ocr
import cv2
import xlsxwriter
import os
import shutil
import glob
from pyzbar.pyzbar import decode
from tkinter import *
from tkinter import filedialog

##########################################################################

script_path = os.path.abspath(os.curdir)

# creating main root
root = Tk()
root.geometry("350x150")
root.iconbitmap(script_path,"/anonymous.ico")
root.title("Text rocognition")

##########################################################################


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


# this function asks the user for the file location
def selectingFromFolder():
    # promts used for location where files are stored
    global img_path
    global folder_path
    global img_list

    userPath = filedialog.askdirectory()
    img_path = userPath
    folder_path = userPath


#############################################################################
#############################################################################
def runMainScript():

    # need to run only once to download and load model into memory
    ocr = PaddleOCR(use_angle_cls=True, lang='en')

    #sets up excel file
    # generates output excel file
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()

    # headers values
    header1 = 'File name'
    header2 = 'Output file'

    # adds headers to the excel
    worksheet.write(0,0,header1)
    worksheet.write(0,1,header2)


    # removes the "thumbs.db" files
    img_list = os.listdir(img_path)
    img_list.remove("Thumbs.db")




    # copies a files from the img source to the script path
    for fname in img_list:
        shutil.copy2(os.path.join(img_path,fname),script_path)



    # sets where the script will start from
    row = 1
    col = 0

    #############################################################################
    #############################################################################

    # enters for loop to iterate through files and get all text fields
    # for filename in os.listdir(img_path):
    for filename in img_list:

        # writes img name into excel
        worksheet.write(row, col, filename)

        col = col +1

        # barcode decoder
        img = cv2.imread(filename)

        # writes the barcodes into excel
        for code in decode(img):
            # gets the detected files from the image
            detectedBarcodes = code.data.decode('utf-8')

            # adds information into an excel
            worksheet.write(row, col, detectedBarcodes)

        col = col + 1

        # 
        # for filename in img_list:
        #     # img_path = 'edited-1.jpg'
        result = ocr.ocr(filename, cls=True)
        res = []
        data_input = []


        # result holds all the information for the current image
        for line in result:
            itterable = 0

            print(line)
            col = 2
        
            res.append([line[0][0], line[0][2]])
            print(res)

            
            data_input.append(line[1][0])
            print(data_input)


        for items in data_input:

            worksheet.write(row, col, items)
            col = col + 1


        # # writes the information into excel
        # for data in data_input:
        #     worksheet.write(row, col, data)
            

        # sets and resets the rows and cols in excel
        row = row +1
        col = 0

    # finished adding barcodes to excel and closes excel    
    workbook.close()

    #############################################################################
    #############################################################################


    # # this where the images are
    # for img in img_list:
    #     # img_path = 'edited-1.jpg'
    #     result = ocr.ocr(img, cls=True)
    #     res = []
    #     # result holds the information from all images
    #     for line in result:
    #         print(line)
    #         row = 3
    #         col = 1
    #         worksheet.write(row, col, line)
    #         worksheet.write(row, col, line)
    #         res.append([line[0][0], line[0][2]])
    #         col = col + 1
    #     row = row +1


    # this is outisde the scope of the for loop
    ##########################################################################
    ##########################################################################
    ##########################################################################


    # # get info from printed list
    # # draw result
    # from PIL import Image, ImageFont
    # image = Image.open(img_path).convert('RGB')
    # boxes = [line[0] for line in result]
    # # print(boxes[0][0][0])
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores, font_path='arial.ttf')
    # # print(type(im_show))
    # im_show = Image.fromarray(im_show)
    # # print(type(im_show))
    # im_show.save('result.jpg')
    # im = Image.open(r"result.jpg")
    # im.show()


    # # print(res)
    # # print(len(res))
    # # Key of dictionary depending upon result.jpg
    # key = []
    # for i in range(len(res)):
    #     key.append(i+1)

    # # print(key)
    # #Dictiornary of bounding boxes from image
    # res_dict = dict(zip(key, res))
    # print(res_dict)
    # # number = take_input()
    # # print(number)
    # # um_box = number.split()
    # # print(num_box)
    # img = cv2.imread(img_path)


    # print(img_list)






# create gui with Tkinter

##########################################################################

#creating GUI widgets
scriptDescript = Label(root, text="This script reads all images in a folder \n for text and outputs them in a specified folder")
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
