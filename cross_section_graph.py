import numpy as np
import plotly.graph_objects as go
from utilities import load_value_function

goal = 100
j = 30

# Load reachability
filename = f"data/reachable/pig/goal_{goal}_opponent_score_30.json"
reachable = load_value_function(filename)

# Build 2D reachability matrix (k, i)
reachable_matrix = np.zeros((goal, goal)) 
for i in range(goal):
    for k in range(goal):
        reachable_matrix[k, i] = reachable.get((i, j, k), 0)

# Load value functions
V_hold = load_value_function("data/value_function/pig/hold_100.json")
V_roll = load_value_function("data/value_function/pig/roll_100.json")

# Build difference grid
grid = np.full((goal, goal, goal), np.nan)
for (i, j, k) in V_hold:
    if i < goal and j < goal and k < goal:
        grid[i, j, k] = V_roll[(i, j, k)] - V_hold[(i, j, k)]

# Extract policy boundary cross-section at j = 30 (and transpose)
cross_section = grid[:, 30, :]         
cross_section_transposed = cross_section.T 

# Create plot
fig = go.Figure()

# Add heatmap of reachable states
fig.add_trace(go.Heatmap(
    z=reachable_matrix,
    colorscale='Blues',
    colorbar=dict(title='Reachable'),  
    showscale=False,                   
    opacity=0.6,
    zmin=0,
    zmax=1,
    name='Reachable Region',           
    showlegend=False
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
    line_color='black',
    showscale=False,
    name='Optimal Policy Boundary', 
    showlegend=False
))

# Add the hold at 20 line
fig.add_trace(go.Scatter(x=[0, reachable_matrix.shape[1]-1],
    y=[20, 20],
    mode='lines',
    line=dict(color='grey', width=2, dash='dash'),
    name='Hold at 20 Policy',
    showlegend=False
))


# Reachable Region Key
fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', 
                         marker=dict(size=10, color='#617ba2', opacity=1), name='Reachable Region'))

# Boundary Key
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', 
                         line=dict(color='black', width=2), name='Policy Boundary'))

# Hold at 20 Key
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', 
                         line=dict(color='grey', width=2, dash='dash'), name='Hold at 20 Policy'))

# Layout
fig.update_layout(
    title=f"Reachable States and Policy Boundary at j = 30",
    xaxis_title='Player 1 Score (i)',
    yaxis_title='Turn Total (k)',
    width=800,
    height=700,
    legend=dict(
        x=1.02, y=1,
        bordercolor="black",
        borderwidth=1
    )
)

fig.show()
