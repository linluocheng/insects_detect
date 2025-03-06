import cv2
imgname = 'mydetect/vermin_pics/R-C.jpg'
img = cv2.imread(imgname)
# 画矩形框
cv2.rectangle(img, (539,414), (881,781), (0,255,0), 4)
# 显示图像
cv2.imshow('show', img)
#一定要加这一句，否则图片会一闪而过
cv2.waitKey(0)