import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer

# Load simplified symptom-condition mapping
with open('condition_mapping.json') as f:
    data = json.load(f)

# Prepare synthetic dataset
samples = []
labels = []

for condition_id, cond in data['conditions'].items():
    for i in range(3):  # synthetic duplication
        samples.append(cond['symptoms'])
        labels.append(condition_id)

# Convert symptoms to binary features
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(samples)
y = np.array(labels)

# Train classifier
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Prediction function
def predict_condition(symptoms):
    input_vector = mlb.transform([symptoms])
    prediction = model.predict(input_vector)
    return prediction[0]

# Example usage
if __name__ == "__main__":
    test_input = ['cough', 'sore_throat']
    print("Predicted condition:", predict_condition(test_input))
