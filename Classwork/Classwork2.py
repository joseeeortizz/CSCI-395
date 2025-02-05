"""
Name: Jose Miguel Ortiz
Email: jose.ortiz60@lagcc.cuny.edu
Pod: 5th right
Date: 02/04/2025

"""

import pandas as pd

if __name__ == "__main__":

    input_file = input("Enter an input file name: ")
    output_file = input("Enter an output file name:  ")

    df = pd.read_csv(input_file)

    test_results = df[(df['Grade'] == 3) and (df['Year'] == 2019)]
    test_results.to_csv(output_file, index=False)

    print(f"Filtered data has been saved to {output_file}")
