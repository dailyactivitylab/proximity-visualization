from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pytz
import ast
import os

app = Flask(__name__)
CORS(app)

LOCAL_TIMEZONE = "America/Chicago"
PROXIMITY_RANGES = [(0, 1000), (1000, 2000), (2000, 3000), (3000, 4000), (4000, float('inf'))]

OUTPUT_GRAPHS_DIR = 'output_graphs'
os.makedirs(OUTPUT_GRAPHS_DIR, exist_ok=True)


def extract_range_value(row, test_keys):
    if 'r' not in row or pd.isna(row['r']):
        return None
    try:
        parsed_r = ast.literal_eval(row['r']) if isinstance(row['r'], str) else row['r']
        if isinstance(parsed_r, dict):
            for key in parsed_r:
                for test_key in test_keys:
                    if key.endswith(f" {test_key}"):
                        return parsed_r[key]
    except (ValueError, SyntaxError):
        return None
    return None

def generate_graphs(name_df, name):
    plt.close('all')
    
    fig, ax = plt.subplots(figsize=(50, 4))
    ax.plot(name_df['datetime'], name_df['range'], label='Relative Distance', color='blue', alpha=0.7)
    ax.fill_between(name_df['datetime'], name_df['range'], alpha=0.2, color='blue')
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p', tz=pytz.timezone(LOCAL_TIMEZONE)))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    
    ax.set(title=f'{name} Relative Distance', xlabel='Time (Central Time)', ylabel='Distance')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    avg_distance = name_df['range'].mean()
    ax.axhline(y=avg_distance, color='r', linestyle='--', label=f'Avg Distance: {avg_distance:.0f}')
    ax.legend()
    plt.tight_layout()
    
    line_graph_path = os.path.join(OUTPUT_GRAPHS_DIR, f'{name}_line_graph.png')
    plt.savefig(line_graph_path)
    plt.close()
    
    proximity_ranges = [(0, 1000), (1000, 2000), (2000, 3000), (3000, 4000), (4000, float('inf'))]
    proximity_durations = []
    
    for start, end in proximity_ranges:
        subset = name_df[(name_df['range'] >= start) & (name_df['range'] < end)].copy()
        if not subset.empty:
            subset['time_diff'] = subset['datetime'].diff().dt.total_seconds()
            duration = subset['time_diff'].sum() / 60
            proximity_durations.append((f"{start}-{end}", duration))
    
    if proximity_durations:
        labels, durations = zip(*proximity_durations)
        plt.figure(figsize=(10, 6))
        plt.bar(labels, durations, color='skyblue')
        plt.xlabel('Proximity Range')
        plt.ylabel('Duration (minutes)')
        plt.title(f'{name} Proximity Durations')
        plt.tight_layout()
        
        bar_chart_path = os.path.join(OUTPUT_GRAPHS_DIR, f'{name}_bar_chart.png')
        plt.savefig(bar_chart_path)
        plt.close()
    
    df_heatmap = name_df[['datetime', 'range']].set_index('datetime').dropna()
    df_heatmap.index = df_heatmap.index.strftime('%I:%M:%S %p')
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(df_heatmap.T, cmap="coolwarm", cbar_kws={'label': 'Range Difference'})
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Time (Central Time)")
    plt.ylabel("Distance")
    plt.title(f'{name} Difference in Proximity Over Time')
    plt.tight_layout()
    
    heatmap_path = os.path.join(OUTPUT_GRAPHS_DIR, f'{name}_heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    names = request.form.getlist('names')
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    try:
        df = pd.read_csv(file)
        if 't' not in df.columns:
            return jsonify({"error": "Missing expected column 't'"}), 400
        
        for name in names:
            test_keys = [name]
            df['range'] = df.apply(lambda row: extract_range_value(row, test_keys), axis=1)
            name_df = df.dropna(subset=['range']).copy()
            if not name_df.empty:
                name_df.loc[:, 'datetime'] = pd.to_datetime(name_df['t'], unit='s', errors='coerce', utc=True).dt.tz_convert(LOCAL_TIMEZONE)
                name_df['range'] = pd.to_numeric(name_df['range'], errors='coerce')
                
                generate_graphs(name_df, name)
        
        return jsonify({"message": "Graphs generated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5500)