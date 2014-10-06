# -*- coding: utf-8 -*-
"""
Testing nilearn toolbox
"""
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.input_data import NiftiMasker

data = datasets.fetch_localizer_calculation_task(data_dir='.')