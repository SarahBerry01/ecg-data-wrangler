import scipy.signal


# def butter(cutoff, fs, order, high_or_low):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = scipy.signal.butter(order, normal_cutoff, high_or_low)
#     return b, a

def bandpass(sig, low, high, fs):
    nyq = 0.5 * fs
    high = high / nyq
    low = low / nyq
    b, a = scipy.signal.butter(1, [low, high], btype='bandpass')
    y = scipy.signal.filtfilt(b, a, sig)
    return y


def apply_filters(sig):
    return bandpass(sig, 0.5, 45, 360)
    # return apply_low_pass(apply_high_pass(sig))
