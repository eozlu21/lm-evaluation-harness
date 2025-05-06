import json
import os
import glob
import pandas as pd
import re


# Function to flatten the nested structure
def flatten_data(data_item):
    flattened = {
        'file_name': data_item.get('file_name').split('\\')[-1],  # Extract the file name from the path
        #'doc_id': data_item.get('doc_id'),
        'section': data_item.get('doc', {}).get('section'),
        'question_number': data_item.get('doc', {}).get('question_number'),
        #'page': data_item.get('data').get('doc', {}).get('page'),
        #'question': data_item.get('doc', {}).get('question'),
        'has_image': data_item.get('doc', {}).get('has_image'),
        #'passage': data_item.get('doc', {}).get('passage'),
        'target': data_item.get('target'),
        'acc': data_item.get('acc'),
    }
    


    
    return flattened




# Define the path to the directory containing the JSONL files
# Create absolute path to 'result_logs/' assuming it's next to the script
directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'result_logs'))

# Use glob to find all JSONL files in the directory

jsonl_files = glob.glob(os.path.join(directory_path, '*.jsonl'))

# Print the list of JSONL files found

if not jsonl_files:
    print(f"No JSONL files found in the specified directory. {directory_path}")
    exit(1)
else:
    print(f"Found {len(jsonl_files)} JSONL files:")
for file in jsonl_files:
    print(file)



# Initialize an empty list to store the parsed data

big_data_list = []
 
for jsonl_path in jsonl_files:


    # Read the JSONL file and parse each line
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Parse each line as a JSON object
                data = json.loads(line.strip())
                data["file_name"] = re.split(r'[\\/]',jsonl_path)[-1]  # Extract the file name from the path
                big_data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")


print(f"Successfully loaded {len(big_data_list)} records from the JSONL file.")

    
# Flatten each item in the list
flattened_data = [flatten_data(item) for item in big_data_list]
# Create a DataFrame
df = pd.DataFrame(flattened_data)


# First, compute total, correct, and no_image
grouped_df = df.groupby(['file_name', 'section']).agg(
    total=('acc', 'count'),
    correct=('acc', lambda x: (x == 1).sum()),
    no_image=('has_image', lambda x: (~x).sum())
).reset_index()

# Then compute correct_no_image separately
# Step 1: create a helper column
df['correct_no_image_flag'] = (df['acc'] == 1) & (~df['has_image'])

# Step 2: group and count it
correct_no_image_df = df.groupby(['file_name', 'section'])['correct_no_image_flag'].sum().reset_index()
correct_no_image_df.rename(columns={'correct_no_image_flag': 'correct_no_image'}, inplace=True)

# Step 3: merge it back into grouped_df
grouped_df = pd.merge(grouped_df, correct_no_image_df, on=['file_name', 'section'])

# Optional: add accuracy %
grouped_df['accuracy'] = grouped_df['correct'] / grouped_df['total']
# Optional: add accuracy %
grouped_df['accuracy'] = grouped_df['correct'] / grouped_df['total']

# Avoid divide-by-zero issues:
grouped_df['accuracy_no_image'] = grouped_df.apply(
    lambda row: row['correct_no_image'] / row['no_image'] if row['no_image'] > 0 else None,
    axis=1
)


# Overall aggregation

overall_df = grouped_df.groupby('file_name').agg(
    total=('total', 'sum'),
    correct=('correct', 'sum'),
    no_image=('no_image', 'sum'),
    correct_no_image=('correct_no_image', 'sum')
).reset_index()

# Add accuracy columns
overall_df['accuracy'] = overall_df['correct'] / overall_df['total']
overall_df['accuracy_no_image'] = overall_df.apply(
    lambda row: row['correct_no_image'] / row['no_image'] if row['no_image'] > 0 else None,
    axis=1
)

# Save the DataFrame to a CSV file

output_csv_path = os.path.join(os.path.dirname(__file__),'section_based_results.csv')

grouped_df.to_csv(output_csv_path, index=False)
overall_csv_path = os.path.join(os.path.dirname(__file__),'overall_results.csv')
overall_df.to_csv(overall_csv_path, index=False)

print(f"Results saved to {output_csv_path} and {overall_csv_path}.")

