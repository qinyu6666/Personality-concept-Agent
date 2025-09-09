# import torch, torchvision
# print(torch.__version__)        # 应显示 CUDA 版本
# print(torchvision.__version__)  # 应与 torch 匹配
# print(torch.cuda.is_available())  # 应为 True
# print(torchvision.ops.nms)

import cv2, os, time
idx = int(os.getenv('CAMERA_INDEX', 0))
cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)   # 关键：加 DSHOW
print("open:", cap.isOpened())
ret, f = cap.read()
print("read:", ret, f.shape if ret else "None")
cap.release()
