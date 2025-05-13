import numpy as np
import plotly.graph_objects as go

goal = 100

# Create 3D grid for each possible state
grid = np.full((goal, goal, goal), np.nan)

# Store the difference in value between holding and rolling for each (i,j,k)
for (i, j, k) in V_hold:
    if i < goal and j < goal and k < goal:
        grid[i, j, k] = V_roll[(i, j, k)] - V_hold[(i, j, k)]

# Prepare axis ranges
X, Y, Z = np.meshgrid(np.arange(goal), np.arange(goal), np.arange(goal), indexing='ij')

# Replace NaNs with -1 to make it work
safe_grid = np.nan_to_num(grid, nan=-1.0)

# Create the surface plot
fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=safe_grid.flatten(),
    isomin=0,
    isomax=0,
    surface_count=1,
    colorscale="Viridis",
    caps=dict(x_show=False, y_show=False, z_show=False),
    showscale=False
))

fig.update_layout(
    title='Roll/hold boundary for optimal Pig policy',
    scene=dict(
        xaxis_title='Player 1 Score (i)',
        yaxis_title='Player 2 Score (j)',
        zaxis_title='Turn Score (k)'
    )
)

fig.show()