# ANPR using SVM for OCR 🧠

Automatic Number Plate Reconigtion using SVM for OCR  is my work to qualify for electrical engineering degree. 🎓





##  📖 What is it about  ?



 This project use Computer Vision and Machine Learning to build an ANPR. Rather use Neural Network as is comonm, this work is implementing SVM as algorithm for Optical Character Reconigtion. 
 
 




## 🗃️ What you gonna find :


In this repository you gonna find diferents files you could use:

- **Extraction**: this file allows you detect and extract plate's characters. You have to have a image that enclose perfectly the plate's rectangle and just that rectangle. 

-  **PPIF**: (Pre Processing Image Functions) this is a little library with some processing image tecniques using OpenCV and other functions made by me. 

-  **Building_data**: this algorithim builds the data_base file. Take all the trainning examples and sort it in a matrix of n_smaple x n_features.  

	 Note: in this repository I don't provide you the character images to build this matrix. 

- **Training_model**: this algorithim train the SVM model with data_base.csv.  
