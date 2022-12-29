# Finger Counter with MediaPipe and OpenCV
 
![Finger Couter Gif](./finger_counter.gif)

## Introduction

This is a study project I developed to implement my former [Hand Tracking Project](https://github.com/lucasmirachi/hand-tracking) in a more useful application. That's why I, with the guidance of this [informative video](https://www.youtube.com/watch?v=01sAkU_NvOY) created by [Murtaza Hassan](https://www.youtube.com/channel/UCYUjYU5FveRAscQ8V21w81A), implemented it in a program where it is possible identify and count the number of finger that the user has lifted on a live image.

## Development 

For this code, it was utilized the [MediaPipe](https://google.github.io/mediapipe/) framework. MediaPipe is a framework developed by Google that contains some amazing models that allows us to quickly get started with some fundamental AI problems such as Face Detection, Object Detection, Hair Segmentation and much more!

Having said that, the model I'll be working with for this project is going to be the [Hand Tracking](https://google.github.io/mediapipe/solutions/hands). Basically, it combines two main modules: the Palm Detection Model and the Hand Landmark Model.

As the name suggests, the **Palm Detection Model** will detect the user's hands and provides a cropped image of the hand. From there, the **Hand Landmark Model** can find up to 21 different landmarks on this cropped image of the hand (like the image bellow):

![Hand Landmarks](https://mediapipe.dev/images/mobile/hand_landmarks.png)
[Source](https://google.github.io/mediapipe/solutions/hands)

For this project, in order to identify whether a finger is "up" or not, it was made a comparison between each finger's landmarks. If the finger's tip (using as example the index finger, where the tip's ID = 8) is above a landmark 2 units bellow (ID = 6), it means that the finger is lifted. Similarly if it's tip is bellow, it means that that finger is down!

```
#4 FINGERS
for id in range(1,5):
	if landmarksList[tipIds[id]][2] < landmarksList[tipIds[id]-2][2]:
		fingers.append(1)
	else:
		fingers.append(0)

```

It is also important to notice that this rule cannot be applied for the thumb, once the user can find a lot o difficulty to put the thumb's tip down. That's why, for this special case, it was consider that, when comparing the tip (ID = 4) to one landmark unit bellow (ID=3), if the thumb's tip is to the left of it, it means that the finger is up. At the same way, if the landmark is to the right of it, it means that the finger is down!

```
#THUMB
if landmarksList[tipIds[0]][1] > landmarksList[tipIds[0]-1][1]:
	fingers.append(1)
else:
	fingers.append(0)
```
 
---

## Files

<mark>HandTrackingModule.py</mark> contains the code that is required to run the Hand Tracking program.

<mark>GestureVolumeControl.py</mark> contains the code to count the fingers in real time. Obs: note that when capturing the webcam's image, I changed the standard "cap = cv2.VideoCapture(0)" to "cap = cv2.VideoCapture(2)", because I was utilizing another camera.