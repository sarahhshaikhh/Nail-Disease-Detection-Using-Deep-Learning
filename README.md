# Nail Disease Detection using Deep Learning
A deep learning-based system that classifies nail disease images with high accuracy. This tool aims to assist dermatologists and individuals in detecting nail diseases by simply uploading an image.

# Overview
This project aims to classify nail images into six categories using a Convolutional Neural Network based on the MobileNetV2 architecture. The system can assist dermatologists or individuals in identifying nail diseases by simply uploading an image.

# Classes Detected:
- Acral Lentiginous Melanoma
- Blue Finger
- Clubbing
- Healthy Nail
- Onychogryphosis
- Pitting

# Dataset & Preprocessing
The dataset includes labeled nail images across six disease categories.
Images were preprocessed for enhanced feature extraction.
Applied data augmentation techniques to improve model generalization:

- Rotation
- Scaling
- Shearing
- Zooming
- Horizontal Flipping

# Model Architecture
Base Model: MobileNetV2 (Pretrained on ImageNet)
- Layers Added:
- Global Average Pooling
- Fully Connected Layers
- Softmax Activation for multiclass classification
- Loss Function: Categorical Cross-Entropy
- Optimizer: Adam

# Training Details
- Epochs: 10
- Batch Size: 32
- Validation Accuracy: 91.6%
- Validation Loss: 0.27

# Deployment
- Backend: Flask
- Frontend: HTML/CSS with Bootstrap
- AI Model: MobileNetV2 (pretrained on ImageNet)
  
# Core Features: <br>
🔍 Real-Time Disease Detection:
- Upload nail images directly via the web interface
- Deep learning model predicts disease class with confidence scores
- Smooth, responsive frontend for real-time interaction

Diagnail AI Chatbot (powered by Chatbase):
- Personalized AI assistant for nail care queries
- Provides suggestions, reminders, and health advice based on user interaction

Expert Consultation:
- Book appointments with certified dermatologists
- Users can select available time slots via a simple interface

Insights Section:
- Nail Health Progress Graph: Visualizes improvements over time
- Heatmap Tracker: Tracks zones of nail damage or recovery
- Health Timeline: Chronological view of past reports and scores
- Trend Analysis: Personalized insights + predictive analytics on future risk

User Forum:
- A supportive community space for users to share experiences
- Ask questions, get answers, and connect with others
- Moderated for safety and privacy

Blog Section
- Curated educational content about nail health, common diseases, and treatment
- Tips from dermatologists, self-care routines, and lifestyle hacks

Profile Management
- Edit personal details and health preferences
- Track appointment history and chatbot conversations

# Data Security & Privacy <br>
- All personal data is securely stored and encrypted <br>
- Health-related information handled with strict confidentiality standards

# How to Run Locally
1. Clone the repository
2. Install requirements: <br>
pip install -r requirements.txt
3. Run the Flask server: <br>
python app.py
4. Open in browser: <br>
http://127.0.0.1:5000/

# Future Improvements
- Improve accuracy with deeper models or fine-tuning
- Add explainability (e.g., Grad-CAM visualization)
- Extend to other skin/nail diseases
- Mobile App version





  

