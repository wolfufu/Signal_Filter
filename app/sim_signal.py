import numpy as np
import matplotlib.pyplot as plt

from numba import njit, prange

@njit(parallel=True)
def parallel_arange(start, stop, step):
    n = int((stop - start) / step)
    arr = np.empty(n, dtype=np.float64)
    for i in prange(n):
        arr[i] = start + i * step
    return arr

def create_signal(freq: float = 5.0):
    np.random.seed(0)
    dt = 0.001
    Fs = 1 / dt               
    t = parallel_arange(0, 100, dt)  
    
    nse = np.random.randn(len(t))
    r = np.exp(-t / 0.05)
    cnse = np.convolve(nse, r)[:len(t)] * dt
    
    f_signal = freq            # частота сигнала (Гц)
    s = 0.1 * np.sin(2 * np.pi * f_signal * t) + cnse

    return t, s, Fs, dt, f_signal

def find_freq(s, dt):
    N = len(s)

    fft_vals = np.fft.fft(s)
    fft_abs = np.abs(fft_vals) / N * 2

    freqs = np.fft.fftfreq(N, d=dt)

    positive_freqs = freqs[:N//2]
    positive_amp = fft_abs[:N//2]

    positive_amp[0] = 0   # убираем постоянную составляющую

    idx_max = np.argmax(positive_amp)

    return positive_freqs[idx_max]


def draw_grafs(t, s, Fs):
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(7, 7))

    axs[0, 0].set_title("Signal")
    axs[0, 0].plot(t, s, color = 'C0')
    axs[0, 0].set_xlabel("Time")
    axs[0, 0].set_ylabel("Amplitude")

    axs[1, 0].set_title("Magnitude Spectrum")
    axs[1, 0].magnitude_spectrum(s, Fs=Fs, color='C1')

    axs[1, 1].set_title("Log. Magnitude Spectrum")
    axs[1, 1].magnitude_spectrum(s, Fs=Fs, scale='dB', color='C1')

    axs[2, 0].set_title("Phase Spectrum")
    axs[2, 0].magnitude_spectrum(s, Fs=Fs, color='C2')

    axs[2, 1].set_title("Angle Spectrum")
    axs[2, 1].magnitude_spectrum(s, Fs=Fs, color='C2')

    axs[0, 1].remove() 

    fig.tight_layout()
    plt.show()

"""
if __name__ == "__main__":
    t, s, Fs, dt, f_true = create_signal()
    f_detected = find_freq(s, dt)
    print(f"Заданная частота: {f_true} Гц, обнаруженная: {f_detected:.3f} Гц")
    draw_grafs(t, s)
"""