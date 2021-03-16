import os 
import cv2
from matplotlib import pyplot as plt
import numpy as np  
import math 

cap = cv2.VideoCapture(1)
currentWB = cap.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U) 
cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, currentWB)

def qiege(gray):
	gn=gray.ravel()
	gh=np.zeros(256,dtype =int) 

	for i in range (len(gn)):
		gh[gn[i]]+=1
	img= np.zeros((512,512,3),np.uint8)

	for i in range(256):
		cv2.line(img,(i*2,2000),(i*2,2000-gh[i]),(255,0,0),2)

	qu = np.zeros(9)
	qc = math.ceil(256/30)

	for i in range(qc):
		qu[i-1] = gh[(i-1)*30:((i-1)*30+30)].sum()
	max_2=int(0)
	wei=int(0)
	for i in range (qc):
		if qu[i] >max_2:
			max_2=qu[i]
			wei=i

	max_1=int(0)
	wei_1=int(0)
	for i in range(qc):
		if(qu[i] > max_1)and(i != wei):
			max_1=qu[i]
			wei_1=i
	if abs(wei_1-wei)>2:
		print("stranger,none")

#break (realtime)

	elif len(qu) > int(wei + 2):
		
		ret,thresh1 = cv2.threshold(gray,(wei + 2)*30,255,4)
		cv2.imshow('thresh1-f',thresh1)
		cv2.imshow('img',img)
		return thresh1

def houghl(lines):

	lines_data =np.empty([0,8])
	for line in lines: 
		for rho,theta in line:
			a=  np.cos(theta)
			b= np.sin(theta)
			x0 = a*rho 
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))
			cv2.line(tempIamge,(x1,y1),(x2,y2),(0,255,0),5)
			if(x2-x1 != 0):
				slope = abs((y2-y1)/(x2-x1))
				a = np.array([(x1,x2,y1,y2,slope,0,rho,theta)])
				lines_data = np.append(lines_data,a, axis=0)
				#print(slop)
			else:
				slop = 0
				a= np.array([(x1,x2,y1,y2,slope,1,rho,theta)])
				lines_data = np.append(lines_data,a, axis=0)
			for i in range(len(lines_data)):
				if lines_data[i][5] != 1 :
					return lines_data
			


#print("start capture")

while(True):
	try :
		ret,frame = cap.read()
		scr = frame.copy()
		brightLAB = cv2.cvtColor(scr, cv2.COLOR_BGR2LAB)
		red = brightLAB[..., 1]
		ret,red_1 = cv2.threshold (red, 130, 255, 0)
		white_mask = cv2.bitwise_and(scr,scr, mask=red)
		gray = cv2.cvtColor(white_mask,cv2.COLOR_BGR2GRAY)

		thresh1 = qiege(gray)
		
		tempIamge = scr.copy()
		edges = cv2.Canny(gray,150,200,apertureSize = 3)
		lines = cv2.HoughLines(edges,1,np.pi/180,150)
		lines_data=houghl(lines)

#         print("....")

		if cv2.waitKey(1) & 0xFF == ord('q'):
			cap.release()
			cv2.destroyAllWindows()
			break 
			              

	except ValueError:
		print(error)

#print("DONE.")