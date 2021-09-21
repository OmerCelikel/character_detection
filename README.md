# character_detection
 
In this Project, the letters in the image given by handwriting are perceived. The image is assumed to be a series of codes. After the necessary methods are applied, the image is converted into binary format. In this way, the background and the letters are separated. With the hole detection in the letters, it is understood that the letter is A, B, or C.

## Reading Image

The Tkinter page opens with the Main method. UML file can be tracked (Figure 1)
First of all, the required Image will be selected.

<img width="666" alt="Screen Shot 2021-09-21 at 08 18 11" src="https://user-images.githubusercontent.com/44753206/134115424-0ed6ec47-a7a5-4cb2-87a4-722379ae933e.png">


For this, a GUI has been created with Tkinter (Figure 2). File selection is performed with the "Select File" button on the page opened by opening Tkinter. After the photo is selected, a new window (Figure 3) opens and the "Start" button is clicked to start the process.
<img width="411" alt="Screen Shot 2021-09-21 at 08 19 26" src="https://user-images.githubusercontent.com/44753206/134115612-2ec053dd-3294-4612-b994-046c9a23fa59.png">



### Character Detection

Using 8-connected labeling gives information about labels. With that, labels can detect and count. Every character seems in a different value which starts 1. After labeling the letters, I found their location (min x, min y, max x max y). Then I drew these positions using a loop for each label. Then I cropped these photos one by one. I enlarged the rectangle I drew by 3 pixels. The purpose of this will now be the background letter. I used ONE of the labels in my first transaction. However, this time I used binaries that are ZERO. In this way, new labels have now given me holes. By subtracting 1 of these, I saw that A had 1 hole, B had 2 holes and C had no holes.


## Test Results


Results in png and txt files (Figure 4).

<img width="204" alt="Screen Shot 2021-09-21 at 08 17 30" src="https://user-images.githubusercontent.com/44753206/134115322-af3585fb-98ed-426e-9721-42ea7e1647a5.png">

<img width="708" alt="Screen Shot 2021-09-21 at 08 21 03" src="https://user-images.githubusercontent.com/44753206/134115639-d45539c4-a86f-4f98-b9ff-16bc694818f9.png">


