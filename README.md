# (Railr)oad (o)peration (c)enter, a handy CLI tool for running operations on a model railroad.
Railroc is meant to be a companion to your model railroad so that running operations is more like a game. At present railroc is quite simple but fully functional.

## How to use:
### Input
In order to run you have to load your model railroad layout information where you have specify which hubs are available as well as which cars belong to them in which states. For example, if you have one *depot* and one *coal mine* with one *coal car* and one *passenger car* you would specify it as below. The states of the cars are specified after the '|'. Here you first write what it transports (**cargo** or **people**) and then a number for how it can depart from that hub (**0** for empty, **1** for full and **2** for either).
```bash
depot;coal car|cargo 1,passenger car|people 2
coal mine;coal car|cargo 0,passenger car|people 2
```

### Running railroc
Make sure to have your 'operations_input.txt' in the same directory as 'railroc.py' and run:
```bash
$ python railroc.py
```
