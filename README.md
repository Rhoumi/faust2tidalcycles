# faust2superdirt.py
## faust2superdirt.py is a python program, created to help users of TidalCycles in the faust audio effect adding process.
## faust2superdirt.py is conceived in adequacy with [faust2sc.py](https://github.com/madskjeldgaard/faust2sc.py)
Enabling automated writing on SuperDirt core-files and BootTidal.hs just after we make the installation of the Faust Extensions on SuperCollider.
It's got two arguments, the path to the jsonfile created by the faust2sc.py compiler and the path to your BootTidal.hs

# How to use

## The package maker
Run the faust2superdirt_packagemaker.py to create the different files. In order to add the effets manually or automatically.
* `python3 faust2superdirt_packagemaker.py 'PathtoyourJsonFile'`

## /manual_installation\

In the files2add directory, you will find three differents files :

* add2core-synth.scd 
* add2core-modules.scd 

     Add this to your core-synth.scd and core-modules.scd files usually located in /home/yourusername/.local/share/SuperCollider/downloaded-quarks/SuperDirt/synths/

* add2BootTidal.scd 

    ___ Add this to your BootTidal.hs file, be careful it's never where you think it is, mine is located in /home/yourusername/.cabal/share/x86_64-linux-ghc-8.6.5/tidal-1.7.10/

## /automatic_installation\

The real interesting thing is the automatic installation, 
just run the python program faust2superdirt.py with the two arguments :

* the path to jsonfile created by the faust2sc.py compiler.
* the path to your BootTidal.hs
### example : 
 `python3 faust2superdirt.py '/home/myusername/Documents/Myfaustplugins/Myplug.dsp.json' '/home/myusername/.cabal/share/x86_64-linux-ghc-8.6.5/tidal-1.7.10/'`
 
It will automatically write the where it has to be. 



         ><]]]^>                  ><]]]^>          ><]]]^>
       ><]]]^>           ><]]]^>         ><]]]^>      ><]]]^>
              ><]]]^>      ><]]]^>                ><]]]^>
