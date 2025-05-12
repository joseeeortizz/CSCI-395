# NYC Subway Accessibility Analysis

## Overview
This project analyzes the accessibility of New York City's subway system by examining the distribution and characteristics of subway entrances and exits across the five boroughs. The analysis focuses on identifying areas with limited accessibility options, particularly for individuals with mobility challenges who require elevator access.

## Background
New York City's subway system is one of the largest and oldest public transportation networks in the world. While it provides essential transportation for millions of residents and visitors daily, the system's age and design present accessibility challenges. Understanding the current state of subway entrance accessibility is crucial for urban planning, equity considerations, and improving the system for all users.

## Data Source
This analysis uses the [MTA Subway Entrances and Exits (2024)](https://data.ny.gov/Transportation/MTA-Subway-Entrances-and-Exits-2024/i9wp-a4ja/about_data) dataset, which provides detailed information about each subway entrance and exit in the NYC system, including location, entrance type, and accessibility features.

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### Dependencies
The project requires several Python libraries. You can install them using:

```bash
pip install -r requirements.txt
```

Key dependencies include:
- pandas & numpy for data manipulation
- matplotlib & seaborn for data visualization
- folium for interactive maps
- scikit-learn for analysis

## Project Structure
- `Project01.ipynb`: Main Jupyter notebook containing the analysis
- `MTA_Subway_Entrances_and_Exits__2024_20250418.csv`: Dataset used for analysis
- `MTA_SubwayEntrancesAndExits_DataDictionary.pdf`: Documentation for the dataset
- `MTA_SubwayEntrancesAndExits_Overview.pdf`: Overview of the dataset

## Methodology
The analysis follows these steps:
1. Data loading and exploration
2. Data cleaning and preparation
3. Exploratory data analysis
   - Analysis of subway entrances by borough
   - Analysis of entrance types
   - Analysis of elevator access by borough
4. Geospatial analysis using interactive maps
5. Analysis of subway lines and their accessibility
6. Identification of accessibility gaps

## Key Findings

### Borough Disparities
There are significant differences in subway entrance accessibility across the five boroughs, with some boroughs having much better elevator access than others.

### Entrance Types
The vast majority of subway entrances are stairs, with elevators making up only a small percentage of all entrances. This presents significant challenges for individuals with mobility limitations.

### Subway Line Accessibility
Some subway lines have much better accessibility than others, with certain lines having a much higher percentage of entrances with elevator access.

### Accessibility Gaps
The analysis identified numerous stations with no elevator access at all, including some high-traffic stations that serve as major transit hubs.

## Usage
To run the analysis:
1. Clone this repository
2. Install the required dependencies
3. Open `Project01.ipynb` in Jupyter Notebook or JupyterLab
4. Run the cells in sequence

## Author
José Miguel Ortiz  
Hunter College  
CSCI 395: Introduction to Data Science  
Professor Adrián Soto Cambres

## License
This project is licensed under the terms of the included LICENSE file.