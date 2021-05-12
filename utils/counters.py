# dependencies
from PIL import Image
import numpy as np
import os

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

def count_pixels(SystemClass, params, file_path, imgs_path='imgs/sys_00/tmin_tmax_tdim', x_prec=4, y_prec=4):
    """Function to count the pixels in quadrature dynamics.

    Parameters
    ----------
    SystemClass : :class:`qom.systems.*`
        Class containing the system.
    params : dict
        Parameters for the system.
    file_path : str
        Path and prefix of the .npz file.
    imgs_path : str, optional
        Path and prefix of the .png files.
    x_prec : int, optional
        Decimal precision for the X-axis variable.
    y_prec : int, optional
        Decimal precision for the Y-axis variable.  
    
    Returns
    -------
    Counts : list
        Pixel counts for each point.
    """
    
    # initialize logger
    init_log()

    # system
    system = SystemClass(params['system'])

    # complete filename
    X = params['looper']['X']
    for key in X:
        file_path += '_' + str(X[key])
    x_var = X['var']
    x_vals = np.around(np.linspace(X['min'], X['max'], X['dim']), x_prec).tolist()
    Y = params['looper']['Y']
    for key in Y:
        file_path += '_' + str(Y[key])

    # if file exists
    if os.path.isfile(file_path + '.npz'):
        Counts = np.load(file_path + '.npz')['arr_0'].tolist()
    
    else:
        y_var = Y['var']
        y_vals = np.around(np.linspace(Y['min'], Y['max'], Y['dim']), y_prec).tolist()

        # pixel counts
        Counts = list()
        for y_val in y_vals:
            counts = list()
            for x_val in x_vals:
                system.params[x_var] = x_val
                system.params[y_var] = y_val
                filename_img = ''
                for key in system.params:
                    filename_img += '_' + str(system.params[key])

                # if file does not exist
                if not os.path.isfile(imgs_path + filename_img + '.png'):
                    # measure
                    M = system.get_measure_dynamics(params['solver'], system.ode_func, system.ivc_func)
                    _xs = np.real(np.transpose(M)).tolist()[0]
                    _ys = np.imag(np.transpose(M)).tolist()[0]

                    # plot and save
                    plotter = MPLPlotter({
                        'X': _xs
                    }, params['plotter'])
                    plotter.update(xs=_xs, vs=_ys)
                    plotter.save(imgs_path + filename_img + '.png')

                # load image
                im = Image.open(imgs_path + filename_img + '.png')
                # count blue pixels
                count = 0
                for pixel in im.getdata():
                    if not pixel[0] == pixel[1] and not pixel[1] == pixel[2]:
                        count += 1

                # progress
                print('\r{}={}, {}={}, count={}'.format(x_var, x_val, y_var, y_val, count), end='\t\t')

                counts.append(count)
            Counts.append(counts)

        # save counts
        np.savez_compressed(file_path, np.array(Counts))
    
    return Counts

    