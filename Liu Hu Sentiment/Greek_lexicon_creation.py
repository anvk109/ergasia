import csv

def calculate_average(scores):
    valid_scores = [int(score) for score in scores if score.isdigit()]
    if valid_scores:
        return round(sum(valid_scores) / len(valid_scores), 2)
    return 'N/A'  # Return 'N/A' if all scores are 'N/A'

def convert_polarity(polarity, polarities_so_far):
    if polarity == 'POS':
        return 1
    elif polarity == 'NEG':
        return -1
    elif polarity == 'N/A':
        return 0
    else:  # Both
        if polarities_so_far:
            return process_polarity(polarities_so_far)
        else:
            return 0  # Default to 0 if we don't have any polarities to process

def process_polarity(polarities):
    avg_polarity = sum(polarities) / len(polarities)
    if avg_polarity == 0:
        return 0
    elif avg_polarity < 0:
        return -0.5
    else:
        return 0.5
    
def compute_final_polarity(row):
    emotion_weights = {
        'Anger': -0.1,
        'Disgust': -0.1,
        'Fear': -0.1,
        'Happiness': 0.2,
        'Sadness': -0.1,
        'Surprise': 0.05
    }

    emotion_score = sum(float(row[emotion]) * weight for emotion, weight in emotion_weights.items() if row[emotion] != 'N/A')
    return emotion_score + float(row['Polarity_Avg'])

def normalize(value, original_min, original_max, new_min, new_max):
    # Handle the special case where original_max and original_min are the same
    if original_max == original_min:
        return (new_max + new_min) / 2  # Return the midpoint of the new range
    
    return ((value - original_min) / (original_max - original_min)) * (new_max - new_min) + new_min

input_file_path = 'greek_sentiment_lexicon.tsv'
output_file_path = 'my_lexicon.tsv'

with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter='\t')
    
    # Define new output columns
    new_fieldnames = [field for field in reader.fieldnames if not any(emotion in field for emotion in ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise', 'Polarity', 'Subjectivity','Aditional', 'Comments'])]
    new_fieldnames.extend(['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise', 'Polarity1', 'Polarity2', 'Polarity3', 'Polarity4', 'Polarity_Avg','Emotion_Affected_Polarity','Normalized_Polarity'])
    
    writer = csv.DictWriter(outfile, fieldnames=new_fieldnames, delimiter='\t')
    writer.writeheader()  # Write header

    all_emotion_affected_polarities = []
    rows_to_write = []
    
    for row in reader:
        new_row = {key: row[key] for key in new_fieldnames if key not in ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise', 'Polarity1', 'Polarity2', 'Polarity3', 'Polarity4', 'Polarity_Avg','Emotion_Affected_Polarity','Normalized_Polarity']}
        
        # Collect polarities first
        polarities_data = [(i, row[f'Polarity{i}']) for i in range(1, 5)]

        # Sort polarities so that BOTH is processed last
        sorted_polarities_data = sorted(polarities_data, key=lambda x: x[1] == 'BOTH')

        polarities = []
        for i, polarity in sorted_polarities_data:
            polarity_val = convert_polarity(polarity, polarities)
            polarities.append(polarity_val)
            new_row[f'Polarity{i}'] = polarity_val
        
        new_row['Polarity_Avg'] = round(sum(polarities) / 4, 2)
        
        for emotion in ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise']:
            scores = [row[f'{emotion}{i}'] for i in range(1, 5)]
            avg_score = calculate_average(scores)
            new_row[emotion] = avg_score  # Set the average score to the emotion column
        
        # Calculate the final polarity influenced by other emotions
        emotion_affected_polarity = compute_final_polarity(new_row)
        new_row['Emotion_Affected_Polarity'] = round(emotion_affected_polarity, 2)
        all_emotion_affected_polarities.append(emotion_affected_polarity)

        rows_to_write.append(new_row)

    # Find the min and max of Emotion_Affected_Polarity to normalize later
    min_polarity = min(all_emotion_affected_polarities)
    max_polarity = max(all_emotion_affected_polarities)

    for row in rows_to_write:
        normalized_polarity = normalize(row['Emotion_Affected_Polarity'], min_polarity, max_polarity, -4, 4)
        row['Normalized_Polarity'] = round(normalized_polarity, 2)
        writer.writerow(row)

print(f"Processed lexicon saved to {output_file_path}")
