# Audiosurf 2 Bot

Audiosurf 2 image detection bot using LBP classifier.


## Cascade Classifier Docs
- [Cascade Classifier](https://docs.opencv.org/4.5.1/db/d28/tutorial_cascade_classifier.html)
- [Cascade Training](https://docs.opencv.org/4.5.1/dc/d88/tutorial_traincascade.html)
- [OpenCV on Windows](https://docs.opencv.org/3.4.13/d3/d52/tutorial_windows_install.html)
- [Tutorial](http://note.sonots.com/SciSoftware/haartraining.html)

## Training Data

### Raw Images

Game screenshots with 600x500 dimension.

### Positive Samples

900+ samples extracted from 300 game screenshots using Annotation Tool.

### Negative Samples

The same images as positive samples but with blocks or spikes hidden.

## Terminal Commands

In [OpenCV v3.4.13](https://sourceforge.net/projects/opencvlibrary/files/3.4.13/), the executables are found in `opencv/build/x64/vc15/bin`. Append the commands to the file path in the terminal.

Read **Cascade Training** for information about command arguments.

### Annotation Tool

```shell
opencv_annotation.exe --annotations=pos_block.txt --images=positive_block/
opencv_annotation.exe --annotations=pos_spike.txt --images=positive_spike/
```

The program opens all images inside the positive directory. You can draw rectangles with the mouse around the positive samples you want to train with.

**Annotation shortcuts:**
- 'c' - accept selection
- 'd' - delete last selection
- 'n' - next image
- 'esc' - exit


### Create Positive Samples

```shell
opencv_createsamples.exe -info pos_block.txt -w 24 -h 24 -num 900 -vec pos_block.vec
opencv_createsamples.exe -info pos_spike.txt -w 24 -h 24 -num 900 -vec pos_spike.vec
```

Change `-num` argument as needed for a different value of positive samples.

### Train Cascade

```shell
opencv_traincascade.exe -data cascade_block/ -vec pos_block.vec -bg neg_block.txt -numPos 800 -numNeg 350 -numStages 25 -w 24 -h 24
opencv_traincascade.exe -data cascade_spike/ -vec pos_spike.vec -bg neg.txt -numPos 250 -numNeg 200 -numStages 20 -w 24 -h 24
```

Width and height dimensions need to be the same as the positive samples.

Use `-precalcValBufSize` and `-precalcIdxBufSize` arguments to allocate more memory (in Mb) for training. Total values of those two arguments should not be more than available system memory.

To change the classifier from Haar to LBP, add `-featureType LBP` argument. 
