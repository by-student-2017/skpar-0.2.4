#1/bin/bash

if [ -e template ]; then
  echo "delete previous file (iter000)"	
  rm -f -r template
fi

if [ -z "$1" ]; then
  echo "please, input name of element 1 after command"
elif [ -z "$2" ]; then
  echo "please, input name of element 2 after command"
else
  #
  chmod +x vasp2gen
  chmod +x pwscf2force
  #
  cif2cell *.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr="./potentials" --setup-all --k-resolution=0.2 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in
  cp pw.scf.in tmp.scf.in
  #sed 2i"  disk_io = \'none\'," tmp.scf.in > pw.scf.in
  #
  cif2cell *.cif -p vasp --vasp-cartesian --vasp-format=5
  ./vasp2gen
  cp POS.gen tmp.gen
  #
  python3 data.py
  #
  rm -f -r tmp.scf.in pw.scf.in pw.out
  rm -f -r tmp.gen tmp.out
  rm -f -r POS.gen POSCAR
  rm -f -r config
  rm -f -r work
  #
  cd template
  mv XxYy.ml-evol $1$2.ml-evol
  cd ..
  #
  cp skpar_origin.in.yaml skpar.in.yaml
  sed -i "s/Xx/$1/g" skpar.in.yaml
  sed -i "s/Yy/$2/g" skpar.in.yaml
  #
fi
