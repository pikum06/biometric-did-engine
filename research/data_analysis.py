# Conductiing data analysis and generating plots for the cleaned dataset.


# importing libraries

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def data_analysis(data_path='../data/creditcard_cleaned.csv', output_dir='../output/graphs'):
    """
    Loads the cleaned dataset and generates comprehensive exploratory data analysis (EDA) plots:
    1. Class Distribution (Log Scale)
    2. Transaction Amount Distribution (Fraud vs Normal)
    3. Transaction Time Distribution (Density Over Time)
    4. Feature Correlation Heatmap (Top Features)
    5. Discriminative Feature Boxplots (V10, V12, V14, V17)
    """
    print("Data Analysis & Plot Generation")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cleaned dataset not found at: {data_path}")

    df = pd.read_csv(data_path)
    os.makedirs(output_dir, exist_ok=True)

    # Graph 1: Log-Scaled Class Distribution Countplot

    plt.figure(figsize=(8, 6))
    ax = sns.countplot(x='Class', data=df, palette=['#1f77b4', '#d62728'])
    plt.yscale('log')
    y_max = df['Class'].value_counts().max()
    ax.set_ylim(bottom=1, top=y_max * 8)
    plt.title('Distribution of Classes (0: Normal, 1: Fraudulent)', fontsize=13, pad=20)
    plt.xlabel('Class', fontsize=11, labelpad=10)
    plt.ylabel('Count (Log Scale)', fontsize=11, labelpad=10)

    for p in ax.patches:
        count = int(p.get_height())
        if count > 0:
            ax.annotate(f'{count:,}', 
                        (p.get_x() + p.get_width() / 2., count), 
                        ha='center', 
                        va='bottom', 
                        fontweight='bold',
                        fontsize=10, 
                        color='black', 
                        xytext=(0, 6), 
                        textcoords='offset points')

    plt.tight_layout()
    plot1_path = os.path.join(output_dir, 'class_distribution.png')
    plt.savefig(plot1_path, bbox_inches='tight', pad_inches=0.3, dpi=300)
    plt.close()
    print(f"Saved Class Distribution Plot to: {plot1_path}")

    # Graph 2: Transaction Amount Distribution (Log Density)

    plt.figure(figsize=(9, 5))
    sns.kdeplot(df[df['Class'] == 0]['Amount'] + 1, label='Normal (Class 0)', fill=True, color='blue', log_scale=True)
    sns.kdeplot(df[df['Class'] == 1]['Amount'] + 1, label='Fraud (Class 1)', fill=True, color='red', log_scale=True)
    plt.title('Transaction Amount Distribution (Log Scale)', fontsize=13, pad=15)
    plt.xlabel('Amount', fontsize=11)
    plt.ylabel('Density', fontsize=11)
    plt.legend()
    plt.tight_layout()
    plot2_path = os.path.join(output_dir, 'amount_distribution.png')
    plt.savefig(plot2_path, bbox_inches='tight', pad_inches=0.3, dpi=300)
    plt.close()
    print(f"Saved Transaction Amount Distribution Plot to: {plot2_path}")

    # Graph 3: Transaction Time Distribution

    plt.figure(figsize=(10, 5))
    sns.kdeplot(df[df['Class'] == 0]['Time'], label='Normal (Class 0)', color='blue', common_norm=False)
    sns.kdeplot(df[df['Class'] == 1]['Time'], label='Fraud (Class 1)', color='red', common_norm=False)
    plt.title('Transaction Density Over Time (Seconds)', fontsize=13, pad=15)
    plt.xlabel('Time (Seconds elapsed from first transaction)', fontsize=11)
    plt.ylabel('Density', fontsize=11)
    plt.legend()
    plt.tight_layout()
    plot3_path = os.path.join(output_dir, 'time_distribution.png')
    plt.savefig(plot3_path, bbox_inches='tight', pad_inches=0.3, dpi=300)
    plt.close()
    print(f"Saved Transaction Time Distribution Plot to: {plot3_path}")

    # Graph 4: Correlation Heatmap for Key Features

    plt.figure(figsize=(10, 8))
    correlations = df.corr()
    top_corr_features = correlations['Class'].abs().sort_values(ascending=False).head(12).index
    sns.heatmap(df[top_corr_features].corr(), annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap (Top Features Related to Fraud Class)', fontsize=13, pad=15)
    plt.tight_layout()
    plot4_path = os.path.join(output_dir, 'top_correlation_heatmap.png')
    plt.savefig(plot4_path, bbox_inches='tight', pad_inches=0.3, dpi=300)
    plt.close()
    print(f"Saved Top Correlation Heatmap to: {plot4_path}")

    # Graph 5: Discriminative Feature Boxplots

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    features_to_plot = ['V14', 'V17', 'V12', 'V10']
    for idx, feat in enumerate(features_to_plot):
        r, c = idx // 2, idx % 2
        sns.boxplot(x='Class', y=feat, data=df, ax=axes[r, c], palette=['#1f77b4', '#d62728'])
        axes[r, c].set_title(f'Distribution of {feat} by Class', fontsize=11)
    fig.suptitle('Top Discriminative PCA Features Comparison', fontsize=14, y=1.02)
    fig.tight_layout()
    plot5_path = os.path.join(output_dir, 'discriminative_features_boxplot.png')
    fig.savefig(plot5_path, bbox_inches='tight', pad_inches=0.3, dpi=300)
    plt.close()
    print(f"Saved Discriminative Features Boxplot to: {plot5_path}\n")

if __name__ == '__main__':
    data_analysis()