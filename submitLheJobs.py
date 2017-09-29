#!/usr/bin/env python
import os, sys, subprocess
import argparse 
import commands
import time

#____________________________________________________________________________________________________________
### processing the external os commands
def processCmd(cmd, quite = 0):
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
    return output
#_____________________________________________________________________________________________________________
def main():

    parser = argparse.ArgumentParser()

    # --  flat gun options (all but output file name/seed)--
    parser.add_argument("--pdg", nargs='+', type=int)
    parser.add_argument('--guntype', dest='guntype', help='pt or e gun. The parameters pmin(max) are then interpreted as ptmin(max) or emin(max) depending on the specified gunmode', default='pt')
    parser.add_argument("--pmin", type=float, help="minimum pt/e [GeV] (default: 1.)", default=1.)
    parser.add_argument("--pmax", type=float, help="maximum pt/e [GeV] (default: 50000.)", default=50000.)
    parser.add_argument("--etamin", type=float, help="minimum eta (default: -2.5)", default=-6.)
    parser.add_argument("--etamax", type=float, help="maximum eta (default: 2.5)", default=6.)
    parser.add_argument("--ecm,", dest='ecm', type=float, help="center of mass energy (default: 13000)", default=13000)
    parser.add_argument("--nevts", type=int, help="number of events per job to generate (default: 1000)", default=1000)
    parser.add_argument('--log', dest='log', help="flat in log pt (default: yes)", action='store_true')
    parser.add_argument('--nolog', dest='log', help="flat in pt (default: false)", action='store_false')
    parser.set_defaults(log=True)

    # --  LSF options --
    parser.add_argument ('--dir', help='output directory (where all LHE files are going to be stored)', default='outputDir')
    parser.add_argument ('--queue', help='lsf queue', default='1nh')
    parser.add_argument ('--njobs', help='number of jobs', type=int, dest='njobs')

    args = parser.parse_args()

    # first create output dir
    output_dir = os.path.abspath(args.dir)
    
    if not os.path.exists(output_dir):
       os.makedirs(output_dir)
       os.makedirs(output_dir+'/std/')
       os.makedirs(output_dir+'/cfg/')
    else:
       print output_dir
       sys.exit('Output dir: "'+output_dir+'" exists.')

    # prepare dummy submission script
    currentDir = os.getcwd()
    dummyscript="""
unset LD_LIBRARY_PATH
unset PYTHONHOME
unset PYTHONPATH
source /cvmfs/sft.cern.ch/lcg/releases/LCG_88/Python/2.7.13/x86_64-slc6-gcc49-opt/Python-env.sh
python {}/flatGunLHEventProducer.py \
  --pdg DUMMYPDGLIST \
  --guntype DUMMYGUNTYPE \
  --nevts DUMMYNEVTS \
  --ecm DUMMYECM \
  --pmin DUMMYPMIN \
  --pmax DUMMYPMAX \
  --etamin DUMMYETAMIN \
  --etamax DUMMYETAMAX \
  --DUMMYLOG \
  --seed DUMMYSEED \
  --output DUMMYOUTPUT
    """.format(currentDir)
    # replace relevant parts in script and dump into file
    pdg_str = ''
    for part in args.pdg:
       pdg_str += '{} '.format(part)
    
    if args.log: log_str = 'log'
    else: log_str = 'nolog'
    
    dummyscript = dummyscript.replace('DUMMYPDGLIST', pdg_str)
    dummyscript = dummyscript.replace('DUMMYGUNTYPE', str(args.guntype))
    dummyscript = dummyscript.replace('DUMMYNEVTS', str(args.nevts))
    dummyscript = dummyscript.replace('DUMMYECM', str(args.ecm))
    dummyscript = dummyscript.replace('DUMMYPMIN', str(args.pmin))
    dummyscript = dummyscript.replace('DUMMYPMAX', str(args.pmax))
    dummyscript = dummyscript.replace('DUMMYETAMIN', str(args.etamin))
    dummyscript = dummyscript.replace('DUMMYETAMAX', str(args.etamax))
    dummyscript = dummyscript.replace('DUMMYLOG', log_str)

    print '[Submitting jobs]'
    jobCount=0
    for job in xrange(args.njobs):
       
       print 'Submitting job '+str(job)+' out of '+str(args.njobs)
       basename = os.path.basename(output_dir) + '_'+str(job)
       outputFile = output_dir+'/'+basename+'.lhe'

       script = dummyscript
       script = script.replace('DUMMYSEED', str(job))
       script = script.replace('DUMMYOUTPUT', outputFile)

       fscript = output_dir+'/cfg/'+basename
       with open('script.sh', "w") as f:
          f.write(script)
       processCmd('chmod u+x script.sh')
       processCmd('mv script.sh {}'.format(fscript))

       cmd = 'bsub -o '+output_dir+'/std/'+basename +'.out -e '+output_dir+'/std/'+basename +'.err -q '+args.queue
       cmd +=' -J '+basename+' "'+fscript+'" '
       
       # submitting jobs
       output = processCmd(cmd)
       while ('error' in output):
           time.sleep(1.0);
           output = processCmd(cmd)
           if ('error' not in output):
               print 'Submitted after retry - job '+str(jobCount+1)

       jobCount += 1

#_______________________________________________________________________________________
if __name__ == "__main__":
    main()
