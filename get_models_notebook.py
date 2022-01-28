# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import ipdb
import numpy as np
import h5py
from shutil import copyfile
from astropy.table import Table, Column
from astropy.utils.data import download_file

desk_path = '.'

def read_hdf5(filename, testing):
    """Reads HDF5 file.

    Parameters
    ----------
    filename : str
        name of the file to be read including the full path.
    testing : str
        If testing flag enabled, the function will only return the
        first couple columns of the table.

    Returns
    -------
    out: astropy table
        contents of table at filename.

    """
    with h5py.File(filename, "r") as f:
        key = list(f.keys())[0]
        if (testing == True) | (testing == "True"):
            data = list(f[key][0:3])
        else:
            data = list(f[key])
    out = Table(np.array(data))
    return out


def get_remote_models(model_grid_name):
    """Downloads models and model results files (HDF5) from BOX.

    Parameters
    ----------
    model_grid_name : str
        Name of model grid to download.

    """
    # update if zeonodo repository updated
    repository = 5912191

    fname_dld_outputs = download_file(
        "https://zenodo.org/record/"
        + str(repository)
        + "/files/"
        + model_grid_name
        + "_outputs.hdf5?download=1"
    )
    fname_dld_models = download_file(
        "https://zenodo.org/record/"
        + str(repository)
        + "/files/"
        + model_grid_name
        + "_models.hdf5?download=1"
    )

    copyfile(
        fname_dld_outputs, model_grid_name + "_outputs.hdf5"
    )
    copyfile(
        fname_dld_models, model_grid_name + "_models.hdf5"
    )
    # \n Padova options: J400, J1000, H11, R12, R13'


def check_models(model_grid, respond, size_filename="desk_model_grid_sizes.csv"):

    """
    Checks if model grids are available and returns the full path to the model.
    If the model is not downloaded, it is downloaded via Box.

    Parameters
    ----------
    model_grid : str
        Name of model grid to use.
    respond: Bool
        Whether to print if models were found.

    Returns
    -------
    outputs_file: str
        The full path/name of the model outputs file.
    models_file: str
        The full path/name of the model grid file.

    """

    outputs_file = model_grid + "_outputs.hdf5"
    models_file = model_grid + "_models.hdf5"

    # Checks if grid is available
    if os.path.isfile(outputs_file) and os.path.isfile(models_file):
        if respond == True:
            print("\nYou already have the grid!\n")

    else:
        # asks if you want to download the models
        if respond == True:
            print("Models not found locally, downloading . . .")
        get_remote_models(model_grid)
    return (outputs_file, models_file)
