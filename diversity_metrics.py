import numpy as np
import scipy

TOTAL_DAYS = 50 # The total number of survey days. Hard-coded.
TOTAL_VALID_DAYS = 46 # The total number of valid survey days, as defined in data-cleaning.ipynb. Hard-coded.

# Possible: measure of abundance more closely related to actual bird count?
# These methods use the "Point Count Species" data

def abundance_days_seen(data, species):
    """
    Calculate abundance measured in number of days seen.

    Parameters:
        data: the data containing bird species and their counts
        species: the species for which we want to find abundance
    """
    species_subset = data[data['Species'] == species]
    return len(species_subset['Date'].unique())

def frequency_days_seen(data, species):
    """
    Calculate frequency measured in abundance divided by total number 
    of valid survey days.

    Parameters:
        data: the data containing bird species and their counts
        species: the species for which we want to find abundance
    """
    abundance = abundance_days_seen(data, species)
    return abundance / TOTAL_VALID_DAYS

def simpson_diversity(data, date):
    """
    Calculates Simpson's diversity for all the counts on a given day.
    Does not account for duplicate sightings of the same individual.

    Parameters:
        data: the data containing bird species and their counts
        date: the date for which we want to calculate Simpson diversity
    """
    counts_from_date = data[data['Date'] == date][['Species', '# Individuals']]
    date_species_groups = counts_from_date.groupby("Species").agg(sum)

    N = np.sum(counts_from_date["# Individuals"])

    # Helper function.
    def _summation_term(n):
        return (n*(n-1))/(N*(N-1))

    date_species_groups['simpson_temp'] = date_species_groups[["# Individuals"]].apply(_summation_term)
    return 1 - np.sum(date_species_groups["simpson_temp"])

def shannon_diversity(data, date):
    """
    Calculates Shannon diversity for all the counts on a given day.
    Does not account for duplicate sightings of the same individual.

    Parameters:
        data: the data containing bird species and their counts
        date: the date for which we want to calculate Simpson diversity
    """
    counts_from_date = data[data['Date'] == date][['Species', '# Individuals']]
    date_species_groups = counts_from_date.groupby("Species").agg(sum)

    N = np.sum(counts_from_date["# Individuals"])

    date_species_groups['shannon_props'] = date_species_groups[['# Individuals']]/N
    return scipy.stats.entropy(pk = date_species_groups["shannon_props"])

# Alpha Diversity
def alpha_diversity(data, date):
    """
    Calculates Alpha diversity as 1/D (as per Schultz et al., 2012) for all the 
    counts on a given day.
    Does not account for duplicate sightings of the same individual.

    Parameters:
        data: the data containing bird species and their counts
        date: the date for which we want to calculate Alpha diversity
    """
    d = simpson_diversity(data, date)
    if d != 0:
        return 1/d

# Beta Diversity
def beta_diversity(data, date1, date2):
    """
    Calculates Beta diversity as described here: https://www.int-res.com/articles/meps/9/m009p147.pdf
    for all the counts on two different days.  
    Does not account for duplicate sightings of the same individual.

    Parameters:
        data: the data containing bird species and their counts
        date1: the first date for which we want to calculate Beta diversity
        date2: the second date for which we want to calculate Beta diversity
    """
    date1_data = data[data['Date'] == date1]
    date1_data = date1_data[['Species', '# Individuals']]

    date2_data = data[data['Date'] == date2]
    date2_data = date2_data[['Species', '# Individuals']]

    sp_counts = date1_data.merge(date2_data, on = 'Species', how = 'outer').fillna(0)

    numerator = 0
    denominator = 0

    for row in sp_counts.iterrows():
        numerator += min(row['# Individuals_x'], row['# Individuals_y'])
        denominator += row['# Individuals_x'] + row['# Individuals_y']

    return (2 * numerator) / denominator
