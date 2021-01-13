import cv2 as cv

# Total number of images
img_count = 5331

# Outline and crop
idx = 0
image = cv.imread(fr'screenshots\{img_count}.jpg')
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
edged = cv.Canny(image, 10, 250)
(cnts, _) = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
for c in cnts:
    x, y, w, h = cv.boundingRect(c)
    if w > 50 and h > 50:
        idx += 1
        new_img = image[y:y + h, x:x + w]
        cv.imwrite(fr'crops\{str(idx)}.png', new_img)
