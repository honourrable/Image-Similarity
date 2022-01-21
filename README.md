# Image-Similarity

There are different methods to measure how similar two images are. In this project, the goal was creating a program to find most similar images in a test dataset. The steps of
the program are:

- Data reading and preparation
- Calculating R, G, B histograms of images (RGB colour space)
- Calculating Hue histogram of images (HSV colour space)
- Measurement of Euclidean distance between images' histograms
- Sorting the distances and getting the most similar ones

### Input & Output and Some Details

In dataset, some grayscale images were not suitable to perform the task. Therefore they were skipped but there could be another solution which is converting grayscale to RGB
by simply repeating the first channel values to second and third channels (dimensions). The relevant condition code block was shown below.

![grayscale_to_rgb](https://user-images.githubusercontent.com/57035819/150499567-3fd45993-e2a3-47cd-9c15-0ec45dc96ef4.png)

The inputs from user and program output were shown below to demonstrate how the background process perform and what it finds.

![input](https://user-images.githubusercontent.com/57035819/150499888-4df1111a-876a-4ef6-94bb-bbb0da229bb5.png)

![output](https://user-images.githubusercontent.com/57035819/150499913-62b11852-24c5-48c0-b774-bfc5b5706adf.png)
