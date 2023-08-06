# zapit-Python-Bridge

**This code is still under development. It is in no way ready for use.**
This bridge uses `matlab.engine` to communicate with MATLAB.


### Example
Until it's on PiPy you should first `cd` to code dir and
```
pip install -e .
```

Then in iPython:
```python
import zapit_python_bridge.bridge as zpb
from importlib import reload

# Create an instance of the bridge object
hZP = zpb.bridge()

# Interact
hZP.send_samples()
hZP.stop_opto_stim


hZP.send_samples(conditionNum=2,laserOn=0)
hZP.stop_opto_stim()
```

If you need to reload the module for development purposes, you **must** first delete the running class instance or it will hang when it next tries to connect:

```ipython
In [1]: hZP.release_matlab()
Disconnecting from MATLAB

In [2]: reload(zpb)
Out[2]: <module 'zapit_python_bridge.bridge' from 'D:zapit-python-bridge\\zapit_python_bridge\\bridge.py'>

In [3]: hZP = zpb.bridge()
Attempting MATLAB connection...
Connected!
```

### Minimal example for running an exeperiment
See `examples` directory

```
python minimal_experiment_example.py
```

### Connecting to the zapit session: minimal example

In MATLAB:
```MATLAB
 >> matlab.engine.shareEngine('zapit')
```

In iPython:

```python
import matlab.engine
eng = matlab.engine.connect_matlab('zapit')
```

Make sure you have set up and calibrated everything in Zapit. Now in Python you can do:

```python
hZP = eng.workspace['hZP']
hZPview = eng.workspace['hZPview']
eng.eval('hZP.stimConfig.plotChanSamples(2)',nargout=0)

# OR
SC = eng.subsref(hZP, {'type':'.','subs':'stimConfig'})
eng.plotChanSamples(SC, 1, nargout=0)


eng.sendSamples(hZP,  nargout=0)
eng.stopOptoStim(hZP,  nargout=0)
```
