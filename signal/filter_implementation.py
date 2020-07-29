import numpy as np

__all__ = ['ba_filter', '_sosfilt']

def ba_filter(b, a, sig):
    res = np.zeros(sig.size)
    # Use direct II transposed structure:
    for i in range(sig.size):
        tmp = 0.0
        for j in range(b.size):
            if i < j:
                continue
            tmp += b[j] * sig[i - j]
        for j in range(a.size):
            if i < j:
                continue
            tmp -= a[j] * res[i - j]
        tmp /= a[0]
        res[i] = tmp
    return res

def _sosfilt(sos, x, zi):
    # Modifies x and zi in place
    n_signals = x.shape[0]
    n_samples = x.shape[1]
    n_sections = sos.shape[0]
    b = sos[:, :3]
    # We ignore sos[:, 3] here because _validate_sos guarantees it's 1.
    a = sos[:, 4:]
    for i in range(n_signals):
        for n in range(n_samples):
            for s in range(n_sections):
                x_n = x[i, n]  # make a temporary copy
                # Use direct II transposed structure:
                x[i, n] = b[s, 0] * x_n + zi[i, s, 0]
                zi[i, s, 0] = (b[s, 1] * x_n - a[s, 0] * x[i, n] + zi[i, s, 1])
                zi[i, s, 1] = (b[s, 2] * x_n - a[s, 1] * x[i, n])
    return (x, zi)