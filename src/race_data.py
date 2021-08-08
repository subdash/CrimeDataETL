import pandas as pd

"""
Demographic data:
https://en.wikipedia.org/wiki/Demographics_of_the_United_States#Race
https://www.census.gov/prod/2002pubs/censr-4.pdf
"""

population_by_demographic = {
    1980: pd.DataFrame({
        "White": 83.0,
        "Black": 11.7,
        "American Indian": 0.8,
        "Asian": 1.5
    }, index=[0]),

    1990: pd.DataFrame({
        "White": 80.3,
        "Black": 12.1,
        "American Indian": 0.8,
        "Asian": 2.9
    }, index=[0]),

    2000: pd.DataFrame({
        "White": 75.1,
        "Black": 12.3,
        "American Indian": 0.9,
        "Asian": 5.5
    }, index=[0]),

    2010: pd.DataFrame({
        "White": 72.4,
        "Black": 12.6,
        "American Indian": 0.9,
        "Asian": 6.2
    }, index=[0])
}
