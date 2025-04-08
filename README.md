# IQRM

[![arXiv](http://img.shields.io/badge/astro.ph-2108.12434-B31B1B.svg)](https://arxiv.org/abs/2108.12434)   ![License](https://img.shields.io/badge/License-MIT-green.svg)   ![CI status](https://github.com/v-morello/iqrm/actions/workflows/CI.yml/badge.svg?branch=master)   [![codecov](https://codecov.io/gh/v-morello/iqrm/branch/master/graph/badge.svg)](https://codecov.io/gh/v-morello/iqrm)

A minimal implementation of the IQRM interference flagging algorithm for radio pulsar and transient searches. This module only provides the algorithm that infers a channel mask from some spectral statistic that measures the level of RFI contamination in a time-frequency data block. It should be useful as a reference implementation to developers who wish to integrate IQRM into an existing pipeline / search code.

**However, if you wish to clean existing SIGPROC files using IQRM, please use Kaustubh Rajwade's full implementation:**  
https://gitlab.com/kmrajwade/iqrm_apollo


## Citation

If IQRM contributes to a scientific publication, please cite the article (link will be provided soon):  
[IQRM: real-time adaptive RFI masking for radio transient and pulsar searches](https://arxiv.org/abs/2108.12434)

## Installation

The easiest method is to use pip install, which also pulls required dependencies:
```
pip install iqrm
```

Alternatively you can clone the repository and run `make install`:
```
git clone https://github.com/v-morello/iqrm
cd iqrm
make install
```

This simply runs `pip install` in [editable mode](https://pip.pypa.io/en/latest/cli/pip_install/#editable-installs), which means you can freely edit the code. It also installs any required dependencies with pip that are not present already. You can check that it all works by running the test suite in a Python or IPython console:

```python
>>> import iqrm
>>> iqrm.test()
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

