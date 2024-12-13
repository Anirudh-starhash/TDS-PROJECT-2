import requests
import json
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from sklearn.cluster import KMeans

AIPROXY_TOKEN = os.environ["AIPROXY_TOKEN"]

# Load your CSV file
def load_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Extract metadata and basic information about the dataset
def get_dataset_information(df):
    information = {
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "missing_values": df.isnull().sum().to_dict(),
        "summary_stats": df.describe(include='all').to_dict(),
        "sample_data": df.head(3).to_dict(orient='records')
    }
    return information

# Extract smaller subsets of data for analysis
def extract_relevant_data(df, max_rows=100):
    numeric_data = df.select_dtypes(include=["number"]).sample(n=min(len(df), max_rows), random_state=42)
    categorical_data = df.select_dtypes(exclude=["number"]).sample(n=min(len(df), max_rows), random_state=42)
    return {
        "numeric_sample": numeric_data.to_dict(orient='records'),
        "categorical_sample": categorical_data.to_dict(orient='records')
    }

# Define analysis functions for OpenAI function calling
def define_analysis_functions():
    return {
        "outlier_detection": {
            "description": "Detect outliers in numeric data using the 3-sigma rule.",
            "parameters": {"data": "array of numbers"}
        },
        "correlation_analysis": {
            "description": "Compute the correlation matrix for numeric data.",
            "parameters": {"data": "array of numeric columns"}
        },
        "time_series_anomalies": {
            "description": "Detect anomalies in time series data.",
            "parameters": {"timestamps": "array of timestamps", "values": "array of numbers"}
        },
        "geographic_analysis": {
            "description": "Perform geographic analysis and clustering based on latitude and longitude.",
            "parameters": {"latitude": "array of latitudes", "longitude": "array of longitudes"}
        },
        "storytelling": {
            "description": "Write a story about the dataset analysis including data, insights, and implications.",
            "parameters": {"metadata": "object", "analysis_results": "object", "charts": "array of chart paths"}
        }
    }

# Send a request to OpenAI for analysis suggestions
def request_llm_analysis(metadata, data_samples, functions):
    prompt = (
        "You are a data analysis assistant. Based on the dataset metadata and provided samples, choose an appropriate function from the provided functions. "
        "Return results in JSON or as DataFrame-ready structures. Here is the metadata:\n" + json.dumps(metadata, indent=2) + "\n"
        "Here are the data samples:\n" + json.dumps(data_samples, indent=2) + "\n"
        "Functions:\n" + json.dumps(functions, indent=2)
    )

    try:
        headers = {
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful data analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            "functions": functions
        }
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error with OpenAI request: {e}")
        return None

# Request storytelling from OpenAI after analysis and visualization
def request_llm_storytelling(metadata, analysis_results, chart_paths):
    prompt = (
        "You are a data analysis assistant. Based on the dataset metadata, analysis results, and provided charts, write a narrative that includes:\n"
        "1. A summary of the dataset.\n"
        "2. The analysis performed.\n"
        "3. Insights discovered.\n"
        "4. Implications of the findings.\n"
        "Here is the metadata:\n" + json.dumps(metadata, indent=2) + "\n"
        "Here are the analysis results:\n" + json.dumps(analysis_results, indent=2) + "\n"
        "Here are the chart paths:\n" + json.dumps(chart_paths, indent=2)
    )

    try:
        headers = {
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful storytelling assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error with OpenAI request: {e}")
        return None

# Filter data before analysis for each function
def prepare_function_data(df, function_name):
    if function_name == "outlier_detection" or function_name == "correlation_analysis":
        return df.select_dtypes(include=["number"]).head(100).to_dict(orient="records")
    elif function_name == "time_series_anomalies":
        if "timestamp" in df.columns and len(df.select_dtypes(include=["number"]).columns) > 0:
            return {
                "timestamps": df["timestamp"].head(100).tolist(),
                "values": df.select_dtypes(include=["number"]).iloc[:, 0].head(100).tolist()
            }
        else:
            return None
    elif function_name == "geographic_analysis":
        if "latitude" in df.columns and "longitude" in df.columns:
            return {
                "latitude": df["latitude"].head(100).tolist(),
                "longitude": df["longitude"].head(100).tolist()
            }
        else:
            return None
    elif function_name == "storytelling":
        return {
            "metadata": get_dataset_information(df),
            "analysis_results": "Summary of analysis functions applied.",
            "charts": ["correlation_matrix.png", "outliers.png", "time_series_anomalies.png", "geographic_analysis.png"]
        }
    else:
        return None

# Visualization functions
def visualize_correlation_matrix(correlation_matrix):
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Matrix Heatmap")
    plt.savefig("correlation_matrix.png")
    plt.close()

def visualize_outliers(outliers):
    outliers_df = pd.DataFrame(outliers)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=outliers_df, x="index", y="value", hue="is_outlier", palette="Set1")
    plt.title("Outlier Detection")
    plt.savefig("outliers.png")
    plt.close()

def visualize_time_series_anomalies(timestamps, values, anomalies):
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, values, label="Values", marker="o")
    plt.scatter([timestamps[i] for i in anomalies], [values[i] for i in anomalies], color="red", label="Anomalies")
    plt.title("Time Series Anomalies")
    plt.legend()
    plt.savefig("time_series_anomalies.png")
    plt.close()

def visualize_geographic_analysis(latitudes, longitudes, cluster_labels):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=longitudes, y=latitudes, hue=cluster_labels, palette="viridis")
    plt.title("Geographic Clustering")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("geographic_analysis.png")
    plt.close()

# Main workflow
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a CSV file using OpenAI-powered functions.")
    parser.add_argument("file_name", type=str, help="Name of the CSV file to analyze.")
    args = parser.parse_args()

    df = load_csv(args.file_name)
    if df is not None:
        metadata = get_dataset_information(df)
        data_samples = extract_relevant_data(df)
        functions = define_analysis_functions()

        analysis_results = {}
        chart_paths = []

        for function_name, function_details in functions.items():
            if function_name == "storytelling":
                continue

            relevant_data = prepare_function_data(df, function_name)
            if relevant_data:
                print(f"Requesting analysis for {function_name}...")
                result = request_llm_analysis(metadata, {"data": relevant_data}, {function_name: function_details})

                if result:
                    print(f"Results for {function_name}:")
                    print(json.dumps(result, indent=2))
                    analysis_results[function_name] = result

                    # Visualization based on function name
                    if function_name == "correlation_analysis":
                        visualize_correlation_matrix(pd.DataFrame(result))
                        chart_paths.append("correlation_matrix.png")
                    elif function_name == "outlier_detection":
                        visualize_outliers(result)
                        chart_paths.append("outliers.png")
                    elif function_name == "time_series_anomalies":
                        visualize_time_series_anomalies(
                            relevant_data["timestamps"],
                            relevant_data["values"],
                            result.get("anomalies", [])
                        )
                        chart_paths.append("time_series_anomalies.png")
                    elif function_name == "geographic_analysis":
                        cluster_labels = result.get("cluster_labels", [])
                        visualize_geographic_analysis(
                            relevant_data["latitude"],
                            relevant_data["longitude"],
                            cluster_labels
                        )
                        chart_paths.append("geographic_analysis.png")

        # Request storytelling after analysis and visualization
        storytelling_result = request_llm_storytelling(metadata, analysis_results, chart_paths)
        if storytelling_result:
            print("Storytelling Result:")
            print(json.dumps(storytelling_result, indent=2))
