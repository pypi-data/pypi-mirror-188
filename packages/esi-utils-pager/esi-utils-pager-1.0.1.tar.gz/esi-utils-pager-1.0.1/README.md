# Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Installation](#installation)
- [Upgrading](#upgrading)
- [Required data](#required-data)
- [Usage](#usage)

# Introduction

This library of tools forms the modeling core of the Prompt Assessment for Global Earthquake Response (PAGER) system,
which provides fatality and economic loss impact estimates following significant earthquakes worldwide. The models implemented here are based on work described in the following papers:

```
Jaiswal, K. S., and Wald, D. J. (2010). An Empirical Model for Global Earthquake Fatality Estimation. Earthquake Spectra, 26, No. 4, 1017-1037
```

```
Jaiswal, K. S., and Wald, D. J. (2011). Rapid estimation of the economic consequences of global earthquakes. U.S. Geological Survey Open-File Report 2011-1116, 47p.
```

```
Jaiswal, K. S., Wald, D. J., and D’Ayala, D. (2011). Developing Empirical Collapse Fragility Functions for Global Building Types. Earthquake Spectra, 27, No. 3, 775-795
```

The software here can be used for other applications, although it is important to note that the empirical loss models
have not been calibrated with events newer than 2010, and the semi-empirical fatality model results are less accurate than the empirical equivalent.

# Installation

`pip install esi-utils-pager`

# Upgrading

`pip install --upgrade esi-utils-pager`

# Required data

A number of data files external to the repository are required for usage:

 - Population grid, which can be obtained from Oakridge National Labs [Landscan project](https://landscan.ornl.gov/about)
 - Country code grid, which can be obtained upon request from the PAGER team <span style="color:red">DATA RELEASE??</span>
 - Urban/rural code grid, obtained from the Socioeconomic Data and Applications Center [(SEDAC)](https://sedac.ciesin.columbia.edu/data/collection/grump-v1)

# Usage

Usage of the relevant code modules is detailed in the Jupyter notebooks, most notably in the 
[Earthquake Losses notebook](https://code.usgs.gov/ghsc/esi/esi-utils-pager/-/blob/main/notebooks/EarthquakeLosses.ipynb)


