### 2D cross-section graph (j=30)
import numpy as np
import plotly.graph_objects as go
from utilities import load_value_function

goal = 100

# Load raw value function from JSON
filename_hold = "data/value_function/pig/hold_100.json"
V_hold = load_value_function(filename_hold)

filename_roll = "data/value_function/pig/roll_100.json"
V_roll = load_value_function(filename_roll)


### 3D boundary graph
# Create 3D grid for each possible state
grid = np.full((goal, goal, goal), np.nan)

# Store the difference in value between holding and rolling for each (i,j,k)
for (i, j, k) in V_hold:
    if i < goal and j < goal and k < goal:
        grid[i, j, k] = V_roll[(i, j, k)] - V_hold[(i, j, k)]


# Extract cross-section at j = 30
cross_section = grid[:, 30, :]  

# Transpose so i is on x-axis, k is on y-axis
cross_section_transposed = cross_section.T  

# Plot contour at value = 0 (i.e. where policy changes from roll to hold)
fig = go.Figure(data=go.Contour(
    z=cross_section_transposed,
    contours=dict(
        start=0, end=0, size=1,
        coloring='none',
        showlabels=False
    ),
    line_width=2,
    showscale=False
))

fig.update_layout(
    title='Policy Boundary at j = 30',
    xaxis_title='i',
    yaxis_title='k',
    width=700,
    height=600
)

fig.show()

