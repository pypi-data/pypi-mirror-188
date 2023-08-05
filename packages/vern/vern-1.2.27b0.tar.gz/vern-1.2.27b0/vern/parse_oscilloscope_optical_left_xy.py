# profilometer
import numpy as np
import pandas as pd
from .misc import *
import mat73
import scipy.io
__all__ = ['parse_oscilloscope_optical_left_xy']

def read_files(input_path, txt_path, plot_path, hist_path, interactive=False):
    try:
        mat = mat73.loadmat(input_path)
    except:
        mat = scipy.io.loadmat(input_path)
    data = {
        "Time (ns)": mat["x"][0,:]*1e9,
        "Voltage (mV)": mat["y"][0,:]*1e3,
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(txt_path, index=False)
    p = Plot(df, interactive=interactive)
    p.plot(plot_path)
    p.hist(hist_path)

def parse_oscilloscope_optical_left_xy(**kwargs):
    read_files(kwargs["input_path"], kwargs["txt_path"], kwargs["plot_path"], kwargs["hist_path"])
