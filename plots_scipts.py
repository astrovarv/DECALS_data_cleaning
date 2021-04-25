import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def flux_to_mag(flux, gal_ext, cor = 0, AB = 0):
  """
  Coversion from nanomaggies to AB-magnitudes, taking galactic extinction 
  into account.
  """
  if cor==0 and AB==1:
    mag=22.5 - 2.5*np.log10(flux)
  elif cor==1 and AB==1:
    mag=22.5 - 2.5*np.log10(flux/gal_ext)
  elif cor==1 and AB==0:
    mag=flux/gal_ext
  return mag
        
def hist2d(df, object):
  """
  Plotting a 2D colour-colour histogram for a number of different colours.
  """
  qsos = df[df['CLASS'] == 'QSO']
  stars = df[df['CLASS'] == 'STAR']

  fig, ax = plt.subplots(1,5, figsize = [20, 5])
  if object == 'qsos':
    hist = ax[0].hist2d(qsos['AB_FLUX_G'] - qsos['AB_FLUX_R'],
                  qsos['AB_FLUX_R'] - qsos['AB_FLUX_Z'], bins = 50,
                  cmap = 'YlOrRd', norm = matplotlib.colors.LogNorm())
    ax[1].hist2d(qsos['AB_FLUX_G'] - qsos['AB_FLUX_R'],
                  qsos['AB_FLUX_Z'] - qsos['AB_FLUX_W1'], bins = 50,
                  cmap = 'YlOrRd', norm = matplotlib.colors.LogNorm())
    ax[2].hist2d(qsos['AB_FLUX_Z'] - qsos['AB_FLUX_R'],
                  qsos['AB_FLUX_R'] - qsos['AB_FLUX_W1'], bins = 50,
                  cmap = 'YlOrRd', norm = matplotlib.colors.LogNorm())
    ax[3].hist2d(qsos['AB_FLUX_G'] - qsos['AB_FLUX_R'],
              qsos['AB_FLUX_W1'] - qsos['AB_FLUX_G'], bins = 50,
              cmap = 'YlOrRd', norm = matplotlib.colors.LogNorm())  
    ax[4].hist2d(qsos['AB_FLUX_G'] - qsos['AB_FLUX_R'],
        qsos['AB_FLUX_W2'] - qsos['AB_FLUX_R'], bins = 50,
        cmap = 'YlOrRd', norm = matplotlib.colors.LogNorm())        

  else:
    hist = ax[0].hist2d(stars['AB_FLUX_G'] - stars['AB_FLUX_R'],
              stars['AB_FLUX_R'] - stars['AB_FLUX_Z'], bins = 50,
              cmap = 'Greys', norm = matplotlib.colors.LogNorm())
    ax[1].hist2d(stars['AB_FLUX_G'] - stars['AB_FLUX_R'],
            stars['AB_FLUX_R'] - stars['AB_FLUX_W1'], bins = 50,
            cmap = 'Greys', norm = matplotlib.colors.LogNorm())
    ax[2].hist2d(stars['AB_FLUX_Z'] - stars['AB_FLUX_R'],
            stars['AB_FLUX_R'] - stars['AB_FLUX_W1'], bins = 50,
            cmap = 'Greys', norm = matplotlib.colors.LogNorm())
    ax[3].hist2d(stars['AB_FLUX_G'] - stars['AB_FLUX_R'],
        stars['AB_FLUX_W1'] - stars['AB_FLUX_G'], bins = 50,
        cmap = 'Greys', norm = matplotlib.colors.LogNorm())   
    ax[4].hist2d(stars['AB_FLUX_G'] - stars['AB_FLUX_R'],
        stars['AB_FLUX_W2'] - stars['AB_FLUX_R'], bins = 50,
        cmap = 'Greys', norm = matplotlib.colors.LogNorm())     
  
  for i in range(len(ax)):
    ax[i].set_title(object)

  ax[0].set_xlabel(r'$g-r$')
  ax[0].set_ylabel(r'$r-z$')

  ax[1].set_xlabel(r'$g-r$')
  ax[1].set_ylabel(r'$z-w1$')

  ax[2].set_xlabel(r'$z-r$')
  ax[2].set_ylabel(r'$r-w1$')

  ax[3].set_xlabel(r'$g-r$')
  ax[3].set_ylabel(r'$w1-g$')

  ax[4].set_xlabel(r'$g-r$')
  ax[4].set_ylabel(r'$w2-r$')

  plt.colorbar(hist[3], label='Num. Density')
  plt.tight_layout()