"""
Name: Jose Miguel Ortiz
Email: jose.ortiz60@lagcc.cuny.edu
Pod: 4th left5th left
Date: 01/30/2025
Description: make a function make_dict.

"""

from fileinput import filename

if __name__ == '__main__':

    def make_dict(filename, sep=":  "):
        dictionary = {}
        with open(filename) as f:
            for line in f:
                value, key = line.strip().split(sep)
                dictionary[key] = value
        return dictionary