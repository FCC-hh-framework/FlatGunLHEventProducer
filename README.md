[]() FlatGunLHEventProducer
================================================

This simple script allows to generate 2-->2 process with a flat pT, eta spectrum and store the output in LHE format.
For simplification, momentum balance in "z" axis is assumed (i.e pz = 0). 

The following processes are supported:
-   g g --> g g
-   q q --> q q

**NOTE: This script is intended to be used for detector studies only, not for physics.**

[]() General instructions
--------------------------

In order to run this script, you first need to ensure you have at least **Python 2.7**.
If you are on lxplus, you can type:

```
source /cvmfs/sft.cern.ch/lcg/releases/LCG_87/Python/2.7.10/x86_64-slc6-gcc49-opt/Python-env.sh
```

For instructions, type:
```
./flatGunLHEventProducer.py -h
```

For instance:
```
 ./flatGunLHEventProducer.py --process gg2gg --ptmin 1 --ptmax 10000 --etamin -5 --etamax 5 --N 1000 --seed 1233 --output events.lhe --nolog --ecm 100000
```
