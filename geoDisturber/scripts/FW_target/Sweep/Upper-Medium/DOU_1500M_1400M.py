#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: DOU_1500M_1400M
# GNU Radio version: 3.10.9.2

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
from gnuradio import radar
import DOU_1500M_1400M_change_sink as change_sink  # embedded python module
import time
import threading




class DOU_1500M_1400M(gr.top_block):

    def __init__(self, uri='192.168.1.11'):
        gr.top_block.__init__(self, "DOU_1500M_1400M", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.uri = uri

        ##################################################
        # Variables
        ##################################################
        self.hf_function_probe = hf_function_probe = 0
        self.freq_b = freq_b = 1422500000,1447500000
        self.freq_a = freq_a = 1492500000,1517500000,1542500000,1567500000,1592500000,1617500000
        self.bbb = bbb = 1
        self.atten_b = atten_b = 19.6,19.7
        self.atten_a = atten_a = 19.8,19.4,19.2,19.1,19.2,19.2
        self.aaa = aaa = 1
        self.true_en = true_en = change_sink.work(hf_function_probe,aaa, bbb, freq_a, freq_b, atten_a, atten_b, 1492500000,1,19.8)[1]
        self.loss = loss = 1.5
        self.atten = atten = change_sink.work(hf_function_probe,aaa, bbb, freq_a, freq_b, atten_a, atten_b, 1492500000,1,19.8)[2]
        self.SW_feq = SW_feq = 25000000
        self.SAMP = SAMP = 25000000
        self.LO_feq = LO_feq = change_sink.work(hf_function_probe,aaa, bbb, freq_a, freq_b, atten_a, atten_b, 1492500000,1,19.8)[0]
        self.BW = BW = 30000000

        ##################################################
        # Blocks
        ##################################################

        self.hf_probe_signal = blocks.probe_signal_c()
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(SAMP, (2**12), (2**12), 1, -SW_feq/2, SW_feq, 1, "packet_len")
        self.iio_fmcomms2_sink_0 = iio.fmcomms2_sink_fc32(uri, [true_en, true_en, not true_en, not true_en], 32768, True)
        self.iio_fmcomms2_sink_0.set_len_tag_key('')
        self.iio_fmcomms2_sink_0.set_bandwidth(BW)
        self.iio_fmcomms2_sink_0.set_frequency(LO_feq)
        self.iio_fmcomms2_sink_0.set_samplerate(SAMP)
        if true_en:
            self.iio_fmcomms2_sink_0.set_attenuation(0, atten-7+loss)
        if not true_en:
            self.iio_fmcomms2_sink_0.set_attenuation(1, atten-7+loss)
        self.iio_fmcomms2_sink_0.set_filter_params('Auto', '', 0, 0)
        def _hf_function_probe_probe():
          while True:

            val = self.hf_probe_signal.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_hf_function_probe,val))
              except AttributeError:
                self.set_hf_function_probe(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _hf_function_probe_thread = threading.Thread(target=_hf_function_probe_probe)
        _hf_function_probe_thread.daemon = True
        _hf_function_probe_thread.start()
        self.analog_sig_source_x_1 = analog.sig_source_c(10, analog.GR_CONST_WAVE, 0, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_1, 0), (self.hf_probe_signal, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.iio_fmcomms2_sink_0, 0))


    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def get_hf_function_probe(self):
        return self.hf_function_probe

    def set_hf_function_probe(self, hf_function_probe):
        self.hf_function_probe = hf_function_probe
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[0])
        self.set_atten(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[2])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[1])

    def get_freq_b(self):
        return self.freq_b

    def set_freq_b(self, freq_b):
        self.freq_b = freq_b
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[0])
        self.set_atten(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[2])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[1])

    def get_freq_a(self):
        return self.freq_a

    def set_freq_a(self, freq_a):
        self.freq_a = freq_a
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[0])
        self.set_atten(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[2])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[1])

    def get_bbb(self):
        return self.bbb

    def set_bbb(self, bbb):
        self.bbb = bbb
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[0])
        self.set_atten(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[2])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[1])

    def get_atten_b(self):
        return self.atten_b

    def set_atten_b(self, atten_b):
        self.atten_b = atten_b
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[0])
        self.set_atten(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[2])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[1])

    def get_atten_a(self):
        return self.atten_a

    def set_atten_a(self, atten_a):
        self.atten_a = atten_a
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[0])
        self.set_atten(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[2])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[1])

    def get_aaa(self):
        return self.aaa

    def set_aaa(self, aaa):
        self.aaa = aaa
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[0])
        self.set_atten(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[2])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.atten_a, self.atten_b, 1492500000,1,19.8)[1])

    def get_true_en(self):
        return self.true_en

    def set_true_en(self, true_en):
        self.true_en = true_en

    def get_loss(self):
        return self.loss

    def set_loss(self, loss):
        self.loss = loss
        self.iio_fmcomms2_sink_0.set_attenuation(0, self.atten-7+self.loss)
        self.iio_fmcomms2_sink_0.set_attenuation(1, self.atten-7+self.loss)

    def get_atten(self):
        return self.atten

    def set_atten(self, atten):
        self.atten = atten
        self.iio_fmcomms2_sink_0.set_attenuation(0, self.atten-7+self.loss)
        self.iio_fmcomms2_sink_0.set_attenuation(1, self.atten-7+self.loss)

    def get_SW_feq(self):
        return self.SW_feq

    def set_SW_feq(self, SW_feq):
        self.SW_feq = SW_feq

    def get_SAMP(self):
        return self.SAMP

    def set_SAMP(self, SAMP):
        self.SAMP = SAMP
        self.iio_fmcomms2_sink_0.set_samplerate(self.SAMP)

    def get_LO_feq(self):
        return self.LO_feq

    def set_LO_feq(self, LO_feq):
        self.LO_feq = LO_feq
        self.iio_fmcomms2_sink_0.set_frequency(self.LO_feq)

    def get_BW(self):
        return self.BW

    def set_BW(self, BW):
        self.BW = BW
        self.iio_fmcomms2_sink_0.set_bandwidth(self.BW)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--uri", dest="uri", type=str, default='192.168.1.11',
        help="Set uri [default=%(default)r]")
    return parser


def main(top_block_cls=DOU_1500M_1400M, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(uri=options.uri)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
