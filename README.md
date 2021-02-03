# Audiosurf 2 Bot

Audiosurf 2 bot using Haar Cascade.

## Quickstart

Run the script and play the game. The bot will take over once it detects incoming blocks and spikes.

The current x and y offsets in `capture` are based on 1920x1080 monitor. Change them according to monitor resolution to get the center region of the game.

## Cascade Classifier Docs
- [Cascade Classifier](https://docs.opencv.org/4.5.1/db/d28/tutorial_cascade_classifier.html)
- [Cascade Training](https://docs.opencv.org/4.5.1/dc/d88/tutorial_traincascade.html)
- [OpenCV on Windows](https://docs.opencv.org/3.4.13/d3/d52/tutorial_windows_install.html)
- [Tutorial](http://note.sonots.com/SciSoftware/haartraining.html)

## Training Data

### Raw Images

3000 screenshots with 600x500 dimension. 1000 images for each lane.

### Positive Samples

Blocks: 1151 samples from 350 images.

Spikes: 530 samples from 300 images.

### Negative Samples

Blocks: 350 images.

Spikes: 300 images.

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
opencv_createsamples.exe -info pos_block.txt -w 24 -h 24 -num 1200 -vec pos_block.vec

opencv_createsamples.exe -info pos_spike.txt -w 24 -h 24 -num 600 -vec pos_spike.vec
```

Change `-num` argument as needed for a different value of positive samples.

### Train Cascade

```shell
opencv_traincascade.exe -data cascade_block/ -vec pos_block.vec -bg neg_block.txt -numPos 900 -numNeg 350 -numStages 25 -w 24 -h 24 -precalcValBufSize 2048 -precalcIdxBufSize 2048

opencv_traincascade.exe -data cascade_spike/ -vec pos_spike.vec -bg neg_spike.txt -numPos 400 -numNeg 300 -numStages 25 -w 24 -h 24 -precalcValBufSize 2048 -precalcIdxBufSize 2048
```

Width and height dimensions need to be the same as the positive samples.

Use `-precalcValBufSize` and `-precalcIdxBufSize` arguments to allocate more memory (in Mb) for training. Total values of those two arguments should not be more than available system memory.

To change the classifier from Haar to LBP, add `-featureType LBP` argument. 

## Limitations

This bot currently only works with the [GlowTastic](https://steamcommunity.com/sharedfiles/filedetails/?id=808429383&searchtext=glowtastic) skin. Keyboard inputs were used because the game blocks mouse movements from Python script.
