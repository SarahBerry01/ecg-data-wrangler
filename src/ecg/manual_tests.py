import sys
import matplotlib.pyplot as plt
from utils import get_signal
from filters import apply_low_pass, apply_high_pass


def test_filtering():
    signal = get_signal(102)
    low_pass = apply_low_pass(signal)
    high_pass = apply_high_pass(signal)
    figure, ax = plt.subplots(3)
    ax[0].set_title("original")
    ax[1].set_title("low pass")
    ax[2].set_title("high pass")
    ax[0].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
    ax[1].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
    ax[2].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
    ax[0].plot(signal[:10000])
    ax[0].plot()
    ax[1].plot(low_pass[:10000])
    ax[2].plot(high_pass[:10000])
    plt.show()


if __name__ == '__main__':
    globals()[sys.argv[1]]()
