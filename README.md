[]() FlatGunLHEventProducer
================================================

This simple script allows to generate 2-->2 process with a flat pT/energy, eta spectrum and store the output in LHE format.
For simplification, momentum balance in "z" axis is assumed (i.e pz = 0). 

The following particle production is supported:

- gluons
- light quarks (u,d,s)
- heavy quarks (c,b,t)
- leptons (e, ve, mu, vm, tau, vtau)
- EWK bosons (photon/W/Z/H)

**NOTE: This script is intended to be used for detector studies only, not for physics.**

[]() General instructions
--------------------------

This script requires at least **Python 2.7**.
If you are on lxplus, you can type:

```
source /cvmfs/sft.cern.ch/lcg/releases/LCG_87/Python/2.7.10/x86_64-slc6-gcc49-opt/Python-env.sh

```

For instructions, type:
```
./flatGunLHEventProducer.py -h
```
For instance, to produce 1k di-jet (equal mixing of quarks and gluons) events, at ECM = 100 TeV, with 100
GeV < pT < 10 TeV, in -4.0 < eta < 4.0, in flat log pT mode, type:

```
python flatGunLHEventProducer.py
  --pdg [1,2,3,4,5,21] \
  --guntype pt \
  --nevts 1000 \
  --ecm 100000. \
  --pmin 100. \
  --pmax 10000. \
  --etamin -4. \
  --etamax 4. \
  --maxFail 100 \
  --seed 123 \
  --output my_dijet.lhe \
```
