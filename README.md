# Audiosurf Bot

Audiosurf image detection bot.

## Documentations

### Image Detection
- [Object Detection](https://docs.opencv.org/4.5.1/df/dfb/group__imgproc__object.html)
- [Image Flags](https://docs.opencv.org/3.4/d8/d6a/group__imgcodecs__flags.html)
- [Template Matching](https://docs.opencv.org/4.5.1/d4/dc6/tutorial_py_template_matching.html)

### Cascade Classifier
- [Cascade Classifier](https://docs.opencv.org/4.2.0/db/d28/tutorial_cascade_classifier.html)
- [Cascade Training](https://docs.opencv.org/4.2.0/dc/d88/tutorial_traincascade.html)
- [OpenCV on Windows](https://docs.opencv.org/3.4.11/d3/d52/tutorial_windows_install.html)

## OpenCV 3.4.13 Terminal Commands

### Annotation Tool

```shell
opencv_annotation.exe --annotations=pos.txt --images=positive/
```

### Create Positive Samples

```shell
opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec
```

### Train Cascade

```shell
opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -numPos 100 -numNeg 100 -numStages 25 -w 24 -h 24
```