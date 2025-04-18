from flask import Flask, request, render_template, redirect, url_for, session
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_path = "nail_disease_model.keras"
model = load_model(model_path)

class_names = ["Acral Lentiginous Melanoma", "Blue Finger", "Clubbing", "Healthy Nail", "Onychogryphosis", "Pitting"]

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MySQL Database Connection
db = mysql.connector.connect(
    host='localhost',
    port='3307',
    user='root',
    password='',
    database='nail_disease_db'
)
cursor = db.cursor()

# Disease-specific preventive measures
DISEASE_PREVENTIVE_MEASURES = {
    "Acral Lentiginous Melanoma": [
        "Consult a dermatologist immediately.",
        "Avoid prolonged exposure to UV rays.",
        "Monitor the affected area for changes in size or color."
    ],
    "Blue Finger": [
        "Keep your hands warm in cold weather.",
        "Avoid smoking, as it can worsen circulation.",
        "Consult a doctor to rule out underlying conditions."
    ],
    "Clubbing": [
        "Consult a healthcare provider to identify underlying causes.",
        "Avoid smoking and exposure to secondhand smoke.",
        "Maintain a healthy diet rich in vitamins and minerals."
    ],
    "Healthy Nail": [
        "Maintain good nail hygiene.",
        "Keep your nails trimmed and clean.",
        "Moisturize your nails and cuticles regularly."
    ],
    "Onychogryphosis": [
        "Trim thickened nails carefully or seek professional help.",
        "Wear comfortable shoes to avoid pressure on nails.",
        "Consult a podiatrist for long-term management."
    ],
    "Pitting": [
        "Consult a dermatologist for proper diagnosis and treatment.",
        "Avoid trauma to the nails.",
        "Use moisturizers to keep nails and skin hydrated."
    ]
}

@app.route('/')
def home():
    return render_template('login_signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if user:
        session['email'] = email
        return redirect(url_for('index'))
    else:
        return "Invalid Email or Password"

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return "Email already registered. Please login."
    
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    db.commit()

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'email' not in session:
        return redirect(url_for('home'))

    predicted_class = None
    confidence = None
    image_path = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            try:
                image = Image.open(filepath).convert("RGB")
                image = image.resize((224, 224))
                image = np.array(image) / 255.0
                image = np.expand_dims(image, axis=0)

                prediction = model.predict(image)
                predicted_class_index = np.argmax(prediction)
                predicted_class = class_names[predicted_class_index]
                confidence = float(prediction[0][predicted_class_index] * 100)
                image_path = filepath
                user_email = session['email']
                cursor.execute(
                    "INSERT INTO predictions (email, image_path, predicted_class, confidence) VALUES (%s, %s, %s, %s)",
                    (user_email, image_path, predicted_class, confidence)
                )
                db.commit()

            except Exception as e:
                return f"Error processing image: {e}"

    return render_template('index.html', predicted_class=predicted_class, confidence=confidence, image_path=image_path)

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'email' not in session:
        return redirect(url_for('home'))

    email = session['email']

    if 'avatar' not in request.files:
        return "No file uploaded", 400

    file = request.files['avatar']

    if file.filename == '':
        return "No file selected", 400

    if file:
        # Save the file to the upload folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Update the avatar path in the database
        cursor.execute("UPDATE users SET avatar=%s WHERE email=%s", (filepath, email))
        db.commit()

        return redirect(url_for('profile'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' not in session:
        return redirect(url_for('home'))

    current_email = session['email']
    message = None
    success = False

    # Fetch the current avatar path from the database
    cursor.execute("SELECT avatar FROM users WHERE email=%s", (current_email,))
    current_avatar = cursor.fetchone()[0]

    if request.method == 'POST':
        new_email = request.form['email']
        new_password = request.form['password']

        try:
            cursor.execute("UPDATE users SET email=%s, password=%s WHERE email=%s", (new_email, new_password, current_email))
            db.commit()

            session['email'] = new_email
            current_email = new_email

            message = "Profile updated successfully!"
            success = True
        except Exception as e:
            message = f"Error updating profile: {e}"
            success = False

    return render_template('profile.html', current_email=current_email, current_avatar=current_avatar, message=message, success=success)

@app.route('/blog')
def blog():
    return render_template('blog html.html')

@app.route('/user_forum')
def user_forum():
    if 'email' not in session:
        return redirect(url_for('home'))

    # Fetch all forum posts from the database
    cursor.execute("SELECT username, title, content FROM forum_posts ORDER BY created_at DESC")
    forum_posts = cursor.fetchall()

    # Debug: Print fetched data
    print("Fetched Forum Posts:", forum_posts)

    return render_template('user forum.html', forum_posts=forum_posts)
@app.route('/about_us')
def about():
    return render_template('about us.html')

@app.route('/expert_advice')
def expert():
    return render_template('expert_advice.html')

@app.route('/insights')
def insights():
    if 'email' not in session:
        return redirect(url_for('home'))

    email = session['email']

    # Fetch predictions data for the logged-in user
    cursor.execute("SELECT predicted_class, confidence, timestamp, image_path FROM predictions WHERE email=%s ORDER BY timestamp", (email,))
    predictions = cursor.fetchall()

    # Prepare data for the graph
    labels = [prediction[2].strftime('%Y-%m-%d') for prediction in predictions]  # Timestamps
    data = [prediction[1] for prediction in predictions]  # Confidence scores

    # Prepare data for the heatmap (example: count predictions per day)
    heatmap_data = []
    for i, prediction in enumerate(predictions):
        heatmap_data.append({
            'x': i * 50,  # X position (example)
            'y': i * 50,  # Y position (example)
            'value': prediction[1]  # Confidence score as heatmap value
        })

    # Prepare data for the timeline (example: group by month)
    timeline_data = {
        'selected_month': predictions[-1][2].strftime('%b') if predictions else 'Jan',  # Latest month
        'months': list(set([prediction[2].strftime('%b') for prediction in predictions]))  # Unique months
    }

    # Prepare data for the comparison tool
    comparison_data = {
        'previous_month': {
            'health_score': predictions[1][1] if len(predictions) > 1 else "No data available",  # Second-latest confidence score
            'image_path': predictions[1][0] if len(predictions) > 1 else 'https://via.placeholder.com/300'  # Second-latest predicted class
        },
        'current_month': {
            'health_score': predictions[0][1] if predictions else "No data available",  # Latest confidence score
            'image_path': predictions[0][0] if predictions else 'https://via.placeholder.com/300'  # Latest predicted class
        }
    }

    # Prepare data for personalized analysis (example: latest 3 predictions)
    personalized_analysis_data = []
    for prediction in predictions[-3:]:  # Get the latest 3 predictions
        personalized_analysis_data.append({
            'date': prediction[2].strftime('%d %b %Y'),  # Formatted date
            'confidence_score': prediction[1],  # Confidence score
            'diagnosis': prediction[0],  # Predicted class
            'image_path': prediction[3]  # Actual image path from the database
        })

    # Prepare data for predictive analysis
    latest_prediction = predictions[-1][0] if predictions else None
    predictive_analysis_data = {
        'risk': latest_prediction if latest_prediction else 'No Risk',
        'preventive_measures': DISEASE_PREVENTIVE_MEASURES.get(latest_prediction, [
            "Maintain good nail hygiene.",
            "Consult a healthcare provider if you notice any abnormalities."
        ])
    }

    return render_template('insights.html', 
                           labels=labels, 
                           data=data, 
                           heatmap_data=heatmap_data, 
                           timeline_data=timeline_data, 
                           comparison_data=comparison_data, 
                           personalized_analysis_data=personalized_analysis_data, 
                           predictive_analysis_data=predictive_analysis_data)

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'email' not in session:
        return redirect(url_for('home'))

    user_email = session['email']
    title = request.form.get('title')
    content = request.form.get('content')

    # Fetch the username from the users table
    cursor.execute("SELECT name FROM users WHERE email=%s", (user_email,))
    user = cursor.fetchone()
    if not user:
        return "User not found", 404

    username = user[0]

    # Insert the post into the forum_posts table
    cursor.execute(
        "INSERT INTO forum_posts (user_email, username, title, content) VALUES (%s, %s, %s, %s)",
        (user_email, username, title, content)
    )
    db.commit()

    return redirect(url_for('user_forum'))

if __name__ == '__main__':
    app.run(debug=True)