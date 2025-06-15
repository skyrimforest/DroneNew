#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CUSTOM_2400M
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
import CUSTOM_2400M_change_sink as change_sink  # embedded python module
import CUSTOM_2400M_receive_para as receive_para  # embedded python module
import time
import threading




class CUSTOM_2400M(gr.top_block):

    def __init__(self, END_1=2500000000, START_1=2400000000, uri='192.168.1.13'):
        gr.top_block.__init__(self, "CUSTOM_2400M", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.END_1 = END_1
        self.START_1 = START_1
        self.uri = uri

        ##################################################
        # Variables
        ##################################################
        self.default = default = 2450000000
        self.hf_function_probe = hf_function_probe = 0
        self.freq_b = freq_b = default
        self.freq_a = freq_a = receive_para.work(START_1,END_1)[1]
        self.bbb = bbb = 0
        self.aaa = aaa = 1
        self.true_en = true_en = change_sink.work(hf_function_probe,aaa, bbb, freq_a, freq_b, freq_a[0],1)[1]
        self.SW_feq = SW_feq = receive_para.work(START_1,END_1)[0]
        self.SAMP = SAMP = receive_para.work(START_1,END_1)[0]
        self.LO_feq = LO_feq = change_sink.work(hf_function_probe,aaa, bbb, freq_a, freq_b, freq_a[0],1)[0]
        self.BW = BW = receive_para.work(START_1,END_1)[0]

        ##################################################
        # Blocks
        ##################################################

        self.hf_probe_signal = blocks.probe_signal_c()
        self.radar_signal_generator_fmcw_c_0 = radar.signal_generator_fmcw_c(SAMP, (2**14), (2**14), 1, -SW_feq/2, SW_feq, 1, "packet_len")
        self.iio_fmcomms2_sink_0 = iio.fmcomms2_sink_fc32(uri, [true_en, true_en, not true_en, not true_en], 32768, True)
        self.iio_fmcomms2_sink_0.set_len_tag_key('')
        self.iio_fmcomms2_sink_0.set_bandwidth(BW)
        self.iio_fmcomms2_sink_0.set_frequency(LO_feq)
        self.iio_fmcomms2_sink_0.set_samplerate(SAMP)
        if true_en:
            self.iio_fmcomms2_sink_0.set_attenuation(0, 14.9)
        if not true_en:
            self.iio_fmcomms2_sink_0.set_attenuation(1, 10.0)
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
        self.analog_sig_source_x_1 = analog.sig_source_c(100, analog.GR_CONST_WAVE, 0, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_1, 0), (self.hf_probe_signal, 0))
        self.connect((self.radar_signal_generator_fmcw_c_0, 0), (self.iio_fmcomms2_sink_0, 0))


    def get_END_1(self):
        return self.END_1

    def set_END_1(self, END_1):
        self.END_1 = END_1
        self.set_BW(receive_para.work(self.START_1,self.END_1)[0])
        self.set_SAMP(receive_para.work(self.START_1,self.END_1)[0])
        self.set_SW_feq(receive_para.work(self.START_1,self.END_1)[0])
        self.set_freq_a(receive_para.work(self.START_1,self.END_1)[1])

    def get_START_1(self):
        return self.START_1

    def set_START_1(self, START_1):
        self.START_1 = START_1
        self.set_BW(receive_para.work(self.START_1,self.END_1)[0])
        self.set_SAMP(receive_para.work(self.START_1,self.END_1)[0])
        self.set_SW_feq(receive_para.work(self.START_1,self.END_1)[0])
        self.set_freq_a(receive_para.work(self.START_1,self.END_1)[1])

    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def get_default(self):
        return self.default

    def set_default(self, default):
        self.default = default
        self.set_freq_b(self.default)

    def get_hf_function_probe(self):
        return self.hf_function_probe

    def set_hf_function_probe(self, hf_function_probe):
        self.hf_function_probe = hf_function_probe
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[0])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[1])

    def get_freq_b(self):
        return self.freq_b

    def set_freq_b(self, freq_b):
        self.freq_b = freq_b
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[0])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[1])

    def get_freq_a(self):
        return self.freq_a

    def set_freq_a(self, freq_a):
        self.freq_a = freq_a
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[0])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[1])

    def get_bbb(self):
        return self.bbb

    def set_bbb(self, bbb):
        self.bbb = bbb
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[0])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[1])

    def get_aaa(self):
        return self.aaa

    def set_aaa(self, aaa):
        self.aaa = aaa
        self.set_LO_feq(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[0])
        self.set_true_en(change_sink.work(self.hf_function_probe,self.aaa, self.bbb, self.freq_a, self.freq_b, self.freq_a[0],1)[1])

    def get_true_en(self):
        return self.true_en

    def set_true_en(self, true_en):
        self.true_en = true_en

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
        "--END-1", dest="END_1", type=intx, default=2500000000,
        help="Set END_1 [default=%(default)r]")
    parser.add_argument(
        "--START-1", dest="START_1", type=intx, default=2400000000,
        help="Set START_1 [default=%(default)r]")
    parser.add_argument(
        "--uri", dest="uri", type=str, default='192.168.1.13',
        help="Set uri [default=%(default)r]")
    return parser


def main(top_block_cls=CUSTOM_2400M, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(END_1=options.END_1, START_1=options.START_1, uri=options.uri)

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
