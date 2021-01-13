# Audiosurf Bot

Audiosurf image detection bot.

## OpenCV Terminal Commands

**Annotation Tool**

```shell
opencv_annotation.exe --annotations=pos.txt --images=positive/
```

**Create Vector File**

```shell
opencv_createsamples.exe -info pos.txt -w 25 -h 25 -num 250 -vec pos.vec
```

**Train Cascade**

```shell
opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -numPos 250 -numNeg 200 -numStages 10 -w 25 -h 25
```