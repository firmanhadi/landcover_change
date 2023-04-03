# Code created with the help of ChatGPT
import numpy as np
from osgeo import gdal

# Load the first raster in the time series
ds = gdal.Open('lc17.tif')
band = ds.GetRasterBand(1)
data = band.ReadAsArray().astype(np.int32)

# Define the categories
categories = [1, 2, 3, 4, 5]

# Create a transition matrix for the first time step
transition_matrix = np.zeros((len(categories), len(categories)))
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if i == 0 or j == 0:
            continue
        current_category = data[i, j]
        previous_category = data[i-1, j-1]
        if current_category in categories and previous_category in categories:
            transition_matrix[categories.index(previous_category)][categories.index(current_category)] += 1

# Calculate the transition probabilities
row_sums = transition_matrix.sum(axis=1)
transition_probability_matrix = np.zeros_like(transition_matrix)
for i in range(len(categories)):
    if row_sums[i] != 0:
        transition_probability_matrix[i,:] = transition_matrix[i,:] / row_sums[i]

# Load the second raster in the time series
ds = gdal.Open('lc21.tif')
band = ds.GetRasterBand(1)
data = band.ReadAsArray().astype(np.int32)

# Update the transition matrix for the second time step
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if i == 0 or j == 0:
            continue
        current_category = data[i, j]
        previous_category = data[i-1, j-1]
        if current_category in categories and previous_category in categories:
            transition_matrix[categories.index(previous_category)][categories.index(current_category)] += 1

# Calculate the transition probabilities for the second time step
row_sums = transition_matrix.sum(axis=1)
transition_probability_matrix = np.zeros_like(transition_matrix)
for i in range(len(categories)):
    if row_sums[i] != 0:
        transition_probability_matrix[i,:] = transition_matrix[i,:] / row_sums[i]

# Save the transition probability matrix as a CSV file
np.savetxt('transition_probability_matrix_2017_2021.csv', transition_probability_matrix, delimiter=',')
