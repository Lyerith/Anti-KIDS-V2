import pandas as pd
import warnings  # Import the warnings module
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset into a DataFrame
data = pd.read_csv("C:\\Users\\63929\\Desktop\\Anti-KIDS\\V1\\scan_results.csv")
print(data.columns)

# Define a function to compute the 'Analysis' column based on feature presence
def compute_analysis(row):
    if row['Keyboard Inputs'] or row['Programs Detected'] or row['Commands'] or row['Links']:
        return 'Malicious'
    else:
        return 'Not Malicious'

# Create a new column 'Analysis' based on the function
data['Analysis'] = data.apply(compute_analysis, axis=1)

# Split the data into features (X) and target (y)
X = data[['Keyboard Inputs', 'Programs Detected', 'Commands', 'Links']]
y = data['Analysis']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Suppress all warnings
warnings.filterwarnings('ignore')

# Print classification report without warnings
print(classification_report(y_test, y_pred))

# Create a confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Print the confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

# Calculate True Positives, True Negatives, False Positives, and False Negatives
tn, fp, fn, tp = conf_matrix.ravel()

# Print these values
print(f"True Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives: {tp}")


# Assuming you have already trained your classifier and have X_test data
#y_pred_proba = classifier.predict_proba(X_test)[:, 1]

# Printing the results
#for i, prob in enumerate(y_pred_proba):
#    print(f"Sample {i + 1}: Probability of being malicious = {prob:.4f}")

# Print the devices and their predicted labels and probabilities
results = data[['USB Device', 'Analysis']]
print(results)