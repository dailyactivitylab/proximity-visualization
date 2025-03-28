# Proximity Tracker Visualization API

## Overview

This Flask-based API generates detailed visualizations to track and analyze proximity data between a family member and a baby. The application processes CSV data to create three distinct graph types that help understand distance patterns over time.

## Requirements

- Python 3.8+
- Required Python Packages:
  - Flask
  - Flask-CORS
  - Pandas
  - Matplotlib
  - Seaborn
  - Pytz

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dailyactivitylab/proximity-visualization.git
   cd proximity-visualization
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the API

```bash
python app.py
```

The API will start on `http://localhost:5500`

### Endpoint: `/analyze`

**Method**: POST

**Parameters**:
- `file`: CSV file containing proximity data
- `names`: List of names to analyze

**CSV File Format**:
- Must contain columns 't' (timestamp)
- Must contain column 'r' with distance/range information

### Example Request (using curl)

```bash
curl -X POST \
  -F "file=@/path/to/your/data.csv" \
  -F "names=MOM" \
  http://localhost:5500/analyze
```

## Output


Generated graphs will be saved in the `output_graphs/` directory:
- `{name}_line_graph.png`
- `{name}_bar_chart.png`
- `{name}_heatmap.png`

# Distress and Proximity Visualization API

## Overview

This Flask-based API generates a layered graph that visualizes the relationship between distress predictions and relative proximity data over time. The application processes two CSV files: one with distress prediction data and one with proximity data, and then creates a graph with the following layers:
- **Distress Predictions** (plotted as red scatter points).
- **Relative Distance** (plotted as a green line).

## Requirements

- Python 3.8+
- Required Python Packages:
  - Flask
  - Pandas
  - Matplotlib
  - ast

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dailyactivitylab/InfantDistressClassification.git
   cd InfantDistressClassification
   
2. Install Dependencies
   pip install -r requirements.txt

### Usage

#### Running the API

```bash
python app.py

### The API will start on `http://localhost:5000`.

## Endpoint: `/generate-graph`

**Method**: POST

### Parameters:

- `file1`: CSV file containing distress prediction data with columns `Second`, `Label`, and `Prediction`.
- `file2`: CSV file containing proximity data with columns `r` (range) and `time` (optional).

### CSV File Format:

#### Distress Prediction Data (file1):
- Must contain columns `Second` (timestamp), `Label` (distress/non-distress), and `Prediction`.

#### Proximity Data (file2):
- Must contain column `r` with relative distance (range) information.

### Example Request (using curl)

```bash
curl -X POST \
  -F "file1=@/path/to/distress_predictions.csv" \
  -F "file2=@/path/to/proximity_data.csv" \
  http://localhost:5000/generate-graph

### Output

Generated graphs will be saved in the `output_graphs/` directory:
- `layered_graph.png`

This file will contain the layered graph that combines distress predictions and relative distance.

