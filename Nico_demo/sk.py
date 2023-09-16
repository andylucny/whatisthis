# Slovak language dependent code
import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image

fonts = {}

def putText(image,text,pt,fnt,sz,color,thickness=1):
    base_sz = 32
    final_sz = int(base_sz * sz)
    if final_sz in fonts.keys():
        font = fonts[final_sz]
    else:
        font = ImageFont.truetype("c:\\windows\\Fonts\\YuGothL.ttc", final_sz)
        fonts[final_sz] = font
    img = np.zeros((image.shape[0]*4,image.shape[1]*4,3),np.uint8)
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    pos = (10,img.shape[0]//2)
    draw.multiline_text(pos, text, font=font, align='left')
    img = np.asarray(pil_img)
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    if thickness > 1:
        img = cv.dilate(img,cv.getStructuringElement(cv.MORPH_ELLIPSE,(2*thickness-1,2*thickness-1)))
    box = cv.boundingRect(img)
    cond = img[box[1]:box[1]+box[3],box[0]:box[0]+box[2]]
    ih, iw = image.shape[:2]
    ch, cw = cond.shape[:2]
    w, h = min(cw, iw-pt[0]), min(ch, pt[1])
    roi_image = image[pt[1]-h:pt[1],pt[0]:pt[0]+w]
    roi_cond = cond[ch-h:ch,0:w]
    roi_image[roi_cond > 0] = color
    return image

if __name__ == "__main__":
    img = np.zeros((300,300,3),np.uint8)
    putText(img,"Janíčko a Anička",(10,100),0,1.0,(0,0,255),1)
    cv.putText(img,"Janicko a Anicka",(10,200),0,1.0,(0,0,255),1)
    putText(img,"Janíčko a Anička",(10,250),0,3.0,(0,0,255),1)
    cv.imshow("text",img)
    cv.waitKey(0)
