from scipy.optimize import linear_sum_assignment


def solve_assignment(score_matrix: list[list[float]]) -> tuple[list[int], list[int]]:
    # Hungarian minimizes cost, so negate similarity matrix.
    row_idx, col_idx = linear_sum_assignment([[-v for v in row] for row in score_matrix])
    return row_idx.tolist(), col_idx.tolist()
