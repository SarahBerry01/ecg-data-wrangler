import scipy.signal


def butter(cutoff, fs, order, high_or_low):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, high_or_low)
    return b, a


def apply_low_pass(sig):
    order = 10
    cutoff = 45
    fs = 360
    b, a = butter(cutoff, fs, order, "lowpass")
    y = scipy.signal.filtfilt(b, a, sig)
    return y


def apply_high_pass(sig):
    order = 3
    cutoff = 0.08
    fs = 360
    b, a = butter(cutoff, fs, order, "highpass")
    y = scipy.signal.filtfilt(b, a, sig)
    return y


def apply_filters(sig):
    return apply_low_pass(apply_high_pass(sig))
