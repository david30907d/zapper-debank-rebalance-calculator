import cvxpy as cp
import numpy as np

# Number of LP pairs
num_pairs = 6

# Define the desired weights (market cap weights scaled by All Weather portfolio allocations)
# For each token, the desired weight is the sum of weights across all LP pairs it appears in
desired_weights = np.array([0.7, 0.1, 0.2, 0.2, 0.15, 0.15, 0.1, 0.1])

# Normalize desired_weights
desired_weights = desired_weights / np.sum(desired_weights)

# Define the LP pairs and their categories
# Tokens 0-1, 0-2, and 0-3 form LP pairs in the first category, and tokens 4-5 and 6-7 form LP pairs in the second category
lp_pairs_categories = [[[0, 1], [0, 2], [0, 3]], [[0, 1], [4, 5], [6, 7]]]

# Define the category weights
category_weights = [0.7, 0.3]

# Create a variable for each LP pair's weight
lp_weights = cp.Variable(num_pairs)

# Flatten the LP pairs for the enumeration
lp_pairs_flat = [pair for sublist in lp_pairs_categories for pair in sublist]

# Set up the objective function: minimize the sum of squared differences between desired and actual weights
# The actual weight of a token is the sum of weights of all LP pairs it appears in
objective = cp.Minimize(
    sum(
        [
            cp.sum_squares(
                desired_weights[token]
                - cp.sum(
                    [
                        lp_weights[i]
                        for i, lp_pair in enumerate(lp_pairs_flat)
                        if token in lp_pair
                    ]
                )
            )
            for token in range(len(desired_weights))
        ]
    )
)

# Set up the constraints: the sum of the weights of the LP pairs in each category equals the category weight,
# each LP pair has equal weights for the two tokens, and all weights are non-negative
constraints = [
    cp.sum(
        [
            lp_weights[i]
            for i, lp_pair in enumerate(lp_pairs_flat)
            if lp_pair in lp_pairs_category
        ]
    )
    == category_weight
    for lp_pairs_category, category_weight in zip(lp_pairs_categories, category_weights)
]
constraints += [
    lp_weights[i] == lp_weights[j]
    for i in range(num_pairs)
    for j in range(i + 1, num_pairs)
    if any(token in lp_pairs_flat[i] for token in lp_pairs_flat[j])
]
constraints += [lp_weights >= 0]

# Define and solve the problem
problem = cp.Problem(objective, constraints)
problem.solve()

# The optimal weights are stored in the 'lp_weights.value' attribute
optimal_weights = lp_weights.value

# Normalize optimal_weights
optimal_weights = optimal_weights / np.sum(optimal_weights)

# Print the optimal weights
print(optimal_weights)
