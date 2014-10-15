# first line: 666
def unmask(X, mask_img, order="F"):
    """Take masked data and bring them back into 3D/4D

    This function can be applied to a list of masked data.

    Parameters
    ==========
    X: numpy.ndarray (or list of)
        Masked data. shape: (samples #, features #).
        If X is one-dimensional, it is assumed that samples# == 1.
    mask_img: nifti-like image
        Mask. Must be 3-dimensional.

    Returns
    =======
    data: nifti-like image (or list of)
        Unmasked data. Depending on the shape of X, data can have
        different shapes:

        - X.ndim == 2:
          Shape: (mask.shape[0], mask.shape[1], mask.shape[2], X.shape[0])
        - X.ndim == 1:
          Shape: (mask.shape[0], mask.shape[1], mask.shape[2])
    """

    if isinstance(X, list):
        ret = []
        for x in X:
            ret.append(unmask(x, mask_img, order=order))  # 1-level recursion
        return ret

    mask, affine = _load_mask_img(mask_img)

    if X.ndim == 2:
        unmasked = _unmask_nd(X, mask, order=order)
    elif X.ndim == 1:
        unmasked = _unmask_3d(X, mask, order=order)
    else:
        raise TypeError(
            "Masked data X must be 2D or 1D array; got shape: %s" % str(
                X.shape))

    return Nifti1Image(unmasked, affine)
