# --------------- The python file for HOST PC of SYSTEM ---------------- #
# Step one ) Receive the signal using 4 rx ports.
# Step two ) Calculate and Compair the recieved power between four rx    #
# 			 ports.
# Step thr ) Select a device that received bigger power.
# Step fou ) Calculate the phase difference value between two ports on   #
# 			 Selected device.
# Step fiv ) Transfer the sinosodier signal with calculated phase diffe- #
#			 rence using two ports on selected Devices.
# Required Values that phase difference between two receiver ports on    #
# one device.
# ---------------------------------------------------------------------- #

# ------------------ Import the libraries for this code ---------------- #
import adi
import time
import math
import numpy as np
import matplotlib.pyplot as plt

# ------------------ The values for initial each ports ----------------- #
offset = 4.73
# ------------------        Generate Signal Date       ----------------- #


# ------------------         Signal Processing         ----------------- #
def hanning (N):
		w = [0]*N
		for m in range(N):
				w[m] = 0.5*(1-np.cos(2*np.pi*(m/N)))
		return w
def fft (sig):
		fft_sig = np.fft.fft(sig)
		return fft_sig
def signal_process(sig0, sig1, offset): # phase : phase difference value !!!
		#	Remove the DC component of the signal
		sig0 = sig0 - np.mean(sig0)
		sig1 = sig1 - np.mean(sig1)
		#	Calculate signal's length
		len_sig0 = len(sig0)
		len_sig1 = len(sig1)
		#	Generate Window
		win0 = hanning(len_sig0)
		win1 = hanning(len_sig1)
		#	FFT
		sig0 = fft(sig0*win0)
		sig1 = fft(sig1*win1)
		#	Detect fundamental frequency
		sig0_max = np.max(abs(sig0))
		sig1_max = np.max(abs(sig1))
		sig0_location = np.where(abs(sig0)==sig0_max)
		sig1_location = np.where(abs(sig1)==sig1_max)
		sig0_location = sig0_location[0][0]
		sig1_location = sig1_location[0][0]
		#	Calculate Phase difference beween two tx ports on one board
		phase = np.angle(sig0[sig0_location])-(np.angle(sig1[sig1_location])+offset)
		phase = (phase + 2*np.pi)%(2*np.pi)
		#	Amplitude
		amp0 = np.abs(sig0[sig0_location])
		amp1 = np.abs(sig1[sig1_location])
		return phase, amp0, amp1


# ------------------          Devices setting          ----------------- #
dev = adi.ad9361(uri="ip:192.168.3.1")

samp_rate = 2000000
buf_size = 10000
freq = 2400000000
rf_bw = 2000000
dev.sample_rate = int(samp_rate)

# Setting for receiveri
dev.rx_lo = int(freq)
dev.rx_rf_bandwidth = int(rf_bw)
dev.rx_buffer_size = int(buf_size)
#	Setting for rx channelsi
dev.rx_enabled_channels = [0,1]
#dev.gain_control_mode_chan0 = 'fast_attack'
#dev.gain_control_mode_chan1 = 'fast_attack'
dev.gain_control_mode_chan0 = 'manual'
dev.gain_control_mode_chan1 = 'manual'
#dev2.gain_control_mode_chan0 = 'manual'
#dev2.gain_control_mode_chan1 = 'manual'
dev.hardwaregain_chan0 = 55
dev.hardwaregain_chan1 = 60
#dev2.hardwaregain_chan0 = 64
#dev2.hardwaregain_chan1 = 64

# Setting for transceiver
dev.tx_lo = int(freq)
dev.tx_rf_bandwidth = int(rf_bw)
dev.tx_buffer_size = int(buf_size)
#	Setting for tx channels
dev.tx_enabled_channels = [0,1]
dev.tx_hardwaregain_chan0 =-30
dev.tx_hardwaregain_chan1 =-30

    
def receive():
    for i in range(8):
        data = dev.rx()
    phase, amp0, amp1 = signal_process(data[0], data[1], offset)
    a_data = np.real(data[0])
    b_data = np.real(data[1])
    plt.plot(a_data)
    plt.plot(b_data)
    plt.show()
    print(phase)
    #+dif_dev1_rx)


cent_freq = int(10000)
amp = 2**14
ts = float(1/samp_rate)
t = np.arange(0, samp_rate*ts, ts)
I = amp * np.cos(2*np.pi*cent_freq*t+0.0)
Q = amp * np.sin(2*np.pi*cent_freq*t+0.0)
sig = 1*I + 1j*Q
I = amp * np.cos(2*np.pi*cent_freq*t+1.53)
Q = amp * np.sin(2*np.pi*cent_freq*t+1.53)
sig1 = 1*I + 1j*Q
#for i in range(time):
while True:
    dev.tx([sig, sig1])
#receive()

dev.tx_destroy_buffer()
