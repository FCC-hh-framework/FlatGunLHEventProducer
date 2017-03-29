#!/usr/bin/env python
#################################################################################################
#
# Simple script for generation of a LHE file containing events distributed with a flat (log)pt and eta spectrum.
#
# For help type:
# python FlatSpectrumProducer.py -h
#
#################################################################################################

import os
import random
import math
import argparse

def print_params(args):

    print 'sqrt(s)    : ', args.ecm
    print 'ptmin      : ', args.ptmin
    print 'ptmax      : ', args.ptmax
    print 'etamin     : ', args.etamin
    print 'etamax     : ', args.etamax
    print 'Nevents    : ', args.N
    print 'Seed       : ', args.seed
    print 'flat log   : ', args.log
    print 'output     : ', args.output

def write_init(args):

    ebeam = args.ecm/2.

    out = open(args.output, "a")
    out.write('<LesHouchesEvents version="3.0">\n')
    out.write('<init>\n')
    out.write('2212 2212 {0} {1} 0 0 1 1 -4 1\n'.format(ebeam, ebeam))
    out.write('1000. 1. 1000. 1\n')
    out.write('</init>\n')
    out.close()

def write_qq2qq(args, pt, eta, phi):

    # generating "balanced" collision, i.e x1 = x2 = 2*energy/sqrt(s)

    ebeam = args.ecm/2.
    e = pt*math.cosh(eta)
    
    # reject events that violate energy conservation
    if e > ebeam:
       return

    # compute particles 4-vectors (for massless particles): px, py, pz, e
    
    p1 = [0., 0., e, e]
    p2 = [0., 0., -e, e]
    p3 = [pt*math.cos(phi), pt*math.sin(phi), pt*math.sinh(eta), e]
    p4 = [- pt*math.cos(phi), - pt*math.sin(phi), - pt*math.sinh(eta), e]

    cf_list = []
    cf_list.append([501, 501, 502, 502])
    cf_list.append([501, 502, 501, 502])

    color = cf_list[random.randint(0, 1)]

    out = open(args.output, "a")
    out.write('<event>\n')
    out.write(' 4      1 +1000. {:.8e} 0.78186083E-02 0.11800000E+00\n'.format(2*e))
    out.write('        1 -1    0    0  {}    0 {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 1.0000e+00\n'.format(color[0], p1[0], p1[1], p1[2], p1[3], 0.))
    out.write('       -1 -1    0    0  0    {} {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 -1.0000e+00\n'.format(color[1], p2[0], p2[1], p2[2], p2[3], 0.))
    out.write('        1  1    1    2  {}    0 {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 1.0000e+00\n'.format(color[2], p3[0], p3[1], p3[2], p3[3], 0.))
    out.write('       -1  1    1    2  0    {} {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 -1.0000e+00\n'.format(color[3], p4[0], p4[1], p4[2], p4[3], 0.))
    out.write('</event>\n')


def write_gg2gg(args, pt, eta, phi):

    # generating "balanced" collision, i.e x1 = x2 = 2*energy/sqrt(s)

    ebeam = args.ecm/2.
    e = pt*math.cosh(eta)
    
    # reject events that violate energy conservation
    if e > ebeam:
       return

    # compute particles 4-vectors (for massless particles): px, py, pz, e
    
    p1 = [0., 0., e, e]
    p2 = [0., 0., -e, e]
    p3 = [pt*math.cos(phi), pt*math.sin(phi), pt*math.sinh(eta), e]
    p4 = [- pt*math.cos(phi), - pt*math.sin(phi), - pt*math.sinh(eta), e]

    cf_list = []
    cf_list.append([503, 501, 504, 502, 503, 502, 504, 501])
    cf_list.append([504, 501, 503, 502, 503, 501, 504, 502])

    color = cf_list[random.randint(0, 1)]

    out = open(args.output, "a")
    out.write('<event>\n')
    out.write(' 4      1 +1000. {:.8e} 0.78186083E-02 0.11800000E+00\n'.format(2*e))
    out.write('       21 -1    0    0  {}   {} {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 1.0000e+00\n'.format(color[0], color[1], p1[0], p1[1], p1[2], p1[3], 0.))
    out.write('       21 -1    0    0  {}   {} {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 1.0000e+00\n'.format(color[2], color[3], p2[0], p2[1], p2[2], p2[3], 0.))
    out.write('       21  1    1    2  {}   {} {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 1.0000e+00\n'.format(color[4], color[5], p3[0], p3[1], p3[2], p3[3], 0.))
    out.write('       21  1    1    2  {}   {} {:+.8e} {:+.8e} {:+.8e} {:.8e} {:.8e} 0.0000e+00 1.0000e+00\n'.format(color[6], color[7], p4[0], p4[1], p4[2], p4[3], 0.))
    out.write('</event>\n')

#__________________________________________________________

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--process", help='process to be generated. Available: qq2qq/gg2gg', default='qq2qq')
    parser.add_argument("--ptmin", type=float, help="minimum pt [GeV]", default=1.)
    parser.add_argument("--ptmax", type=float, help="maximum pt [GeV]", default=50000.)
    parser.add_argument("--etamin", type=float, help="minimum eta", default=-6.)
    parser.add_argument("--etamax", type=float, help="maximum eta", default=6.)
    parser.add_argument("--ecm,", dest='ecm', type=float, help="center of mass energy", default=13000)
    parser.add_argument("--N", type=int, help="number of events to generate", default=1000)
    parser.add_argument("--seed", type=int, help="random seed", default=0)
    parser.add_argument('--log', dest='log', help="flat in log pt", action='store_true')
    parser.add_argument('--nolog', dest='log', help="flat in pt", action='store_false')
    parser.set_defaults(flatlog=True)
    parser.add_argument("--output", help="output LHE file", default='events.lhe')

    args = parser.parse_args()
    
    # print user-defined parameters
    print_params(args)
    print ''
   
    # intialize file and write LHE file header
    out = open(args.output, "w+")
    out.close()
    write_init(args)
    
    # initialize random seed
    random.seed(args.seed)

    print 'Start event generation ...'
    
    # start event loop
    for i in range(args.N):
       
       if i%1000 == 0:
           print 'Processed {} events'.format(i)
       
       phi = random.uniform(0., math.pi)
       eta = random.uniform(args.etamin, args.etamax)

       # flat in pt or in logpt
       if args.log:
          pt = math.pow(10, random.uniform(math.log10(args.ptmin), math.log10(args.ptmax)))
       else:
          pt = random.uniform(args.ptmin, args.ptmax)
       
       # write event corresponding to required process
       if args.process == 'qq2qq':
          write_qq2qq(args, pt, eta, phi)
       if args.process == 'gg2gg':
          write_gg2gg(args, pt, eta, phi)
       

    print ''
    print 'Event generation completed.'
    print 'Output file:'
    print '{}'.format(os.path.abspath(args.output))
   

    out = open(args.output, "a")
    out.write('</LesHouchesEvents>\n')
    out.close()
