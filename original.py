import numpy as np
import matplotlib.pyplot as plt

Fs = 500
T = 1/Fs
t = np.arange(0, 1, T)

f1 = 10
f2 = 15
f3 = 20
signal = (0.7*np.sin(2*np.pi*f1*t) +
          1.0*np.sin(2*np.pi*f2*t) +
          3.0*np.cos(2*np.pi*f3*t))

fft_values_raw = np.fft.fft(signal)
threshold = 0.05 * np.max(np.abs(fft_values_raw))
fft_values = fft_values_raw.copy()

fft_values[np.abs(fft_values) < threshold] = 0
N = len(signal)

freq = np.fft.fftfreq(N, T)

noise_threshold = 0.01
magnitude = (2 / N) * np.abs(fft_values)
phase = np.angle(fft_values, True)

recreated = np.zeros(len(t), dtype=float)
stacked_freq_domain = np.column_stack((freq, magnitude, phase))
for entry in stacked_freq_domain[:N//2]:
    freq_point, mag_point, phase_point = entry
    recreated += mag_point*np.cos(2*np.pi*freq_point*t + phase_point)

plt.subplot(3, 2, 1)
plt.plot(t, signal)
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(3, 2, 2)
plt.stem(freq[:N//2], magnitude[:N//2])
plt.title('Frequency Domain (Magnitude Spectrum)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')

plt.subplot(3, 2, 3)
plt.stem(freq[:N//2], phase[:N//2])
plt.title('Phase')
plt.xlabel('Phase')
plt.ylabel('Angle [deg]')

plt.subplot(3, 2, 4)
plt.plot(t, recreated)
plt.title('Recreated Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(3, 2, 5)
plt.plot(t, np.absolute(signal - recreated))
plt.title('Error')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
