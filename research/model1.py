# Fraud detection model for biometric DID system

# importing libraries

import pandas
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Loading the dataset

data = pandas.read_csv('../data/creditcard.csv')

print(f"Dataset Shape: {data.shape}")

print(data['Class'].value_counts())

# Visualizing the Imbalance in the Dataset
plt.figure(figsize=(8,6))
ax = sns.countplot(x='Class', data=data)

# Set y-axis to logarithmic scale for better visibility

plt.yscale('log') 

# Expanding the y-axis limits to accommodate the logarithmic scale

y_max = data['Class'].value_counts().max()

# Set the upper limit to 10 times the max count

ax.set_ylim(bottom=1, top=y_max * 8)  

plt.title('Distribution of Classes (0: Normal, 1: Fraudulent)', fontsize=14, pad=20)
plt.xlabel('Class', fontsize=12, labelpad=10)
plt.ylabel('Count', fontsize=12, labelpad=10)

# Annotate the bars with exact counts
for p in ax.patches:
    count = int(p.get_height())
    if count > 0:  # Only annotate if count is greater than 0
        ax.annotate(f'{count}', 
                    (p.get_x() + p.get_width() / 2., count), 
                    ha='center', 
                    va='bottom', 
                    fontweight='bold',
                    fontsize=10, 
                    color='black', 
                    xytext=(0, 6), 
                    textcoords='offset points')

plt.tight_layout()
plt.savefig('../output/model/class_distribution.png')

plt.close()
print("Class distribution plot saved as 'class_distribution.png'")

# Preprocessing the Data    

# Scaling the 'Amount' and 'Time' features

scaler = StandardScaler()
data['scaled_amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1, 1))
data['scaled_time'] = scaler.fit_transform(data['Time'].values.reshape(-1, 1))

# Dropping the original 'Amount' and 'Time' columns

data = data.drop(['Amount', 'Time'], axis=1)    

#Defining the target variable and features

X = data.drop('Class', axis=1)
y = data['Class']

# Splitting the dataset into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Building the Neural Network Model

from keras.models import Sequential
from keras.layers import Dense, Dropout

model =Sequential([
    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Model Compilation

model.compile(
    optimizer='adam', 
    loss='binary_crossentropy', 
    metrics=['accuracy'])

# Model Training

history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=2048,
    validation_split=0.2,
    verbose=1
)

# Model Evaluation

from sklearn.metrics import classification_report, confusion_matrix

y_pred = (model.predict(X_test) > 0.5).astype("int32")

# Classification Report

print("Classification Report")
report = classification_report(y_test, y_pred, output_dict=True)
print(report)

# converting the dictionary to a pandas DataFrame for better visualization

report_df = pandas.DataFrame(report).transpose()

# Adding the total number of samples to the report
report_df.loc['accuracy', 'support'] = len(y_test) 

# Round metrics to 4 decimal places for readability
report_df['precision'] = report_df['precision'].round(4)
report_df['recall'] = report_df['recall'].round(4)
report_df['f1-score'] = report_df['f1-score'].round(4)
report_df['support'] = report_df['support'].astype(int)


# reseting the index to have 'class' as a column instead of an index
report_df.index.name = 'Class / Metric'


# saving the classification report as a CSV file

report_df.to_csv('../output/model/classification_report.csv', index=True)
print("Classification Report saved as 'classification_report.csv'")

# Confusion Matrix

plt.figure(figsize=(6,4))
confusion_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')    
plt.savefig('../output/model/confusion_matrix.png')
plt.close()
print("Confusion Matrix saved as 'confusion_matrix.png'")


# Saving the model
#model.save('../output/model/fraud_detection_model.h5')

#print("Model saved as 'fraud_detection_model.h5'")