#!/usr/bin/python3

import os
import subprocess
import sys

subprocess.getoutput("setenv OMP_NUM_THREADS 1")
num_core = subprocess.getoutput("grep 'core id' /proc/cpuinfo | sort -u | wc -l")
pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"

subprocess.getoutput("mkdir refdata")
subprocess.getoutput("echo '# Energy [eV], Volume tag' > toten-XxYy.ml.dat")

subprocess.getoutput("mkdir template")
subprocess.getoutput("mkdir XxYy.ml-evol")
subprocess.getoutput("cp common.hsd ./XxYy.ml-evol/")
subprocess.getoutput("cp dftb_in.hsd ./XxYy.ml-evol/")
ALC1 = subprocess.getoutput("awk '{if($1==\"A\"){print $3}}' tmp.scf.in")
#
# DeltaCodesDFT: ["094","096","098","100","102","104","106"]
vol_list = ["094","095","096","097","098","099","100","101","102","103","104","105","106","107","108","109"]
for vol in vol_list:
    print("--------------------------------")
    print("Vol(%) = ",vol)
    subprocess.getoutput("mkdir "+str(vol))
    subprocess.getoutput("cp dftb_in.hsd ./"+str(vol))
    natom = subprocess.getoutput("awk '{if(NR==1){print $1}}' tmp.gen")
    sv = (float(vol)/100.0)**(1.0/3.0)
    print("a, b or c * ",sv)
    subprocess.getoutput("awk '{if(NR<=2){printf \"%s\\n\",$0}else if(NR>=3 && NR<=(2+"+str(natom)+")){printf \"%-5i %-5i %-12.8f %-12.8f %-12.8f\\n\",$1,$2,$3*"+str(sv)+",$4*"+str(sv)+",$5*"+str(sv)+"}else if(NR>=(3+"+str(natom)+")){printf \"    %-12.8f %-12.8f %-12.8f\\n\",$1*"+str(sv)+",$2*"+str(sv)+",$3*"+str(sv)+"}}' tmp.gen > POS.gen")
    subprocess.getoutput("cp POS.gen ./"+str(vol))
    #
    # PWscf
    print("PWscf calculation")
    #subprocess.getoutput("awk '{if($1==\"A\"){print \"  \"$1\" \"$2\" \"$3*"+str(sv)+"}else if($1==\"ecutwfc\"){print \"  \"$1\" \"$2\" 40.0,\"}else if($1==\"ecutrho\"){print \"  \"$1\" \"$2\" 200.0,\"}else if($1==\"degauss\"){print \"  \"$1\" \"$2\" 0.001,\"}else{print $0}}' tmp.scf.in > pw.scf.in")
    #subprocess.getoutput("sed -i 's/mp/gaussian/g' pw.scf.in")
    ALC2 = float(ALC1)*float(sv)
    subprocess.getoutput("awk '{if($1==\"A\"){print \"  A = \""+str(ALC2)+"}else{print $0}}' tmp.scf.in > pw.scf.in")
    print("A = ",ALC2)
    subprocess.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
    etot_Ry = subprocess.getoutput("grep \"  total energy\" pw.out | tail -1")
    print(etot_Ry)
    subprocess.getoutput("./pwscf2force > config")
    etot = subprocess.getoutput("awk '{if($1==\"#E\"){print $2*"+str(natom)+"}}' config")
    print(etot," eV")
    subprocess.getoutput("echo '"+str(etot)+" "+str(vol)+"' >> toten-XxYy.ml.dat")
    subprocess.getoutput("mv "+str(vol)+" ./XxYy.ml-evol/")
subprocess.getoutput("mv toten-XxYy.ml.dat ./refdata/")
subprocess.getoutput("mv ./XxYy.ml-evol ./template/")
