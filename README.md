# faust2tidalcycles
## `faust2tidalcycles` is a python program, created to help users of TidalCycles in the faust audio effect adding process.

`faust2tidalcycles` works in adequacy with faust2supercollider,
you need to have faust installed on your computer.

## faust2tidalcycles has two arguments

* -p {0,1} , 1 to create the package, 0 == no package, 0 by default (optional for package installation)
* -i BootTidalPath, path to your BootTidal.hs (necessary in automatic installation mode)
* inputdsp : path to your DSP

## /automatic_installation\

The real interesting thing is the automatic installation, 
just run the python program `faust2tidalcycles` with two argument :

* -i : the path to your BootTidal.hs
* inputdsp : path to your DSP

It will automatically write the where it has to be. 

### Exemple : `faust2tidalcycles -i /home/yourusername/.cabal/share/x86_64-linux-ghc-8.6.5/tidal-1.7.10/BootTidal.hs`

## /package_installation\

Create an installation package, with 
* a faust2tidalcycles_installer python script, 
* a directory named yourDSP.files2add with the different code extract for core-synth.scd core-modules.scd and BootTidal.hs, 
* The class file and the .so file to put in Supercollider Extensions  
* And a personalized HelpFile to verify name, inputs, outputs and parameters list. 

### Exemple : `faust2tidalcycles -p 1 /myFaustDSPdir/MyEffect.dsp`

faust2tidalcycles create package files in your DSP location

R.><]]]^>
