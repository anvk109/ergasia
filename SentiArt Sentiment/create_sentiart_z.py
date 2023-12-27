import pandas as pd

# Load the dataset from the .xlsx file
df = pd.read_excel('sentiment_valence_results.xlsx')

# Compute the z-scores for each column
z_scores_df = (df.iloc[:, 1:] - df.iloc[:, 1:].mean()) / df.iloc[:, 1:].std()
z_scores_df.insert(0, 'Word', df['Word'])

# Save the z-scores to a new .xlsx file
z_scores_df.to_excel('standardized_scores.xlsx', index=False)

print("Standardized scores saved to 'standardized_scores.xlsx'")

