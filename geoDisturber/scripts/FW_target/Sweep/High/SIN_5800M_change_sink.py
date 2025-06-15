import time
import threading


current_channel = 'A'
last_switch_time1 = time.time()
last_switch_time2 = time.time()
counter = 0
first_flag = 1
print(f"INIT.............................................")  

def work(prob_level,enable_a, enable_b, freq_a, freq_b, atten_a, atten_b, temp1, temp2, temp3): 
    global current_channel, last_switch_time1, last_switch_time2, counter, first_flag, LO_freq, true_en, atten
    if first_flag:
        LO_freq = temp1
        true_en = temp2
        atten = temp3
        first_flag = 0
    if prob_level:
        current_time = time.time()
        if current_time - last_switch_time1 > 0.01:
            if enable_a and not enable_b:
                LO_freq = freq_a[counter]
                atten = atten_a[counter]
                counter = (counter + 1) % len(freq_a)
                true_en = True
            elif enable_b and not enable_a:
                LO_freq = freq_b[counter]
                atten = atten_b[counter]
                counter = (counter + 1) % len(freq_b)
                true_en = False
            elif enable_a and enable_b:
                if current_time - last_switch_time2 > 60:
                    if current_channel == 'A':
                        true_en = False
                        last_switch_time2 = current_time
                        current_channel = 'B'
                    elif current_channel == 'B':
                        true_en = True
                        last_switch_time2 = current_time
                        current_channel = 'A'
                active_freqs = freq_a if true_en else freq_b
                active_atten = atten_a if true_en else atten_b
                if counter > len(active_freqs) - 1:
                    counter = 0
                LO_freq = active_freqs[counter]
                atten = active_atten[counter]
                counter = (counter + 1) % len(active_freqs) 
            last_switch_time1 = current_time
    out = [LO_freq, true_en, atten]
    return out
