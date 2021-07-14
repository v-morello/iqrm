# IQRM

A minimal implementation of the IQRM interference flagging algorithm for radio pulsar and transient searches. This module only provides the algorithm that infers a channel mask from some spectral statistic that measures the level of RFI contamination in a time-frequency data block. It should be useful as a reference implementation to developers who wish to integrate IQRM into an existing pipeline / search code.

**However, if you wish to clean existing SIGPROC files using IQRM, please use Kaustubh Rajwade's full implementation:**  
https://gitlab.com/kmrajwade/iqrm_apollo


## Citation

If IQRM contributes to a scientific publication, please cite the article:  
[IQRM: real-time adaptive RFI masking for radio transient and pulsar searches](http://TODO.FIXME)

## Installation

The module is available from PyPI:
```
pip install iqrm
```


Alternatively, you can clone the repository an run:
```
make install
```
Which installs the module in [editable mode](https://pip.pypa.io/en/latest/cli/pip_install/#editable-installs), which means you can freely edit the code. The module has very few dependencies: `numpy`, `pytest` and `pytest-cov` for unit tests. They will be automatically installed by `pip` if not present. To run the unit tests and print a coverage report, simply run:

```
make tests
```


## Usage

The module provides a single function: `iqrm_mask`, that operates on an array that contains a spectral statistic that captures the level of RFI contamination in each frequency channel of a search-mode data block. Here is a basic example on an artificially generated time-frequency data block:


```python
import numpy as np
from iqrm import iqrm_mask

### Generate a time-frequency block containing Gaussian noise
nsamp = 1024
nchan = 10
data = np.random.normal(size=nsamp*nchan).reshape(nsamp, nchan)

# Add simulated RFI to channels indices 5 and 6
data[:, 5] += 5 * np.sin(np.arange(nsamp))
data[:, 6] += 10 * np.sin(np.arange(nsamp))

# Use per-channel standard deviation as contamination measure
spectral_std = data.std(axis=0)

### Run IQRM
mask, votes = iqrm_mask(spectral_std, radius=2)

# 'mask' is a boolean mask where 'True' denotes a channel index deemed to be contaminated
print(np.where(mask)[0])
# Output:
# [5 6]

# 'votes' is a dictionary of sets; see section 2 of the paper for an explanation of the 'voting' system
for caster in sorted(votes.keys()):
    recipients = votes[caster]
    print(caster, recipients)
# Output:
# 3 {5}
# 4 {5, 6}
# 5 {6}
# 7 {5, 6}
# 8 {6}

# For example '7 {5, 6}' means that from the point of view of channel 7, channels 5 and 6 have an abnormally high level of RFI contamination.
```

