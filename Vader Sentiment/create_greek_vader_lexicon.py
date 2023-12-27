import csv
import statistics

# Input and output paths
input_file_path = 'my_lexicon.tsv'
output_file_path = 'my_vader_lexicon.txt'

with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile, delimiter='\t')
    for row in reader:
        term = row['Term']
        normalized_polarity = row['Normalized_Polarity']
        
        # Extract individual polarity scores
        polarity_scores = [row['Polarity1'], row['Polarity2'], row['Polarity3'], row['Polarity4']]
        
        # Compute the standard deviation of the polarity scores
        try:
            stddev = statistics.stdev([float(score) for score in polarity_scores if score.isdigit()])
        except statistics.StatisticsError:
            # Handle cases with insufficient data for calculating standard deviation
            stddev = 0
        
        # Write the data to the output file
        outfile.write(f"{term}\t{normalized_polarity}\t{stddev}\t{' '.join(polarity_scores)}\n")