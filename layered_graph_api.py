import matplotlib
matplotlib.use('Agg')  

import pandas as pd
import matplotlib.pyplot as plt
import ast
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

os.makedirs('output_graphs', exist_ok=True)

def extract_r_value(r_column):
    if pd.isna(r_column):
        return None
    try:
        parsed_r = ast.literal_eval(r_column) if isinstance(r_column, str) else r_column
        if isinstance(parsed_r, dict):
            return next(iter(parsed_r.values()))  
    except (ValueError, SyntaxError):
        return None
    return None

@app.route('/generate-graph', methods=['POST'])
def generate_graph():

    file1 = request.files.get('file1')
    file2 = request.files.get('file2')

    if not file1 or not file2:
        return jsonify({"error": "Both file1 and file2 are required"}), 400

    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    df1.rename(columns={'Second': 'time'}, inplace=True)

    df2['range'] = df2['r'].apply(extract_r_value)
    df2.dropna(subset=['range'], inplace=True)

    df2['time'] = range(len(df2))  

    df1['Label'] = df1['Label'].astype(str)

    distress_mask = df1['Label'].str.lower() == 'distress'

    fig, ax = plt.subplots(figsize=(70, 6)) 

    ax.scatter(df1['time'][distress_mask], df1['Prediction'][distress_mask], 
               label='Distress', color='red', alpha=0.8, s=20)

    ax.plot(df2['time'], df2['range'], label='Relative Distance (Line)', color='green', linewidth=2)

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Distance (mm)")
    ax.set_title("Layered Graph: Distress Predictions and Relative Distance")
    ax.legend()
    ax.grid()

    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.locator_params(axis='x', nbins=100)
    plt.locator_params(axis='y', nbins=30)

    output_file = 'output_graphs/layered_graph.png'
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()  
    
    return jsonify({"message": "Graph generated successfully", "graph_url": output_file})

if __name__ == '__main__':
    app.run(debug=True)
