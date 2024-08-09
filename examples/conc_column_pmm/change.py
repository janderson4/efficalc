import try_axis
import get_error

delta = 1e-8  # small change to be used for finite differences


def change(col, guess, target, output):
    error = get_error.get_error(output, target, col.load_span)
    # A small positive value "delta" is added to both inputs in order to test
    # the effect on the results of "try_axis". It may have to be negative for
    # theta to avoid exceeding 0.
    delta0 = delta if guess[0] < -delta else -delta

    output2 = try_axis.try_axis(col, guess[0] + delta0, guess[1])
    a = (output2[0] - output[0]) / delta0
    c = (output2[3] - output[3]) / delta0

    output2 = try_axis.try_axis(col, guess[0], guess[1] + delta)
    b = (output2[0] - output[0]) / delta
    d = (output2[3] - output[3]) / delta

    e = target[0] - output[0]
    f = target[1] - output[3]

    change = [0] * 2
    det = a * d - b * c

    # avoid divide by zero
    if det != 0:
        # set the planned changes in theta and c to try to reach the point at
        # which lambda and load are both their target values
        change[0] = (d * e - b * f) / det
        change[1] = (a * f - c * e) / det
    return change, error