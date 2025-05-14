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

#######################################
# Need to access Jimmy's code
import numpy as np
import plotly.graph_objects as go
from utilities import load_value_function

goal = 100
j = 30

# Load reachability
filename = f"data/reachable/pig/goal_{goal}_opponent_score_{j}.json"
reachable = load_value_function(filename)

# Build 2D reachability matrix (k, i)
reachable_matrix = np.zeros((goal, goal))  # shape (k, i)
for i in range(goal):
    for k in range(goal):
        reachable_matrix[k, i] = reachable.get((i, j, k), 0)

# Load value functions
V_hold = load_value_function("data/value_function/pig/hold_100.json")
V_roll = load_value_function("data/value_function/pig/roll_100.json")

# Build difference grid
grid = np.full((goal, goal, goal), np.nan)
for (i_, j_, k_) in V_hold:
    if i_ < goal and j_ < goal and k_ < goal:
        grid[i_, j_, k_] = V_roll[(i_, j_, k_)] - V_hold[(i_, j_, k_)]

# Extract policy boundary cross-section at j = 30
cross_section = grid[:, j, :]         # shape (i, k)
cross_section_transposed = cross_section.T  # shape (k, i)

# Create plot
fig = go.Figure()

# Add heatmap of reachable states
fig.add_trace(go.Heatmap(
    z=reachable_matrix,
    colorscale='Blues',
    colorbar=dict(title='Reachable'),
    showscale=True,
    opacity=0.6,
    zmin=0,
    zmax=1
))

# Add policy boundary as contour at value = 0
fig.add_trace(go.Contour(
    z=cross_section_transposed,
    contours=dict(
        start=0, end=0, size=1,
        coloring='none',
        showlabels=False
    ),
    line_width=2,
    line_color='red',
    showscale=False
))

# Layout
fig.update_layout(
    title=f"Reachable States and Policy Boundary at j = {j}",
    xaxis_title='i (player score)',
    yaxis_title='k (turn total)',
    width=800,
    height=700
)

fig.show()
