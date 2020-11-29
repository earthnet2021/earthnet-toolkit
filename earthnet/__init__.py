"""EarthNet2021 Toolkit
A library for downloading, evaluating and plotting Earth surface forecasts.
"""
__version__ = "0.2.0"
__author__ = 'Vitus Benson, Christian Requena-Mesa'
__credits__ = 'Max-Planck-Institute for Biogeochemistry'

from earthnet.parallel_score import EarthNetScore
from earthnet.download import Downloader