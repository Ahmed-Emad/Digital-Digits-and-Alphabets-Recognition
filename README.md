# Digital Digits and Alphabets Recognition

Python program to recognize english digits and alphabets using KNN algorithm.

According to these features:
* [ 0] Aspect Ratio                                   	(double)    0  <  x  <  10
* [ 1] Intensity of ON pixels                         	(double)    0  <  x  <  1
* [ 2] Percent of ON pixels above horizontal half     	(double)    0  <  x  <  1
* [ 3] Percent of ON pixels to right of vertical half 	(double)    0  <  x  <  1
* [ 4] Percent of ON pixels on vertical line 	        	(double)    0  <  x  <  1
* [ 5] Percent of ON pixels on horizontal line 	      	(double)    0  <  x  <  1
* [ 6] Mean X of ON pixels 	                          	(double)    0  <  x  <  1
* [ 7] Mean Y of ON pixels       	                    	(double)    0  <  x  <  1
* [ 8] Standard Deviation X of ON pixels / Width      	(double)    0  <  x  ~< 1
* [ 9] Standard Deviation Y of ON pixels / Height     	(double)    0  <  x  ~< 1
* [10] Vertical state Flips                           	(int)       0 =<  x  <= 10
* [11] Horizontal state Flips                         	(int)       0 =<  x  <= 10
* [12] Is reflected Y axis (Percent)                  	(double)    0  <  x  <  1
* [13] Is reflected X axis (Percent)                  	(double)    0  <  x  <  1


Test Results On '120' image with Train Set of '230' image:
Cells represent percent of correct matches

![Alt text](comparison.png?raw=true "Comparison")
