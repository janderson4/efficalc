import try_axis
import get_error_ecc

delta = 1e-8  # small change to be used for finite differences


# this function is the same as "change" except that it finds a direction for
# eccentricity rather than for c
def change(col, guess, target, output):
    error = get_error_ecc.get_error(output, target)
    # A small positive value "delta" is added to both inputs in order to test
    # the effect on the results of "try_axis". It may have to be negative for
    # theta to avoid exceeding 0.
    delta0 = delta if guess[0] < -delta else -delta

    output2 = try_axis.try_axis(col, guess[0] + delta0, guess[1])
    a = (output2[0] - output[0]) / delta0
    c = (output2[1] - output[1]) / delta0

    output2 = try_axis.try_axis(col, guess[0], guess[1] + delta)
    b = (output2[0] - output[0]) / delta
    d = (output2[1] - output[1]) / delta

    e = target[0] - output[0]
    f = target[1] - output[1]

    change = [0] * 2
    det = a * d - b * c

    # avoid divide by zero
    if det != 0:
        # set the planned changes in theta and c to try to reach the point at
        # which lambda and load are both their target values
        change[0] = (d * e - b * f) / det
        change[1] = (a * f - c * e) / det
    return change, error
