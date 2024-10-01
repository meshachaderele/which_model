from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Step 1: Determine the problem type
    is_classification = request.form.get('classification') == 'True'
    is_regression = request.form.get('regression') == 'True'
    is_clustering = request.form.get('clustering') == 'True'

    # Ensure that conflicting selections are not made
    if is_classification and is_regression:
        error_message = "You can't select both classification and regression. Please clarify the problem."
        return render_template('error.html', error_message=error_message)
    elif is_classification and is_clustering:
        error_message = "You can't select both classification and clustering. Please clarify the problem."
        return render_template('error.html', error_message=error_message)
    elif is_regression and is_clustering:
        error_message = "You can't select both regression and clustering. Please clarify the problem."
        return render_template('error.html', error_message=error_message)

    # Step 2: Dataset size
    is_large_dataset = request.form.get('large_dataset') == 'True'
    
    # Step 3: Interpretability
    is_high_interpretability_required = request.form.get('interpretability') == 'True'
    
    # Step 4: Feature types
    has_categorical_data = request.form.get('categorical_data') == 'True'
    
    # Step 5: Real-time requirements
    is_real_time_required = request.form.get('real_time') == 'True'
    
    # Using a set to avoid duplicate recommendations
    recommendations = set()
    
    # Classification models
    if is_classification:
        if is_high_interpretability_required:
            recommendations.update(["Decision Trees", "Logistic Regression"])
        if not is_high_interpretability_required and is_large_dataset:
            recommendations.update(["Random Forest", "XGBoost", "Neural Networks"])
        if has_categorical_data:
            recommendations.add("CatBoost (Handles categorical features efficiently)")
        if is_real_time_required:
            recommendations.update(["Logistic Regression", "k-Nearest Neighbors (k-NN)", "Naive Bayes"])

    # Regression models
    elif is_regression:
        if is_high_interpretability_required:
            recommendations.update(["Linear Regression", "Decision Trees (Regression)"])
        if not is_high_interpretability_required and is_large_dataset:
            recommendations.update(["Random Forest Regressor", "XGBoost Regressor", "Neural Networks"])
        if has_categorical_data:
            recommendations.add("CatBoost Regressor")
        if is_real_time_required:
            recommendations.update(["Linear Regression", "Ridge/Lasso Regression"])

    # Clustering models
    elif is_clustering:
        if is_large_dataset:
            recommendations.add("K-Means Clustering (Good for large datasets)")
        else:
            recommendations.update(["Agglomerative Clustering", "DBSCAN (Good for finding non-spherical clusters)"])
        if has_categorical_data:
            recommendations.add("GMM (Gaussian Mixture Models for clustering with categorical data)")

    # If no task is selected
    if not (is_classification or is_regression or is_clustering):
        recommendations.add("No specific task selected. Please review your input.")
    
    return render_template('result.html', recommendations=list(recommendations))

if __name__ == '__main__':
    app.run(debug=True)
