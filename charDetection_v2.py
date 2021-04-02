#######################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                     #
#                Ömer Oğuz Çelikel                    #
#                    041801090                        #
#                                                     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#######################################################

"""
In this project, you will develop a program in Python to
the detect and count characters in an image
Instructor: Prof.Dr. Muhittin Gökmen
"""

from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import *
import numpy as np
import os   # os module can be used for file and directory operations
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk,Image

#Create GUI window
window = tk.Tk()
curr_dir = os.path.dirname(os.path.realpath(__file__))
#Some informations about this project will be save on that file
outputFile = open("outputFile.txt","w")

# MAIN FUNCTION OF THE PROGRAM
#-----------------------------------------------------------------------------------
# Main function where this python script starts execution

def main():
    window.title("CHARACTER DETECTION")
    window.geometry("600x300")
    Label(window,text="Please Select Your Image To Detect Characters").pack()

    # See example image in the homepage
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()
    img = ImageTk.PhotoImage(Image.open("ornek.jpg"))
    canvas.create_image(180, 40, anchor=NW,image=img)

    #To select our image
    B = tk.Button(window, text="Select a file", command=ButtonFunc).place(x = 50,y = 65)
    window.mainloop()

#That Button Function is gets the image file which are jpg png format
def ButtonFunc():
    # Opening Filedialog
    window.filename = filedialog.askopenfilename(initialdir="/",
                                                 title="Select file",
                                                 filetypes=(("jpeg files", "*.jpg"),("png files", "*.png"),("all files", "*.*")))

    img_file = window.filename
    print(img_file)
    openNewWindow(img_file)
    outputFile.write("\n Input File name: "+ img_file)

#Taht Button does everything. Takes the image and starts to find chars
def ButtonFunc2():
    img_gray = img_color.convert('L')
    # img_gray.show() # display the grayscale image
    # create a binary image by thresholding the grayscale image
    # --------------------------------------------------------------------------------
    # convert the grayscale PIL Image to a numpy array
    arr_gray = np.asarray(img_gray)
    # values below the threshold are considered as ONE and values above the threshold
    # are considered as ZERO (assuming that the image has dark objects (e.g., letters
    # ABC or digits 123) on a light background)
    THRESH, ZERO, ONE = 155, 0, 255
    # the threshold function defined below returns the binary image as a numpy array
    arr_bin = threshold(arr_gray, THRESH, ONE, ZERO)

    # convert the numpy array of the binary image to a PIL Image
    img_bin = Image.fromarray(arr_bin)

    # component (object) labeling based on 4-connected components
    # --------------------------------------------------------------------------------
    # blob_coloring_4_connected function returns a numpy array that contains labels
    # for the pixels in the input image, the number of different labels and the numpy
    # array of the image with colored blobs
    arr_labeled_img, num_labels, arr_blobs = blob_coloring_8_connected(arr_bin, ONE)

    # print the number of objects as the number of different labels
    print("There are " + str(num_labels) + " objects in the input image.")

    # convert the numpy array of the colored components (blobs) to a PIL Image
    img_blobs = Image.fromarray(arr_blobs)

    #keeps labels coordinates of all characters
    labels_Coordinates = labelCoord(arr_blobs)
    coordinates = where_Rectangle(arr_blobs, labels_Coordinates)

    #draws rectange to around image
    rect_Draw(img_color, coordinates)

    allChars = []  # keeps my chars in an list

    countA = 0
    countB = 0
    countC = 0
    coordinatesOfA= []
    coordinatesOfB= []
    coordinatesOfC= []
    for i in range(num_labels):
        # finding boundry and extended minimum bounding rectangle for 3 pixels
        min_x = coordinates[0][i] - 3
        max_x = coordinates[2][i] + 3
        min_y = coordinates[1][i] - 3
        max_y = coordinates[3][i] + 3
        cropedImage = crop_Image(img_bin, min_x, max_x, min_y, max_y)  # cropes letters

        cropedImage_gray = cropedImage.convert('L')
        cropedImage_gray_np = np.asarray(cropedImage_gray)

        #Change background instead of the first one. With that it can find holes in the characters.
        myChar = holes8Connected(cropedImage_gray_np)
        allChars.append(myChar)  # keeps my chars in an list

        #checking which characters they are and add their own lists.
        if myChar == "A" :
            countA += 1
            coordinatesOfA.append([min_x, max_x, min_y, max_y])
        elif myChar == "B":
            countB += 1
            coordinatesOfB.append([min_x, max_x, min_y, max_y])
        elif myChar == "C":
            countC += 1
            coordinatesOfC.append([min_x, max_x, min_y, max_y])

        lastPhoto = drawText(allChars, min_x, min_y, i, img_color)


    lastPhoto.show()
    #save photo to our directory
    lastPhoto.save('Output.jpg')
    print("There are ", countA, "A in that image")
    print("There are ", countB, "B in that image")
    print("There are ", countC, "C in that image")
    # Write required informations to the txt file
    outputFile.write("\n Count of each detected character: ")
    outputFile.write("\n A:"+ str(countA)+"   B :"+ str(countB)+"  C:"+ str(countC))
    outputFile.write("\n Bounding Boxes for each detected character: ")
    outputFile.write("\n A: "+str(countA) +"\n " + str(coordinatesOfA))
    outputFile.write("\n B "+ str(countB) + "\n " +str(coordinatesOfB))
    outputFile.write("\n C: "+ str(countC)+ "\n"+str(coordinatesOfC))

    outputFile.close()

# function to open a new window
# on a button click
def openNewWindow(img_file):
    global img_color
    newWindow = tk.Toplevel()
    newWindow.title("New Window")
    #newWindow.geometry("widthxheight")
    newWindow.geometry("500x500")
    img_color = Image.open(img_file)
    width, height = img_color.size
    if width > 500 and height > 500:
        messagebox.showinfo("Warning","Image file is too big to show, but it will work")
    render = ImageTk.PhotoImage(img_color)
    img = Label(newWindow,image=render)
    img.image = render
    img.place(x = 80 ,y = 20)
    B2 = tk.Button(newWindow, text="Start", command=ButtonFunc2).place(x = 20 ,y = 20)
    # B2.pack()

""" Image Pregresss Part """

# Draw letter to right labels
def drawText(allChars,min_x, min_y,i,img):
   text = allChars[i]
   fnt = ImageFont.truetype("/arial.ttf", 20)
   draw1 = ImageDraw.Draw(img)
   draw1.text((min_y,min_x), text=text, font=fnt, fill=(255, 128, 0))
   return img

# Checks holes with 8-connectlabeling
def holes8Connected(cropedImage_gray_np):
   THRESH, ZERO, ONE = 155, 0, 1
   # the threshold function defined below returns the binary image as a numpy array
   #Put ZERO instead of ONE, bacground will be 1 not zero.
   arr_labeled_img, holes, arr_blobs = blob_coloring_8_connected(cropedImage_gray_np, ZERO)

   if holes - 1 == 1:
      return "A"
   elif holes - 1 == 2:
      return "B"
   elif holes - 1 == 0:
      return "C"

#Finds labels coordinates
def labelCoord(img_color):
   row = img_color.shape[0]
   column = img_color.shape[1]

   labels_Coordinates = {}
   for i in range(row):
      for j in range(column):
         if img_color[i][j][0] != 0 and img_color[i][j][1] != 0 and img_color[i][j][2] != 0:
            labels_Coordinates[rgb_to_hash(img_color[i][j])] = [i, j]
   labels_Coordinates = labelCoord2(labels_Coordinates)
   return labels_Coordinates

#Finds labels coordinates helps
def labelCoord2(labelsCoordinates):
   label_dict2 = {}
   num_labels = 0
   for i in labelsCoordinates:
      label_dict2[i] = num_labels
      num_labels += 1

   return label_dict2

# RGB values created
def rgb_to_hash(rgb_array):
   r = rgb_array[0] * 1000000
   g = rgb_array[1] * 1000
   b = rgb_array[2]
   return r + g + b

#Finds rectangle coordinates
def where_Rectangle(img_color, labelsCoordinates):
    num_labels = len(labelsCoordinates)
    coordinates = np.zeros(shape=(4, num_labels))
    row = img_color.shape[0]
    column = img_color.shape[1]
    for t in range(num_labels):
        coordinates[0][t] = 10000 #max
        coordinates[1][t] = 10000 #max
    for i in range(row):
        for j in range(column):
            if img_color[i][j][0] != 0 and img_color[i][j][1] != 0 and img_color[i][j][2] != 0:
                current = rgb_to_hash(img_color[i][j])
                currentIndex = labelsCoordinates[current]

                # Min i
                if (i < coordinates[0][currentIndex]):
                    coordinates[0][currentIndex] = i
                # Min j
                if j < coordinates[1][currentIndex]:
                    coordinates[1][currentIndex] = j
                # Max i
                if i > coordinates[2][currentIndex]:
                    coordinates[2][currentIndex] = i
                # Max j
                if j > coordinates[3][currentIndex]:
                    coordinates[3][currentIndex] = j

    #print("\ncoordinates",coordinates)
    return coordinates

#Draws rectangle above letter
def rect_Draw(image, coordinates):
   column = coordinates.shape[1]
   for j in range(column):
      shape = [( coordinates[3][j], coordinates[0][j]), (coordinates[1][j] , coordinates[2][j])]
      #rectangle image
      drawedRectangle = ImageDraw.Draw(image)
      drawedRectangle.rectangle(shape, fill= None, outline="red", width=1)

#Crops Images
def crop_Image(img_bin , min_x , max_x , min_y , max_y):
   croppedImage = img_bin.crop( (min_y, min_x, max_y, max_x))
   return croppedImage

# BINARIZATION
#-----------------------------------------------------------------------------------
# Function for creating and returning a binary image as a numpy array by thresholding
# the given array of the grayscale image
def threshold(arr_gray_in, T, LOW, HIGH):
   # get the numbers of rows and columns in the array of the grayscale image
   n_rows, n_cols = arr_gray_in.shape
   # initialize the output (binary) array by using the same size as the input array
   # and filling with zeros
   arr_bin_out = np.zeros(shape = arr_gray_in.shape)
   # for each value in the given array of the grayscale image
   for i in range(n_rows):
      for j in range(n_cols):
         # if the value is smaller than the given threshold T
         if abs(arr_gray_in[i][j]) < T:
            # the corresponding value in the output (binary) array becomes LOW
            arr_bin_out[i][j] = LOW
         # if the value is greter than or equal to the given threshold T
         else:
            # the corresponding value in the output (binary) array becomes HIGH
            arr_bin_out[i][j] = HIGH
   # return the resulting output (binary) array
   return arr_bin_out

# CONNECTED COMPONENT LABELING AND BLOB COLORING
#-----------------------------------------------------------------------------------
# Function for labeling objects as 4-connected components in a binary image whose
# numpy array is given as an input argument and creating an image with randomly
# colored components (blobs)
def blob_coloring_8_connected(arr_bin, ONE):
   # get the numbers of rows and columns in the array of the binary image
   n_rows, n_cols = arr_bin.shape
   # max possible label value is set as 10000
   max_label = 10000
   # initially all the pixels in the image are labeled as max_label
   arr_labeled_img = np.zeros(shape = (n_rows, n_cols), dtype = int)
   for i in range(n_rows):
      for j in range(n_cols):
         arr_labeled_img[i][j] = max_label
   # keep track of equivalent labels in an array
   # initially this array contains values from 0 to max_label - 1
   equivalent_labels = np.arange(max_label, dtype = int)
   # labeling starts with k = 1
   k = 1
   # first pass to assign initial labels and update equivalent labels from conflicts
   # for each pixel in the binary image
   #--------------------------------------------------------------------------------
   for i in range(1, n_rows - 1):
      for j in range(1, n_cols - 1):
         c = arr_bin[i][j] # value of the current (center) pixel

         l = arr_bin[i - 1][j] # value of the left pixel
         u = arr_bin[i][j - 1] # value of the upper pixel
         """8 Connect """
         d = arr_bin[i - 1][j - 1]  # value of the upper left pixel
         r = arr_bin[i + 1][j - 1] # value of the upper right pixel

         label_l = arr_labeled_img[i - 1][j]  # label of the left pixel
         label_u = arr_labeled_img[i][j - 1]  # label of the upper pixel
         label_d = arr_labeled_img[i - 1][j - 1]  # label of the upper left pixel
         label_r = arr_labeled_img[i + 1][j - 1]  # label of the upper right pixel

         """-----------"""

         # only the non-background pixels are labeled
         if c == ONE:
            # get the minimum of the labels of the upper and left pixels
            min_label = min(label_u, label_l, label_d, label_r)
            # if both upper and left pixels are background pixels
            if min_label == max_label:
               # label the current (center) pixel with k and increase k by 1
               arr_labeled_img[i][j] = k
               k += 1
               #print("k: = ", k)
            # if at least one of upper and left pixels is not a background pixel
            else:
               # label the current (center) pixel with min_label
               arr_labeled_img[i][j] = min_label
               # if upper pixel has a bigger label and it is not a background pixel
               if min_label != label_u and label_u != max_label:
                  # update the array of equivalent labels for label_u
                  update_array(equivalent_labels, min_label, label_u)
               # if left pixel has a bigger label and it is not a background pixel
               if min_label != label_l and label_l != max_label:
                  # update the array of equivalent labels for label_l
                  update_array(equivalent_labels, min_label, label_l)

               """Set the Min Labels"""
               if min_label != label_r and label_r != max_label:
                  # update the array of equivalent labels for label_l
                  update_array(equivalent_labels, min_label, label_r)
               if min_label != label_d and label_d != max_label:
                  # update the array of equivalent labels for label_l
                  update_array(equivalent_labels, min_label, label_d)
               """------------------"""

   # final reduction in the array of equivalent labels to obtain the min. equivalent
   # label for each used label (values from 1 to k - 1) in the first pass of labeling
   #--------------------------------------------------------------------------------
   for i in range(1, k):
      index = i
      while equivalent_labels[index] != index:
         index = equivalent_labels[index]
      equivalent_labels[i] = equivalent_labels[index]
   # rearrange equivalent labels so they all have consecutive values starting from 1
   # using the rearrange_array function which also returns the number of different
   # values of the labels used to label the image
   num_different_labels = rearrange_array(equivalent_labels, k)
   # create a color map for randomly coloring connected components (blobs)
   #--------------------------------------------------------------------------------
   color_map = np.zeros(shape = (k, 3), dtype = np.uint8)
   np.random.seed(0)
   for i in range(k):
      color_map[i][0] = np.random.randint(0, 255, 1, dtype = np.uint8)
      color_map[i][1] = np.random.randint(0, 255, 1, dtype = np.uint8)
      color_map[i][2] = np.random.randint(0, 255, 1, dtype = np.uint8)
   # create an array for the image to store randomly colored blobs
   arr_color_img = np.zeros(shape = (n_rows, n_cols, 3), dtype = np.uint8)
   # second pass to resolve labels by assigning the minimum equivalent label for each
   # label in arr_labeled_img and color connected components (blobs) randomly
   #--------------------------------------------------------------------------------
   for i in range(n_rows):
      for j in range(n_cols):
         # only the non-background pixels are taken into account and the pixels
         # on the boundaries of the image are always labeled as 0
         if arr_bin[i][j] == ONE and arr_labeled_img[i][j] != max_label:
            arr_labeled_img[i][j] = equivalent_labels[arr_labeled_img[i][j]]
            arr_color_img[i][j][0] = color_map[arr_labeled_img[i][j], 0]
            arr_color_img[i][j][1] = color_map[arr_labeled_img[i][j], 1]
            arr_color_img[i][j][2] = color_map[arr_labeled_img[i][j], 2]
         # change the label values of background pixels from max_label to 0
         else:
            arr_labeled_img[i][j] = 0
   # return the labeled image as a numpy array, number of different labels and the
   # image with colored blobs (components) as a numpy array
   return arr_labeled_img, num_different_labels, arr_color_img

# Function for updating the equivalent labels array by merging label1 and label2
# that are determined to be equivalent
def update_array(equ_labels, label1, label2) :
   # determine the small and large labels between label1 and label2
   if label1 < label2:
      lab_small = label1
      lab_large = label2
   else:
      lab_small = label2
      lab_large = label1
   # starting index is the large label
   index = lab_large
   # using an infinite while loop
   while True:
      # update the label of the currently indexed array element with lab_small when
      # it is bigger than lab_small
      if equ_labels[index] > lab_small:
         lab_large = equ_labels[index]
         equ_labels[index] = lab_small
         # continue the update operation from the newly encountered lab_large
         index = lab_large
      # update lab_small when a smaller label value is encountered
      elif equ_labels[index] < lab_small:
         lab_large = lab_small # lab_small becomes the new lab_large
         lab_small = equ_labels[index] # smaller value becomes the new lab_small
         # continue the update operation from the new value of lab_large
         index = lab_large
      # end the loop when the currently indexed array element is equal to lab_small
      else: # equ_labels[index] == lab_small
         break

# Function for rearranging min equivalent labels so they all have consecutive values
# starting from 1
def rearrange_array(equ_labels, final_k_value):
   # find different values of equivalent labels and sort them in increasing order
   different_labels = set(equ_labels[1:final_k_value])
   different_labels_sorted = sorted(different_labels)
   # compute the number of different values of the labels used to label the image
   num_different_labels = len(different_labels)
   # create an array for storing new (consecutive) values for equivalent labels
   new_labels = np.zeros(final_k_value, dtype = int)
   count = 1 # first label value to assign
   # for each different label value (sorted in increasing order)
   for l in different_labels_sorted:
      # determine the new label
      new_labels[l] = count
      count += 1 # increase count by 1 so that new label values are consecutive
   # assign new values of each equivalent label
   for ind in range(1, final_k_value):
      old_label = equ_labels[ind]
      new_label = new_labels[old_label]
      equ_labels[ind] = new_label
   # return the number of different values of the labels used to label the image
   return num_different_labels

if __name__ == '__main__':
    main()

