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
import keyboard # Need to run this program with sudo or on sudo su



# ------------------         Plot Received Data        ----------------- #
def plot(sig0, sig1):
    a = np.real(sig0)
    b = np.real(sig1)
    plt.plot(a)
    plt.plot(b)
    plt.show()

# ------------------ The values for initial each ports ----------------- #
dif_dev1_rx = 4.73
dif_dev1_tx = 1.5
dif_dev2_rx = 4.6
dif_dev2_tx = 1.53

# ------------------        Generate Signal Date       ----------------- #
def gen_sig (phase):
	cent_freq = int(10000)
	amp = 2**14
	ts = float(1/2000000)
	t = np.arange(0, 2000000*ts, ts)
	I = amp * np.cos(2*np.pi*cent_freq*t+phase)
	Q = amp * np.sin(2*np.pi*cent_freq*t+phase)
	sig = 1*I + 1j*Q
	return sig

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
		phase = np.angle(sig0[sig0_location]-(sig1[sig1_location])+offset)
		#	Amplitude
		amp0 = np.abs(sig0[sig0_location])
		amp1 = np.abs(sig1[sig1_location])
		return phase, amp0, amp1

# ------------------               Transfer	           ----------------- #
#def trans ():

# ------------------               Receive             ----------------- #


# ------------------          Devices setting          ----------------- #
dev1 = adi.ad9361(uri="ip:192.168.2.1")
dev2 = adi.ad9361(uri="ip:192.168.3.1")

samp_rate = 2000000
buf_size = 10000
freq = 2400000000
rf_bw = 1000000
dev1.sample_rate = int(samp_rate)
dev2.sample_rate = int(samp_rate)

# Setting for receiveri
dev1.rx_lo = int(freq)
dev2.rx_lo = int(freq)
dev1.rx_rf_bandwidth = int(rf_bw)
dev2.rx_rf_bandwidth = int(rf_bw)
dev1.rx_buffer_size = int(buf_size)
dev2.rx_buffer_size = int(buf_size)
#	Setting for rx channelsi
dev1.rx_enabled_channels = [0,1]
dev2.rx_enabled_channels = [0,1]
#dev1.gain_control_mode_chan0 = 'fast_attack'
#dev1.gain_control_mode_chan1 = 'fast_attack'
#dev2.gain_control_mode_chan0 = 'fast_attack'
#dev2.gain_control_mode_chan1 = 'fast_attack'
dev1.gain_control_mode_chan0 = 'manual'
dev1.gain_control_mode_chan1 = 'manual'
dev2.gain_control_mode_chan0 = 'manual'
dev2.gain_control_mode_chan1 = 'manual'
dev1.hardwaregain_chan0 = 64
dev1.hardwaregain_chan1 = 64
dev2.hardwaregain_chan0 = 50
dev2.hardwaregain_chan1 = 50

# Setting for transceiver
dev1.tx_lo = int(freq)
dev2.tx_lo = int(freq)
dev1.tx_rf_bandwidth = int(rf_bw)
dev2.tx_rf_bandwidth = int(rf_bw)
dev1.tx_buffer_size = int(buf_size)
dev2.tx_buffer_size = int(buf_size)
dev1.tx_cyclic_buffer = False
dev2.tx_cyclic_buffer = False
#	Setting for tx channels
dev1.tx_enabled_channels = [0,1]
dev2.tx_enabled_channels = [0,1]
dev1.tx_hardwaregain_chan0 =-30
dev1.tx_hardwaregain_chan1 =-30
dev2.tx_hardwaregain_chan0 =-30
dev2.tx_hardwaregain_chan1 =-30


# ------------------        Complete All Setting       ----------------- #
print("# --------------- Strat Program --------------- #")
#while True:
print("# ------------- Select What to do ------------- #")
print("# MODE A: Receive")
print("# MODE B: Transive(Default)")
print("# MODE C: Transivce(With Phase difference value")
print("# MODE D: Plot Recieve Data")
print("# MODE E: Calculate phase difference Value")
print("# MODE F: Auto Step mode")
print("# MODE O: EXIT")
mode = input("Enter mode num: ")


if (mode == "A"):
	print("O")
elif (mode == "O"):
	print("O")
	
elif(mode == "O"):
	print("No mode... Enter again")

elif (mode == "F"):
    stack = input("Push ENTER after Setting!!!")
    print("!!! Receiving !!!")
    for i in range(8):
        rx_dev1 = dev1.rx()
        rx_dev2 = dev2.rx()
    plot(rx_dev1[0], rx_dev2[0])
    print("!!! Calculate !!!")
    dev1_phase, dev1_1_pow, dev1_2_pow = signal_process(rx_dev1[0], rx_dev1[1], dif_dev1_rx)
    dev2_phase, dev2_1_pow, dev2_2_pow = signal_process(rx_dev2[0], rx_dev2[1], dif_dev2_rx)
    print("Dev1 power: ", dev1_1_pow, ", Dev2 power: ", dev2_1_pow)
    if (dev1_1_pow >=dev2_1_pow):
        print("!----- Select dev1 -----!")
        sel_dev = 1
        plot(rx_dev1[0], rx_dev1[1])
    else:
        print("!----- Select dev2 -----!")
        sel_dev = 2
        plot(rx_dev2[0], rx_dev2[1])
    stack = input("Push ENTER after Setting!!!")
    print("!!! Beamforming Start !!!")
    print("!!! If you want to stop transmit, press q!!!")
    if (sel_dev == 1):
        sig_dev1_1 = gen_sig(0.0)
        sig_dev1_2 = gen_sig(dif_dev1_tx+dev1_phase)
        while True:
            if keyboard.is_pressed("q"):
                print("\n!!! Stop trans using dev 1!!!")
                break
            else:
                dev1.tx([sig_dev1_1, sig_dev1_2])
        print("Start Transfer on Default mode, press 'w' if you want get out!!!")
        while True:
            if keyboard.is_pressed('w'):
                print("STOP!!!!!!!!!!")
                break
            else:
                dev1.tx([sig_dev1_1, sig_dev1_2])
    else:
        sig_dev2_1 = gen_sig(0.0)
        sig_dev2_2 = gen_sig(dif_dev2_tx+dev2_phase)
        while True:
            if keyboard.is_pressed('q'):
                print("\n!!! Stop trans using dev 2!!!")
                break
            else:
                dev2.tx([sig_dev2_1, sig_dev2_2])
        print("Start Transfer on Default mode, press 'w' if you want get out!!!")
        while True:
            if keyboard.is_pressed('w'):
                print("STOP!!!!!!!!!!")
                break
            else:
                dev2.tx([sig_dev2_1, sig_dev2_2])

    stack = input("press Enter if you want transfer on default mode!!!!")
    sig_dev1_1 = gen_sig(0.0)
    sig_dev1_2 = gen_sig(0.0+dif_dev1_tx)
    sig_dev2_1 = gen_sig(0.0)
    sig_dev2_2 = gen_sig(0.0+dif_dev2_tx)

# --------------------    Calculate recieved data    ------------------- #

elif (mode == "O"):
		print("Shutting now... Please wait...")
		dev1.close()
		dev2.close()
		print("!!! Exit program !!!")
		print("!!! GOOD BYE~ !!!")
else:
		print("No mode... Enter again")

# -------------------- Start Transfer with phase val ------------------- #

# -------------------- Generate Transfer signal data ------------------- #

# -------------------- Generate Transfer signal data ------------------- #

# -------------------- Generate Transfer signal data ------------------- #

