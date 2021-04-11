import numpy as np
import cv2
import pywt
import random
import math
import cmath
import dct_algorithm
def Watermarking_DCT(coverImage, watermarkImage):
    #try:	
    coverImage = cv2.resize(coverImage,(512,512))
    	#cv2.imshow('Cover Image',coverImage)
    watermarkImage = cv2.resize(watermarkImage,(64,64))
    	#cv2.imshow('Watermark Image',watermarkImage)
    #except Exception as e:
    #	print(str(e))
    bImg,gImg,rImg = cv2.split(coverImage)

    bImg =  np.float32(bImg)
    watermarkImage = np.float32(watermarkImage) #chuyen doi sang float32

    watermarkImage /= 255  #watermark luc nay la anh xam
    
    blockSize = 8
    c1 = np.size(bImg, 0) # lay kich thuoc toa do x cua anh cover
    c2 = np.size(bImg, 1) # lay kich thuoc toa do y cua anh
    max_message = (c1*c2)/(blockSize*blockSize)#4096 khoi 8*8
    w1 = np.size(watermarkImage, 0) # kich thuoc anh watermark
    w2 = np.size(watermarkImage, 1) 

    #ma tran co so hang = w1*w2 , so cot = 1
    watermarkImage = np.round(np.reshape(watermarkImage,(w1*w2, 1)),0) # lam tron 0 chu so

    if w1*w2 > max_message:
        print("Message too large to fit")
    message_pad = np.ones((int(max_message),1), np.float32) # tao ra ma tran so hang = max_message, mot cot
    
    message_pad[0:w1*w2] = watermarkImage # gan mang

    watermarkedImage = np.ones((c1,c2), np.float32) #tao ma tran co kich thuoc = anh cover

    k=50
    a=0
    b=0

    for kk in range(int(max_message)):
        dct_block = cv2.dct(bImg[b:b+blockSize, a:a+blockSize]) # lay tu b->b+blocksize hang, a->a+blocksize cot
   
        if message_pad[kk] == 0:
            if dct_block[3,1]<dct_block[3,2]:
                temp=dct_block[3,2]
                dct_block[3,2]=dct_block[3,1]
                dct_block[3,1]=temp
        else:
            if dct_block[3,1]>=dct_block[3,2]:
                temp=dct_block[3,2]
                dct_block[3,2]=dct_block[3,1]
                dct_block[3,1]=temp

        if dct_block[3,1]>dct_block[3,2]:
            if dct_block[3,1] - dct_block[3,2] <k:
                dct_block[3,1] = dct_block[3,1]+k/2
                dct_block[3,2] = dct_block[3,2]-k/2
        else:
            if dct_block[3,2] - dct_block[3,1]<k:
                dct_block[3,2] = dct_block[3,2]+k/2
                dct_block[3,1] = dct_block[3,1]-k/2
            
        watermarkedImage[b:b+blockSize, a:a+blockSize]=cv2.idct(dct_block)
        if a+blockSize>=c1-1:
            a=0
            b=b+blockSize
        else:
            a=a+blockSize

    watermarkedImage_8 = np.uint8(watermarkedImage)
    image_color = cv2.merge((watermarkedImage_8,gImg,rImg))
    cv2.imwrite("./watermarked.jpg", image_color)
    cv2.imshow('watermarked',image_color)

def Extract_DCT(watermarkedImage):
    try:	
        watermarkedImage = cv2.resize(watermarkedImage,(512,512))
        #cv2.imshow('Watermarked Image',watermarkedImage)  	
    except Exception as e:
        print(str(e))
    bImg,gImg,rImg = cv2.split(watermarkedImage)
    bImg = np.float32(bImg) #chuyen doi sang float32
    
    wi1 = np.size(bImg, 0) # lay kich thuoc truc x cua anh 
    wi2 = np.size(bImg, 1) # lay kich thuoc truc y cua anh
    signature = np.ones((wi1,wi2),np.float32)
    blockSize=8
    a=0
    b=0
    k=0
    max_block = (wi1*wi2)/(blockSize*blockSize)
    for kk in range(int(max_block)):
        dct_block = cv2.dct(bImg[b:b+blockSize, a:a+blockSize])
        k = dct_block[3,1] - dct_block[3,2]
        if k > 0:
           signature[b:b+blockSize, a:a+blockSize]=0
        else:
           signature[b:b+blockSize, a:a+blockSize]=255
        if a + blockSize >= wi1-1:
            a = 0
            b = b+blockSize
        else:
            a = a+blockSize
    watermarkImage_8 = np.uint8(signature)
    cv2.imwrite('./signature.jpg',watermarkImage_8)
    cv2.imshow('congratulation!!!', watermarkImage_8)
# if __name__ == "__main__":
#     coverImage = cv2.imread('lena.jpg')
#     watermarkImage = cv2.imread('watermark.jpg',0)
#     watermarkedImage = cv2.imread('watermarked.jpg')
#     #bImg,gImg,rImg = cv2.split(watermarkedImage)
#     print("Watermarking...")
#     #print(bImg)
#     print("=====")
#     #print(coverImage)
#     #print('Image Dimensions :', img.shape)
#     #Watermarking_DCT(coverImage,watermarkImage)
#     Extract_DCT(watermarkedImage)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()





