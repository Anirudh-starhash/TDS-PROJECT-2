# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "seaborn",
#   "pandas",
#   "matplotlib",
#   "httpx",
#   "scikit-learn",
#   "chardet",
#   "numpy",
#   "ipykernel",
# ]
# ///

import requests
import json
import os
import pandas as pd
import numpy as np
import seaborn as sns
import argparse
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

AIPROXY_TOKEN = os.environ["AIPROXY_TOKEN"]

# Load your CSV file
def load_csv(file_path):
    # Load a CSV file into a DataFrame
    try:
        data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try with 'ISO-8859-1' encoding
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    
def get_info(df):
    # Extract metadata such as column names, data types, and summary statistics
    information = {
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "missing_values": df.isnull().sum().to_dict(),
        "summary_stats": df.describe(include='all').to_dict(),
        "sample_data": df.head(3).to_dict(orient='records')
    }
    return information

def extract_relevant_data(df, max_rows=100):
    # Extract numeric and categorical data samples for analysis
    numeric_data = df.select_dtypes(include=["number"]).sample(n=min(len(df), max_rows), random_state=42)
    categorical_data = df.select_dtypes(exclude=["number"]).sample(n=min(len(df), max_rows), random_state=42)
    return {
        "numeric_sample": numeric_data.to_dict(orient='records'),
        "categorical_sample": categorical_data.to_dict(orient='records')
    }

def define_analysis_tools():
    return [
        {
            "name": "outlier_detection",
            "description": "Detect outliers in numeric data using the 3-sigma rule.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"type": "number"}
                    }
                },
                "required": ["data"]
            }
        },
        {
            "name": "storytelling",
            "description": "Write a story about the dataset analysis including data, insights, and implications.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metadata": {"type": "object"},
                    "analysis_results": {"type": "object"},
                    "charts": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["metadata", "analysis_results", "charts"]
            }
        }
    ]
    
import json
import requests

def request_llm_storytelling(info, analysis_results, chart_paths):
    prompt = (
        "You are a data analysis assistant. Based on the dataset info, analysis results, and provided charts, write a concise and structured narrative that includes:\n"
        "1. A summary of the dataset, including key characteristics like missing data, outliers, and correlations.\n"
        "2. The analysis performed, focusing on outlier detection and correlation analysis.\n"
        "3. Insights discovered from the analysis, including trends in data like polarized ratings, correlations, etc.\n"
        "4. Implications of the findings and recommendations based on insights.\n\n"
        "Here is the dataset information:\n" + json.dumps(info, indent=2) + "\n\n"
        "Here are the analysis results:\n" + json.dumps(analysis_results, indent=2) + "\n\n"
        "Here are the chart paths (corresponding to the analyses):\n" + json.dumps(chart_paths, indent=2)
    )

    try:
        # Set up headers and data for the API call
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

        # Make the API call
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        # Check the response status
        if response.status_code == 200:
            story_content = response.json()["choices"][0]["message"]["content"]

            # Format the story in a way that works well with save_to_readme function
            formatted_story = (
                f"### Narrative:\n\n"
                f"#### Summary of the Dataset:\n"
                f"- **Total Entries**: {info.get('total_entries', 'N/A')}\n"
                f"- **Missing Values**: {', '.join(f'{key}: {value}' for key, value in info.get('missing_values', {}).items())}\n"
                f"- **Outliers**: {', '.join(f'{outlier}' for outlier in analysis_results.get('outliers', []))}\n\n"
                f"#### The Analysis Performed:\n"
                f"- **Outlier Detection**: {analysis_results.get('outlier_detection', 'N/A')}\n"
                f"- **Correlation Analysis**: {analysis_results.get('correlation_analysis', 'N/A')}\n\n"
                f"#### Insights Discovered:\n"
                f"{story_content}\n\n"
                f"#### Implications of the Findings:\n"
                f"- {analysis_results.get('implications', 'N/A')}\n\n"
            )

            return formatted_story
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error with OpenAI request: {e}")
        return None


# Filter data before analysis for each function
def prepare_function_data(df, function_name):
    # Prepare relevant data subsets for each function to avoid sending the full dataset
    if function_name == "outlier_detection" or function_name == "correlation_analysis":
        return df.select_dtypes(include=["number"]).head(100).to_dict(orient="records")  # Numeric data sample
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
    else:
        return None
    

def request_llm_analysis(metadata, data_samples, tool):
    prompt = (
        "You are a data analysis assistant. Based on the dataset metadata and provided samples, "
        "choose an appropriate tool from the provided tools. Return results in JSON or as DataFrame-ready structures. "
        "Here is the metadata:\n" + json.dumps(metadata, indent=2) + "\n"
        "Here are the data samples:\n" + json.dumps(data_samples, indent=2) + "\n"
        "Tools:\n" + json.dumps(tools, indent=2)
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
            "response_format":  {
                "type" : "json_object"
            },
            "tools": [
                {
                    "type": "function",
                    "function": tool 
                }
               
            ],
            "tool_choice" :
                {
                    "type" :  "function",
                    "function" : {
                        "name" : tool["name"]
                    }
                }
            
        }
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error with OpenAI request: {e}")
        return None


def save_to_readme(storytelling_result, tool, directory_name, tool_name="storytelling"):
    try:
        # Create the folder path using the provided directory_name
        folder_path = os.path.join(os.getcwd(), directory_name)
        os.makedirs(folder_path, exist_ok=True)

        # Define the path for the README.md
        readme_path = os.path.join(folder_path, "README.md")

        # Open the README.md file to write the storytelling results
        with open(readme_path, "w",encoding="utf-8") as readme_file:
            if storytelling_result:
                # Write the tool name as a header
                readme_file.write(f"## {tool_name} Result for {directory_name}.csv:\n\n")
                
                # Write the storytelling result (already formatted neatly)
                readme_file.write(storytelling_result)
            else:
                # If no result, mention no relevant data available
                readme_file.write(f"## {tool_name} Result for {tool['name']}:\n\n")
                readme_file.write(f"No relevant data available for this {tool['name']}.\n")

            # Add extra space between different sections
            readme_file.write("\n\n")
        
        print(f"README.md successfully saved in {directory_name} folder.")
    except Exception as e:
        print(f"Error writing to README.md: {e}")


        
def visualize_outliers(outliers):
    outliers = np.array(outliers)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(6.4, 6.4))  # Original size to match the 512x512 px requirement after saving

    # Generate the stripplot
    sns.stripplot(x=outliers, color="red", jitter=True, ax=ax)

    # Add titles and labels
    ax.set_title("Outlier Detection Visualization", fontsize=14)
    ax.set_xlabel("Values", fontsize=12)

    return fig  # Return the figure object instead of the file name

def create_directory_for_file(file_name):
    directory_name = os.path.splitext(file_name)[0]
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name

def save_chart(chart, directory_name, chart_name):
    os.makedirs(directory_name, exist_ok=True)
    chart_path = os.path.join(directory_name, chart_name)
    chart.savefig(chart_path, dpi=80)  # Save with 80 dpi for 512x512 px
    plt.close(chart)  # Close the figure after saving to free up memory
    

    return chart_path  # Return the saved chart path

if  __name__== "__main__"  :
    parser = argparse.ArgumentParser(description="Analyze a CSV file using OpenAI-powered functions.")
    parser.add_argument("file_name", type=str, help="Name of the CSV file to analyze.")
    args = parser.parse_args()

    df = load_csv(args.file_name)
    if df is not None :
        information=get_info(df)
        dataset=extract_relevant_data(df)
        tools = define_analysis_tools()
        analysis_results = {}
        chart_paths = []
        
        directory_name = create_directory_for_file(args.file_name)
        for tool in tools:
            if tool["name"] == "storytelling":
                continue

            relevant_data = prepare_function_data(df, tool["name"])
            if relevant_data:
                print(f"Requesting analysis for {tool['name']}...")
                result = request_llm_analysis(information, {"data": relevant_data}, tool)
                result=json.loads(result)["data"]

                if result:
                    print(f"Results for {tool['name']}:\n", result)
                    analysis_results[tool["name"]] = result
                    if tool["name"] == "outlier_detection":
                        chart = visualize_outliers(result)
                        chart_paths.append(save_chart(chart, directory_name, "outliers.png"))


        storytelling_tool = next((tool for tool in tools if tool["name"] == "storytelling"), None)
        if storytelling_tool:
            storytelling_result = request_llm_storytelling(information, analysis_results, chart_paths)
            save_to_readme(storytelling_result, storytelling_tool, directory_name)  # Pass directory_name here
        else:
            save_to_readme(None, storytelling_tool, directory_name)  # Pass directory_name here