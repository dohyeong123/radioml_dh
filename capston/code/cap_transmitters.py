#!/usr/bin/env python
import time, math
from scipy.signal import get_window
from gnuradio import gr, blocks, digital, analog, filter
from gnuradio.filter import firdes
import mapper
sps = 8
ebw = 0.35

class transmitter_mapper(gr.hier_block2):
    def __init__(self, modtype, symvals, txname, samples_per_symbol=2, excess_bw=0.35):
        gr.hier_block2.__init__(self, txname,
            gr.io_signature(1, 1, gr.sizeof_char),
            gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self.mod = mapper.mapper(modtype, symvals)
        # pulse shaping filter
        nfilts = 32
        ntaps = nfilts * 11 * int(samples_per_symbol)    # make nfilts filters of ntaps each
        rrc_taps = filter.firdes.root_raised_cosine(
            nfilts,          # gain
            nfilts,          # sampling rate based on 32 filters in resampler
            1.0,             # symbol rate
            excess_bw, # excess bandwidth (roll-off factor)
            ntaps)
        #self.rrc_filter = filter.pfb_arb_resampler_ccf(samples_per_symbol, rrc_taps)
        self.connect(self, self.mod, self)
        #self.rate = const.bits_per_symbol()

class transmitter_bpsk(transmitter_mapper):
    modname = "BPSK"
    def __init__(self):
        transmitter_mapper.__init__(self, mapper.BPSK,
            [0,1], "transmitter_bpsk", sps, ebw)

class transmitter_qpsk(transmitter_mapper):
    modname = "QPSK"
    def __init__(self):
        transmitter_mapper.__init__(self, mapper.QPSK,
            [0,1,3,2], "transmitter_qpsk", sps, ebw)

class transmitter_8psk(transmitter_mapper):
    modname = "8PSK"
    def __init__(self):
        transmitter_mapper.__init__(self, mapper.PSK8,
            [0,1,3,2,7,6,4,5], "transmitter_8psk", sps, ebw)

class transmitter_pam4(transmitter_mapper):
    modname = "PAM4"
    def __init__(self):
        transmitter_mapper.__init__(self, mapper.PAM4,
            [0,1,3,2], "transmitter_pam4", sps, ebw)

class transmitter_qam16(transmitter_mapper):
    modname = "QAM16"
    def __init__(self):
        transmitter_mapper.__init__(self, mapper.QAM16,
            [2,6,14,10,3,7,15,11,1,5,13,9,0,4,12,8], "transmitter_qam16", sps, ebw)

class transmitter_qam64(transmitter_mapper):
    modname = "QAM64"
    def __init__(self):
        transmitter_mapper.__init__(self, mapper.QAM64,
            [0,32,8,40,3,35,11,43,
             48,16,56,24,51,19,59,27,
            12,44,4,36,15,47,7,39,
            60,28,52,20,63,31,55,23,
            2,34,10,42,1,33,9,41,
            50,18,58,26,49,17,57,25,
            14,46,6,38,13,45,5,37,
            62,30,54,22,61,29,53,21], "transmitter_qam64", sps, ebw)

class transmitter_gfsk(gr.hier_block2):
    modname = "GFSK"
    def __init__(self):
        gr.hier_block2.__init__(self, "transmitter_gfsk",
            gr.io_signature(1, 1, gr.sizeof_char),
            gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self.repack = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.mod = digital.gfsk_mod(sps, sensitivity=0.1, bt=ebw)
        self.connect( self, self.repack, self.mod, self )

class transmitter_cpfsk(gr.hier_block2):
    modname = "CPFSK"
    def __init__(self):
        gr.hier_block2.__init__(self, "transmitter_cpfsk",
            gr.io_signature(1, 1, gr.sizeof_char),
            gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self.mod = analog.cpfsk_bc(0.5, 1.0, sps)
        self.connect( self, self.mod, self )

transmitters = {
    "discrete":[transmitter_qpsk, transmitter_bpsk]
}

