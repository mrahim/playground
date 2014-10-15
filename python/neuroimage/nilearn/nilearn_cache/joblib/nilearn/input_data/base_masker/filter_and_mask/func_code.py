# first line: 23
def filter_and_mask(niimgs, mask_img_,
                    parameters,
                    ref_memory_level=0,
                    memory=Memory(cachedir=None),
                    verbose=0,
                    confounds=None,
                    copy=True):
    # If we have a string (filename), we won't need to copy, as
    # there will be no side effect

    if isinstance(niimgs, basestring):
        copy = False

    if verbose > 0:
        class_name = enclosing_scope_name(stack_level=2)

    niimgs = _utils.check_niimgs(niimgs, accept_3d=True)

    # Resampling: allows the user to change the affine, the shape or both
    if verbose > 1:
        print("[%s] Resampling" % class_name)

    # Check whether resampling is truly necessary. If so, crop mask
    # as small as possible in order to speed up the process

    resampling_is_necessary = (
            (not np.allclose(niimgs.get_affine(), mask_img_.get_affine()))
        or np.any(np.array(niimgs.shape[:3]) != np.array(mask_img_.shape)))

    if resampling_is_necessary:
        # now we can crop
        mask_img_ = image.crop_img(mask_img_, copy=False)

        niimgs = cache(image.resample_img, memory, ref_memory_level,
                    memory_level=2, ignore=['copy'])(
                        niimgs,
                        target_affine=mask_img_.get_affine(),
                        target_shape=mask_img_.shape,
                        copy=copy)

    # Load data (if filenames are given, load them)
    if verbose > 0:
        print("[%s] Loading data from %s" % (
            class_name,
            _utils._repr_niimgs(niimgs)[:200]))

    # Get series from data with optional smoothing
    if verbose > 1:
        print("[%s] Masking and smoothing" % class_name)
    data = masking.apply_mask(niimgs, mask_img_,
                              smoothing_fwhm=parameters['smoothing_fwhm'])

    # Temporal
    # ========
    # Detrending (optional)
    # Filtering
    # Confounds removing (from csv file or numpy array)
    # Normalizing

    if verbose > 1:
        print("[%s] Cleaning signal" % class_name)
    if not 'sessions' in parameters or parameters['sessions'] is None:
        clean_memory_level = 2
        if (parameters['high_pass'] is not None
                and parameters['low_pass'] is not None):
            clean_memory_level = 4

        data = cache(signal.clean, memory, ref_memory_level,
                     memory_level=clean_memory_level)(
                        data,
                        confounds=confounds, low_pass=parameters['low_pass'],
                        high_pass=parameters['high_pass'],
                        t_r=parameters['t_r'],
                        detrend=parameters['detrend'],
                        standardize=parameters['standardize'])
    else:
        sessions = parameters['sessions']
        for s in np.unique(sessions):
            if confounds is not None:
                confounds = confounds[sessions == s]
            data[sessions == s, :] = \
                cache(signal.clean, memory, ref_memory_level, memory_level=2)(
                        data[sessions == s, :],
                        confounds=confounds,
                        low_pass=parameters['low_pass'],
                        high_pass=parameters['high_pass'],
                        t_r=parameters['t_r'],
                        detrend=parameters['detrend'],
                        standardize=parameters['standardize']
                )

    # For _later_: missing value removal or imputing of missing data
    # (i.e. we want to get rid of NaNs, if smoothing must be done
    # earlier)
    # Optionally: 'doctor_nan', remove voxels with NaNs, other option
    # for later: some form of imputation

    return data, niimgs.get_affine()
