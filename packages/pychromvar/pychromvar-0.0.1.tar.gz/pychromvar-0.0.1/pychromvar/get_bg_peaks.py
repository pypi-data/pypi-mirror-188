from typing import Union
from anndata import AnnData
from mudata import MuData
import numpy as np
import scipy as sp
from pynndescent import NNDescent

def get_bg_peaks(data: Union[AnnData, MuData], niterations=50, n_jobs=-1):
    """
    Find background peaks based on GC bias.

    Args:
        data (Union[AnnData, MuData]):
            AnnData object with peak counts or MuData object with 'atac' modality.
        niterations (int, optional): 
            Number of background peaks to sample. Defaults to 50.
        n_jobs:

    Raises:
        TypeError: _description_
    """
    if isinstance(data, AnnData):
        adata = data
    elif isinstance(data, MuData) and "atac" in data.mod:
        adata = data.mod["atac"]
    else:
        raise TypeError(
            "Expected AnnData or MuData object with 'atac' modality")

    # check if the object contains bias in Anndata.varm
    assert "gc_bias" in adata.var.columns, "Cannot find gc bias in the input object, please first run add_gc_bias!"

    reads_per_peak = np.log10(np.sum(adata.X, axis=0))

    # here if reads_per_peak is a numpy matrix, convert it to array
    if isinstance(reads_per_peak, np.matrix):
        reads_per_peak = np.squeeze(np.asarray(reads_per_peak))

    mat = np.array([reads_per_peak, adata.var['gc_bias'].values])
    chol_cov_mat = np.linalg.cholesky(np.cov(mat))
    trans_norm_mat = sp.linalg.solve_triangular(
        a=chol_cov_mat, b=mat, lower=True).transpose()

    index = NNDescent(trans_norm_mat, metric="euclidean", n_neighbors=niterations, n_jobs=n_jobs)
    knn_idx, _ = index.query(trans_norm_mat, niterations)

    adata.varm['bg_peaks'] = knn_idx

    return None




