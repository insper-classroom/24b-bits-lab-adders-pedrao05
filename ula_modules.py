#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b 

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    # s1 = Signal(bool(0))
    # s2 = Signal(bool(0)) 
    # s3 = Signal(bool(0))
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]

    # half_1 = halfAdder(a, b, s[0], s[1]) 
    # half_2 = halfAdder(c, s[0], soma, s[2])
    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        # soma.next = a ^ b ^ c
        # carry.next = (a & b) | (b & c) | (a & c)

        carry.next = s[1] | s[2] 

    return instances()


@block
def adder2bits(x, y, soma, carry):
    carry1 = Signal(bool(0))

    ha = halfAdder(x[0], y[0], soma[0], carry1)

    fa = fullAdder(x[1], y[1], carry1, soma[1], carry)
    
    return instances()


@block
def adder(x, y, soma, carry):
    n = len(x)
    carry_in = [Signal(bool(0)) for _ in range(n + 1)]
    
    carry_in[0].next = False

    faList = [None for _ in range(n)]

    for i in range(n):
        faList[i] = fullAdder(x[i], y[i], carry_in[i], soma[i], carry_in[i+1])

    @always_comb
    def comb():
        carry.next = carry_in[n]

    return instances()
