# Nail Disease Detection using Deep Learning
A deep learning-based system that classifies nail disease images with high accuracy. This tool aims to assist dermatologists and individuals in detecting nail diseases by simply uploading an image.

# Overview
This project aims to classify nail images into six categories using a Convolutional Neural Network based on the MobileNetV2 architecture. The system can assist dermatologists or individuals in identifying nail diseases by simply uploading an image.

# 🔬 Classes Detected:
- Acral Lentiginous Melanoma
- Blue Finger
- Clubbing
- Healthy Nail
- Onychogryphosis
- Pitting

# 📂 Dataset & Preprocessing
The dataset includes labeled nail images across six disease categories.
Images were preprocessed for enhanced feature extraction.
Applied data augmentation techniques to improve model generalization:

- Rotation
- Scaling
- Shearing
- Zooming
- Horizontal Flipping

# 🧠 Model Architecture
Base Model: MobileNetV2 (Pretrained on ImageNet)
- Layers Added:
- Global Average Pooling
- Fully Connected Layers
- Softmax Activation for multiclass classification
- Loss Function: Categorical Cross-Entropy
- Optimizer: Adam

# 🏋️ Training Details
- Epochs: 10
- Batch Size: 32
- Validation Accuracy: 91.6%
- Validation Loss: 0.27

# 🚀 Deployment
- Backend: Flask
- Frontend: HTML/CSS with Bootstrap
- Functionality:
- Upload an image via browser
- Model returns predicted class with confidence
- Real-time, responsive prediction interface

# 🧪 How to Run Locally
1. Clone the repository
2. Install requirements:
pip install -r requirements.txt
3. Run the Flask server:
python app.py
4. Open in browser:
http://127.0.0.1:5000/

# ✨ Future Improvements
- Improve accuracy with deeper models or fine-tuning
- Add explainability (e.g., Grad-CAM visualization)
- Extend to other skin/nail diseases
- Mobile App version

# 🧑‍💻 Author
Sarah Shaikh <br>
Aspiring Data & Business Analyst | Passionate about AI for social good <br>
https://www.linkedin.com/in/sarah-shaikh-07a3b3289/




  

