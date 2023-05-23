
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import osmosdr

class fm_receiver(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "FM Receiver")

        ##################################################
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.freq = freq = 88.1e6
        self.gain = gain = 20
        self.volume = volume = 0.2
        ##################################################
        ##################################################
        self.rtl_source = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtl_source.set_sample_rate(samp_rate)
        self.rtl_source.set_center_freq(freq, 0)
        self.rtl_source.set_freq_corr(0, 0)
        self.rtl_source.set_dc_offset_mode(2, 0)
        self.rtl_source.set_iq_balance_mode(2, 0)
        self.rtl_source.set_gain_mode(True, 0)
        self.rtl_source.set_gain(gain, 0)

        self.low_pass_filter = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.high_pass_filter = filter.fir_filter_ccf(1, firdes.high_pass(
        	1, samp_rate, 15e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_filter = filter.freq_xlating_fir_filter_ccf(1, (firdes.low_pass(1, samp_rate, 200e3, 10e3, firdes.WIN_HAMMING, 6.76)), 0, samp_rate)

        self.wfm_rcv = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=10,
        )
        self.audio_sink = audio.sink(int(samp_rate/10), "", True)

        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink, 0))
        self.connect((self.freq_xlating_filter, 0), (self.high_pass_filter, 0))
        self.connect((self.high_pass_filter, 0), (self.wfm_rcv, 0))
        self.connect((self.low_pass_filter, 0), (self.freq_xlating_filter, 0))
        self.connect((self.rtl_source, 0), (self.low_pass_filter, 0))
        self.connect((self.wfm_rcv, 0), (self.blocks_add_const_vxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtl_source.set_sample_rate(self.samp_rate)
        self.low_pass_filter.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.high_pass_filter.set_taps(firdes.high_pass(1, self.samp_rate, 15e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_filter.set_taps((firdes.low_pass(1, self.samp_rate, 200e3, 10e3, firdes.WIN_HAMMING, 6.76)))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.rtl_source.set_center_freq(self.freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.rtl_source.set_gain(self.gain, 0)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

if __name__ == '__main__':
    try:
        fm_receiver().run()
    except KeyboardInterrupt:
        pass
