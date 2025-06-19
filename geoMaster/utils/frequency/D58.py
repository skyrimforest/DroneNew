#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
from gnuradio import zeromq
import D58_build_FFT as build_FFT  # embedded python module
import D58_epy_block_0 as epy_block_0  # embedded python block
import D58_new_change_sink as new_change_sink  # embedded python module
import sip
import time
import threading



class D58(gr.top_block, Qt.QWidget):

    def __init__(self, uri='192.168.1.14', uri_1='192.168.1.15', uri_2='192.168.1.16', uri_3='192.168.1.13'):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "D58")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.uri = uri
        self.uri_1 = uri_1
        self.uri_2 = uri_2
        self.uri_3 = uri_3

        ##################################################
        # Variables
        ##################################################
        self.hf_function_probe = hf_function_probe = 0
        self.CF_TABLE = CF_TABLE =  [(5.741e9, 5.772e9, 5.803e9, 5.834e9),(5.741e9, 5.772e9, 5.803e9, 5.834e9)]
        self.vf_function_probe = vf_function_probe = 0
        self.HZ = HZ = 2
        self.FREQ_QUAD = FREQ_QUAD = new_change_sink.work(hf_function_probe, CF_TABLE, 0.5)
        self.FFT = FFT = 1024
        self.vec_len = vec_len = 1024
        self.threshold_vector = threshold_vector = build_FFT.work(vf_function_probe, FREQ_QUAD, FFT, HZ)[1]
        self.new_vector = new_vector = build_FFT.work(vf_function_probe, FREQ_QUAD, FFT, HZ)[0]
        self.gamma_wifi = gamma_wifi = 0.02
        self.gamma_dji = gamma_dji = 0.05
        self.band_idx = band_idx = 0 if FREQ_QUAD == CF_TABLE[0] else 1
        self.SAMP = SAMP = 30700000
        self.NCP = NCP = 144
        self.FFT_0 = FFT_0 = 4096
        self.CP_length = CP_length = 72

        ##################################################
        # Blocks
        ##################################################

        self.vf_probe_vector = blocks.probe_signal_vf(FFT_0)
        self.hf_probe_signal = blocks.probe_signal_c()
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, 4096, 'ipc:///tmp/fft1.ipc', 100, False, (-1), '', True, True)
        def _vf_function_probe_probe():
          while True:

            val = self.vf_probe_vector.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_vf_function_probe,val))
              except AttributeError:
                self.set_vf_function_probe(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (HZ))
        _vf_function_probe_thread = threading.Thread(target=_vf_function_probe_probe)
        _vf_function_probe_thread.daemon = True
        _vf_function_probe_thread.start()
        self.qtgui_vector_sink_f_0_1 = qtgui.vector_sink_f(
            (FFT*len(CF_TABLE[0])),
            ((FREQ_QUAD[0]-SAMP/2)/1e6),
            ((SAMP/FFT)/1000000),
            "MHz",
            "dB",
            "",
            2, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1.set_update_time(0.1)
        self.qtgui_vector_sink_f_0_1.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_ref_level((-40))


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            SAMP, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-0.2, 1.2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.iio_fmcomms2_source_0_2 = iio.fmcomms2_source_fc32(uri_3, [True, True, False, False], 16384)
        self.iio_fmcomms2_source_0_2.set_len_tag_key('packet_len')
        self.iio_fmcomms2_source_0_2.set_frequency(int(FREQ_QUAD[2]))
        self.iio_fmcomms2_source_0_2.set_samplerate(SAMP)
        if True:
            self.iio_fmcomms2_source_0_2.set_gain_mode(0, 'fast_attack')
            self.iio_fmcomms2_source_0_2.set_gain(0, 64)
        if False:
            self.iio_fmcomms2_source_0_2.set_gain_mode(1, 'slow_attack')
            self.iio_fmcomms2_source_0_2.set_gain(1, 64)
        self.iio_fmcomms2_source_0_2.set_quadrature(True)
        self.iio_fmcomms2_source_0_2.set_rfdc(True)
        self.iio_fmcomms2_source_0_2.set_bbdc(True)
        self.iio_fmcomms2_source_0_2.set_filter_params('Auto', '', 0, 0)
        self.iio_fmcomms2_source_0_1 = iio.fmcomms2_source_fc32(uri_1, [True, True, False, False], 16384)
        self.iio_fmcomms2_source_0_1.set_len_tag_key('packet_len')
        self.iio_fmcomms2_source_0_1.set_frequency(int(FREQ_QUAD[1]))
        self.iio_fmcomms2_source_0_1.set_samplerate(SAMP)
        if True:
            self.iio_fmcomms2_source_0_1.set_gain_mode(0, 'fast_attack')
            self.iio_fmcomms2_source_0_1.set_gain(0, 64)
        if False:
            self.iio_fmcomms2_source_0_1.set_gain_mode(1, 'slow_attack')
            self.iio_fmcomms2_source_0_1.set_gain(1, 64)
        self.iio_fmcomms2_source_0_1.set_quadrature(True)
        self.iio_fmcomms2_source_0_1.set_rfdc(True)
        self.iio_fmcomms2_source_0_1.set_bbdc(True)
        self.iio_fmcomms2_source_0_1.set_filter_params('Auto', '', 0, 0)
        self.iio_fmcomms2_source_0_0 = iio.fmcomms2_source_fc32(uri_2, [True, True, False, False], 16384)
        self.iio_fmcomms2_source_0_0.set_len_tag_key('packet_len')
        self.iio_fmcomms2_source_0_0.set_frequency(int(FREQ_QUAD[2]))
        self.iio_fmcomms2_source_0_0.set_samplerate(SAMP)
        if True:
            self.iio_fmcomms2_source_0_0.set_gain_mode(0, 'fast_attack')
            self.iio_fmcomms2_source_0_0.set_gain(0, 64)
        if False:
            self.iio_fmcomms2_source_0_0.set_gain_mode(1, 'slow_attack')
            self.iio_fmcomms2_source_0_0.set_gain(1, 64)
        self.iio_fmcomms2_source_0_0.set_quadrature(True)
        self.iio_fmcomms2_source_0_0.set_rfdc(True)
        self.iio_fmcomms2_source_0_0.set_bbdc(True)
        self.iio_fmcomms2_source_0_0.set_filter_params('Auto', '', 0, 0)
        self.iio_fmcomms2_source_0 = iio.fmcomms2_source_fc32(uri, [True, True, False, False], 16384)
        self.iio_fmcomms2_source_0.set_len_tag_key('packet_len')
        self.iio_fmcomms2_source_0.set_frequency(int(FREQ_QUAD[0]))
        self.iio_fmcomms2_source_0.set_samplerate(SAMP)
        if True:
            self.iio_fmcomms2_source_0.set_gain_mode(0, 'fast_attack')
            self.iio_fmcomms2_source_0.set_gain(0, 64)
        if False:
            self.iio_fmcomms2_source_0.set_gain_mode(1, 'slow_attack')
            self.iio_fmcomms2_source_0.set_gain(1, 64)
        self.iio_fmcomms2_source_0.set_quadrature(True)
        self.iio_fmcomms2_source_0.set_rfdc(True)
        self.iio_fmcomms2_source_0.set_bbdc(True)
        self.iio_fmcomms2_source_0.set_filter_params('Auto', '', 0, 0)
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
            time.sleep(1.0 / (HZ))
        _hf_function_probe_thread = threading.Thread(target=_hf_function_probe_probe)
        _hf_function_probe_thread.daemon = True
        _hf_function_probe_thread.start()
        self.fft_vxx_0_1_0 = fft.fft_vcc(FFT, True, window.blackmanharris(FFT), True, 1)
        self.fft_vxx_0_1 = fft.fft_vcc(FFT, True, window.blackmanharris(FFT), True, 1)
        self.fft_vxx_0_0_0 = fft.fft_vcc(FFT, True, window.blackmanharris(FFT), True, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(FFT, True, window.blackmanharris(FFT), True, 1)
        self.epy_block_0 = epy_block_0.blk(vlen_in=1024)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f(threshold_vector, True, (FFT*len(CF_TABLE[0])), [])
        self.blocks_vector_source_x_0 = blocks.vector_source_f(new_vector, True, (FFT*len(CF_TABLE[0])), [])
        self.blocks_threshold_ff_0_3 = blocks.threshold_ff(gamma_wifi, gamma_wifi, 0)
        self.blocks_threshold_ff_0_1 = blocks.threshold_ff(gamma_wifi, gamma_wifi, 0)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(gamma_wifi, gamma_wifi, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(gamma_wifi, gamma_wifi, 0)
        self.blocks_stream_to_vector_0_1_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, FFT_0, 0)
        self.blocks_multiply_const_xx_0_1_0 = blocks.multiply_const_cc(1/FFT, FFT)
        self.blocks_multiply_const_xx_0_1 = blocks.multiply_const_cc(1/FFT, FFT)
        self.blocks_multiply_const_xx_0_0_0 = blocks.multiply_const_cc(1/FFT, FFT)
        self.blocks_multiply_const_xx_0_0 = blocks.multiply_const_cc(1/FFT, FFT)
        self.blocks_multiply_conjugate_cc_0_3 = blocks.multiply_conjugate_cc(1)
        self.blocks_multiply_conjugate_cc_0_1 = blocks.multiply_conjugate_cc(1)
        self.blocks_multiply_conjugate_cc_0_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_moving_average_xx_0_3 = blocks.moving_average_cc(NCP, 1/NCP, 4000, 1)
        self.blocks_moving_average_xx_0_1 = blocks.moving_average_cc(NCP, 1/NCP, 4000, 1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_cc(NCP, 1/NCP, 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_cc(NCP, 1/NCP, 4000, 1)
        self.blocks_max_xx_0_0 = blocks.max_ff(FFT_0, FFT_0)
        self.blocks_max_xx_0 = blocks.max_ff(1, 1)
        self.blocks_delay_0_0_0_0_0_0_3 = blocks.delay(gr.sizeof_gr_complex*1, 2048)
        self.blocks_delay_0_0_0_0_0_0_1 = blocks.delay(gr.sizeof_gr_complex*1, 2048)
        self.blocks_delay_0_0_0_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 2048)
        self.blocks_delay_0_0_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 2048)
        self.blocks_delay_0_0_0_0_0 = blocks.delay(gr.sizeof_float*FFT_0, 18432)
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_float*FFT_0, 14336)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_float*FFT_0, 10240)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*FFT_0, 6144)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*FFT_0, 2048)
        self.blocks_correctiq_auto_0_1_0 = blocks.correctiq_auto(SAMP, int(FREQ_QUAD[2]), 0, 100)
        self.blocks_correctiq_auto_0_1 = blocks.correctiq_auto(SAMP, int(FREQ_QUAD[0]), 0, 100)
        self.blocks_correctiq_auto_0_0_0 = blocks.correctiq_auto(SAMP, int(FREQ_QUAD[3]), 0, 100)
        self.blocks_correctiq_auto_0_0 = blocks.correctiq_auto(SAMP, int(FREQ_QUAD[1]), 0, 100)
        self.blocks_complex_to_mag_squared_0_1_0 = blocks.complex_to_mag_squared(FFT)
        self.blocks_complex_to_mag_squared_0_1 = blocks.complex_to_mag_squared(FFT)
        self.blocks_complex_to_mag_squared_0_0_0 = blocks.complex_to_mag_squared(FFT)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(FFT)
        self.blocks_complex_to_mag_0_0_3 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0_0_1 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(100, analog.GR_CONST_WAVE, 0, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_1, 0), (self.hf_probe_signal, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0_1, 0), (self.blocks_threshold_ff_0_1, 0))
        self.connect((self.blocks_complex_to_mag_0_0_3, 0), (self.blocks_threshold_ff_0_3, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.epy_block_0, 1))
        self.connect((self.blocks_complex_to_mag_squared_0_0_0, 0), (self.epy_block_0, 3))
        self.connect((self.blocks_complex_to_mag_squared_0_1, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_1_0, 0), (self.epy_block_0, 2))
        self.connect((self.blocks_correctiq_auto_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_correctiq_auto_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 0))
        self.connect((self.blocks_correctiq_auto_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_correctiq_auto_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_3, 0))
        self.connect((self.blocks_correctiq_auto_0_0_0, 0), (self.blocks_multiply_conjugate_cc_0_3, 0))
        self.connect((self.blocks_correctiq_auto_0_0_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_correctiq_auto_0_1, 0), (self.blocks_delay_0_0_0_0_0_0, 0))
        self.connect((self.blocks_correctiq_auto_0_1, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.blocks_correctiq_auto_0_1, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_correctiq_auto_0_1_0, 0), (self.blocks_delay_0_0_0_0_0_0_1, 0))
        self.connect((self.blocks_correctiq_auto_0_1_0, 0), (self.blocks_multiply_conjugate_cc_0_1, 0))
        self.connect((self.blocks_correctiq_auto_0_1_0, 0), (self.blocks_stream_to_vector_0_1_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_max_xx_0_0, 4))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_max_xx_0_0, 3))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_max_xx_0_0, 2))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.blocks_max_xx_0_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_max_xx_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0_0_1, 0), (self.blocks_multiply_conjugate_cc_0_1, 1))
        self.connect((self.blocks_delay_0_0_0_0_0_0_3, 0), (self.blocks_multiply_conjugate_cc_0_3, 1))
        self.connect((self.blocks_max_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_max_xx_0_0, 0), (self.vf_probe_vector, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_complex_to_mag_0_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_1, 0), (self.blocks_complex_to_mag_0_0_1, 0))
        self.connect((self.blocks_moving_average_xx_0_3, 0), (self.blocks_complex_to_mag_0_0_3, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_1, 0), (self.blocks_moving_average_xx_0_1, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_3, 0), (self.blocks_moving_average_xx_0_3, 0))
        self.connect((self.blocks_multiply_const_xx_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_1, 0), (self.blocks_complex_to_mag_squared_0_1, 0))
        self.connect((self.blocks_multiply_const_xx_0_1_0, 0), (self.blocks_complex_to_mag_squared_0_1_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_delay_0_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.fft_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.fft_vxx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_1_0, 0), (self.fft_vxx_0_1_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_max_xx_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_max_xx_0, 1))
        self.connect((self.blocks_threshold_ff_0_1, 0), (self.blocks_max_xx_0, 2))
        self.connect((self.blocks_threshold_ff_0_3, 0), (self.blocks_max_xx_0, 3))
        self.connect((self.blocks_vector_source_x_0, 0), (self.qtgui_vector_sink_f_0_1, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.qtgui_vector_sink_f_0_1, 1))
        self.connect((self.epy_block_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.epy_block_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_const_xx_0_0, 0))
        self.connect((self.fft_vxx_0_0_0, 0), (self.blocks_multiply_const_xx_0_0_0, 0))
        self.connect((self.fft_vxx_0_1, 0), (self.blocks_multiply_const_xx_0_1, 0))
        self.connect((self.fft_vxx_0_1_0, 0), (self.blocks_multiply_const_xx_0_1_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.blocks_correctiq_auto_0_1, 0))
        self.connect((self.iio_fmcomms2_source_0_0, 0), (self.blocks_correctiq_auto_0_1_0, 0))
        self.connect((self.iio_fmcomms2_source_0_1, 0), (self.blocks_correctiq_auto_0_0, 0))
        self.connect((self.iio_fmcomms2_source_0_2, 0), (self.blocks_correctiq_auto_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "D58")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def get_uri_1(self):
        return self.uri_1

    def set_uri_1(self, uri_1):
        self.uri_1 = uri_1

    def get_uri_2(self):
        return self.uri_2

    def set_uri_2(self, uri_2):
        self.uri_2 = uri_2

    def get_uri_3(self):
        return self.uri_3

    def set_uri_3(self, uri_3):
        self.uri_3 = uri_3

    def get_hf_function_probe(self):
        return self.hf_function_probe

    def set_hf_function_probe(self, hf_function_probe):
        self.hf_function_probe = hf_function_probe
        self.set_FREQ_QUAD(new_change_sink.work(self.hf_function_probe, self.CF_TABLE, 0.5))

    def get_CF_TABLE(self):
        return self.CF_TABLE

    def set_CF_TABLE(self, CF_TABLE):
        self.CF_TABLE = CF_TABLE
        self.set_FREQ_QUAD(new_change_sink.work(self.hf_function_probe, self.CF_TABLE, 0.5))
        self.set_band_idx(0 if self.FREQ_QUAD == self.CF_TABLE[0] else 1)

    def get_vf_function_probe(self):
        return self.vf_function_probe

    def set_vf_function_probe(self, vf_function_probe):
        self.vf_function_probe = vf_function_probe
        self.set_new_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[0])
        self.set_threshold_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[1])

    def get_HZ(self):
        return self.HZ

    def set_HZ(self, HZ):
        self.HZ = HZ
        self.set_new_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[0])
        self.set_threshold_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[1])

    def get_FREQ_QUAD(self):
        return self.FREQ_QUAD

    def set_FREQ_QUAD(self, FREQ_QUAD):
        self.FREQ_QUAD = FREQ_QUAD
        self.set_band_idx(0 if self.FREQ_QUAD == self.CF_TABLE[0] else 1)
        self.set_new_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[0])
        self.set_threshold_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[1])
        self.blocks_correctiq_auto_0_0.set_freq(int(self.FREQ_QUAD[1]))
        self.blocks_correctiq_auto_0_0_0.set_freq(int(self.FREQ_QUAD[3]))
        self.blocks_correctiq_auto_0_1.set_freq(int(self.FREQ_QUAD[0]))
        self.blocks_correctiq_auto_0_1_0.set_freq(int(self.FREQ_QUAD[2]))
        self.iio_fmcomms2_source_0.set_frequency(int(self.FREQ_QUAD[0]))
        self.iio_fmcomms2_source_0_0.set_frequency(int(self.FREQ_QUAD[2]))
        self.iio_fmcomms2_source_0_1.set_frequency(int(self.FREQ_QUAD[1]))
        self.iio_fmcomms2_source_0_2.set_frequency(int(self.FREQ_QUAD[2]))
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.FREQ_QUAD[0]-self.SAMP/2)/1e6), ((self.SAMP/self.FFT)/1000000))

    def get_FFT(self):
        return self.FFT

    def set_FFT(self, FFT):
        self.FFT = FFT
        self.set_new_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[0])
        self.set_threshold_vector(build_FFT.work(self.vf_function_probe, self.FREQ_QUAD, self.FFT, self.HZ)[1])
        self.blocks_multiply_const_xx_0_0.set_k(1/self.FFT)
        self.blocks_multiply_const_xx_0_0_0.set_k(1/self.FFT)
        self.blocks_multiply_const_xx_0_1.set_k(1/self.FFT)
        self.blocks_multiply_const_xx_0_1_0.set_k(1/self.FFT)
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.FREQ_QUAD[0]-self.SAMP/2)/1e6), ((self.SAMP/self.FFT)/1000000))

    def get_vec_len(self):
        return self.vec_len

    def set_vec_len(self, vec_len):
        self.vec_len = vec_len

    def get_threshold_vector(self):
        return self.threshold_vector

    def set_threshold_vector(self, threshold_vector):
        self.threshold_vector = threshold_vector
        self.blocks_vector_source_x_0_0.set_data(self.threshold_vector, [])

    def get_new_vector(self):
        return self.new_vector

    def set_new_vector(self, new_vector):
        self.new_vector = new_vector
        self.blocks_vector_source_x_0.set_data(self.new_vector, [])

    def get_gamma_wifi(self):
        return self.gamma_wifi

    def set_gamma_wifi(self, gamma_wifi):
        self.gamma_wifi = gamma_wifi
        self.blocks_threshold_ff_0.set_hi(self.gamma_wifi)
        self.blocks_threshold_ff_0.set_lo(self.gamma_wifi)
        self.blocks_threshold_ff_0_0.set_hi(self.gamma_wifi)
        self.blocks_threshold_ff_0_0.set_lo(self.gamma_wifi)
        self.blocks_threshold_ff_0_1.set_hi(self.gamma_wifi)
        self.blocks_threshold_ff_0_1.set_lo(self.gamma_wifi)
        self.blocks_threshold_ff_0_3.set_hi(self.gamma_wifi)
        self.blocks_threshold_ff_0_3.set_lo(self.gamma_wifi)

    def get_gamma_dji(self):
        return self.gamma_dji

    def set_gamma_dji(self, gamma_dji):
        self.gamma_dji = gamma_dji

    def get_band_idx(self):
        return self.band_idx

    def set_band_idx(self, band_idx):
        self.band_idx = band_idx

    def get_SAMP(self):
        return self.SAMP

    def set_SAMP(self, SAMP):
        self.SAMP = SAMP
        self.iio_fmcomms2_source_0.set_samplerate(self.SAMP)
        self.iio_fmcomms2_source_0_0.set_samplerate(self.SAMP)
        self.iio_fmcomms2_source_0_1.set_samplerate(self.SAMP)
        self.iio_fmcomms2_source_0_2.set_samplerate(self.SAMP)
        self.qtgui_time_sink_x_0.set_samp_rate(self.SAMP)
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.FREQ_QUAD[0]-self.SAMP/2)/1e6), ((self.SAMP/self.FFT)/1000000))

    def get_NCP(self):
        return self.NCP

    def set_NCP(self, NCP):
        self.NCP = NCP
        self.blocks_moving_average_xx_0.set_length_and_scale(self.NCP, 1/self.NCP)
        self.blocks_moving_average_xx_0_0.set_length_and_scale(self.NCP, 1/self.NCP)
        self.blocks_moving_average_xx_0_1.set_length_and_scale(self.NCP, 1/self.NCP)
        self.blocks_moving_average_xx_0_3.set_length_and_scale(self.NCP, 1/self.NCP)

    def get_FFT_0(self):
        return self.FFT_0

    def set_FFT_0(self, FFT_0):
        self.FFT_0 = FFT_0

    def get_CP_length(self):
        return self.CP_length

    def set_CP_length(self, CP_length):
        self.CP_length = CP_length



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--uri", dest="uri", type=str, default='192.168.1.14',
        help="Set uri [default=%(default)r]")
    parser.add_argument(
        "--uri-1", dest="uri_1", type=str, default='192.168.1.15',
        help="Set uri_1 [default=%(default)r]")
    parser.add_argument(
        "--uri-2", dest="uri_2", type=str, default='192.168.1.16',
        help="Set uri_2 [default=%(default)r]")
    parser.add_argument(
        "--uri-3", dest="uri_3", type=str, default='192.168.1.13',
        help="Set uri_3 [default=%(default)r]")
    return parser


def main(top_block_cls=D58, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(uri=options.uri, uri_1=options.uri_1, uri_2=options.uri_2, uri_3=options.uri_3)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
