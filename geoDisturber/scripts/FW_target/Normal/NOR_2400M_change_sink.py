import time
import threading

#global current_channel
current_channel = 'A'
#global last_switch_time1
last_switch_time1 = time.time()
#global last_switch_time2
last_switch_time2 = time.time()
#global counter
counter = 0
first_flag = 1
print(f"INIT.............................................")  

def work(prob_level,enable_a, enable_b, freq_a, freq_b, temp1, temp2): 
    global current_channel, last_switch_time1, last_switch_time2, counter, first_flag, LO_freq, true_en
    if first_flag:
        LO_freq = temp1
        true_en = temp2
        first_flag = 0
    if prob_level:
        #print(f"####################param1: {LO_freq}, param2: {enable_a}, param3: {enable_b}") 
        current_time = time.time()
        #print(f"OK")  
        #print(f"param1: {current_time}")  
        #print(f"time1: {last_switch_time1}") 
        #print(f"time2: {last_switch_time2}") 
        if current_time - last_switch_time1 > 0.01:
            if enable_a and not enable_b:
                LO_freq = freq_a[counter]
                counter = (counter + 1) % len(freq_a)
                true_en = True
            elif enable_b and not enable_a:
                LO_freq = freq_b[counter]
                counter = (counter + 1) % len(freq_b)
                true_en = False
            elif enable_a and enable_b:
                if current_time - last_switch_time2 > 10:
                    if current_channel == 'A':
                        true_en = False
                        last_switch_time2 = current_time
                        current_channel = 'B'
                    elif current_channel == 'B':
                        true_en = True
                        last_switch_time2 = current_time
                        current_channel = 'A'
                #print(f"param1: {current_channel}") 
                active_freqs = freq_a if true_en else freq_b
                #print(f"param1: {active_freqs}")  
                if counter > len(active_freqs) - 1:
                    counter = 0
                LO_freq = active_freqs[counter]
                counter = (counter + 1) % len(active_freqs) 
            last_switch_time1 = current_time
    out = [LO_freq, true_en]
    return out
