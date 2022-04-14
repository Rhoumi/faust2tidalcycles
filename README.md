# faust2superdirt.py
## faust2superdirt.py is conceived as an autonomous extension in order to be used after [faust2sc.py](https://github.com/madskjeldgaard/faust2sc.py)
Enabling automated writing on SuperDirt core-files and BootTidal.hs just after we make the installation of the Faust Extensions on SuperCollider.

# How to use

## 1. Download 

## 2. just run 
### `python3 faust2superdirt.py 'PathtoyourJsonFile' 'PathtoyourBootTidal.hs'`
  
* First argument is the path to the Faust.dsp.json file to be used, normally created in the same location as your Faust.dsp by faust2sc.py
* Second argument is your BootTidal.hs path, it's never where you think it is, be carefull
you can write the approximate path as long as your are still above it 

### example : 
#### `python3 faust2superdirt.py '/home/myusername/Documents/Myfaustplugins/Myplug.dsp.json' '/home/myusername/.cabal/share/x86_64-linux-ghc-8.6.5/tidal-1.7.10/'`

##### WIP
###### Needed to be fixed : 
###### * Need to be path relative to users and arch, but for now it's working on linux pretty well


> '><]]]^>'
    </br> &nbsp; &nbsp; &nbsp;   '><]]]^>'
