@app.route('/insights')
def insights():
    if 'email' not in session:
        return redirect(url_for('home'))

    email = session['email']

    # Fetch predictions data for the logged-in user
    cursor.execute("SELECT predicted_class, confidence, timestamp FROM predictions WHERE email=%s ORDER BY timestamp", (email,))
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

    # Prepare data for the comparison tool (example: compare latest two predictions)
    comparison_data = {
        'previous_month': {
            'health_score': predictions[-2][1] if len(predictions) > 1 else 0,  # Second-latest confidence score
            'image_path': predictions[-2][0] if len(predictions) > 1 else 'https://via.placeholder.com/300'  # Second-latest predicted class
        },
        'current_month': {
            'health_score': predictions[-1][1] if predictions else 0,  # Latest confidence score
            'image_path': predictions[-1][0] if predictions else 'https://via.placeholder.com/300'  # Latest predicted class
        }
    }

    # Prepare data for personalized analysis (example: latest 3 predictions)
    personalized_analysis_data = []
    for prediction in predictions[-3:]:  # Get the latest 3 predictions
        personalized_analysis_data.append({
            'date': prediction[2].strftime('%d %b %Y'),  # Formatted date
            'confidence_score': prediction[1],  # Confidence score
            'diagnosis': prediction[0],  # Predicted class
            'image_path': 'https://via.placeholder.com/100'  # Placeholder image (replace with actual image path if available)
        })

    # Prepare data for predictive analysis (example: risk based on latest prediction)
    predictive_analysis_data = {
        'risk': predictions[-1][0] if predictions else 'No Risk',  # Latest predicted class
        'preventive_measures': [
            'Keep your nails dry and clean.',
            'Use antifungal creams as recommended.',
            'Avoid walking barefoot in public areas.'
        ]
    }

    return render_template('insights.html', 
                           labels=labels, 
                           data=data, 
                           heatmap_data=heatmap_data, 
                           timeline_data=timeline_data, 
                           comparison_data=comparison_data, 
                           personalized_analysis_data=personalized_analysis_data, 
                           predictive_analysis_data=predictive_analysis_data)