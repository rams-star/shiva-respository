
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Collect accuracy scores
data = {
'Model': ['Logistic Regression', 'Decision Tree', 'SVM', 'KNN'],
'Accuracy': [0.792, 0.789, 0.819,  0.75]
}

# Step 2: Create a DataFrame
df = pd.DataFrame(data)

# Step 3: Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(df['Model'], df['Accuracy'], color='skyblue')
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Model Accuracy Comparison')

# Step 4: Highlight the highest accuracy
max_accuracy = df['Accuracy'].max()
max_model = df.loc[df['Accuracy'] == max_accuracy, 'Model'].values[0]
plt.text(df['Model'].tolist().index(max_model), max_accuracy, f'{max_accuracy:.2f}', ha='center', va='bottom', color='red')

plt.show()
