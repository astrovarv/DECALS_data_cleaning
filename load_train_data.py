#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 10:55:47 2020

@author: Varvara Semenova & Rahul Gupta
"""

import astropy.io.fits as fits
from astropy.table import Table, hstack, vstack
import pandas as pd

target_url1 = 'https://portal.nersc.gov/project/cosmo/data/legacysurvey/dr8/south/external/survey-dr8-south-specObj-dr14.fits'
dat = fits.open(target_url1)
target_url2 = 'https://portal.nersc.gov/project/cosmo/data/legacysurvey/dr8/north/external/survey-dr8-north-specObj-dr14.fits'
dat2 = fits.open(target_url2)
print('Loading photometry (South)...')
photometric_data_south = Table.read(dat) # south
print('Loading photometry (North)...')
photometric_data_north = Table.read(dat2) # north

print('Adding HEMISPHERE column...')
photometric_data_north['HEMISPHERE'] = 'N'
photometric_data_south['HEMISPHERE'] = 'S'

#%%
# merge
print('Merging...')
ind = photometric_data_south['OBJID'] == -1
photometric_data_south[ind] = photometric_data_north[ind]
del photometric_data_north
photometric_data = photometric_data_south

# the SDSS spectroscopy file needs to be downloaded in advance from
# https://data.sdss.org/sas/dr14/sdss/spectro/redux/specObj-dr14.fits 
#%%
print('Loading spectroscopy...')
spectroscopic_data = Table.read('specObj-dr14-new.fits')

#%%
print('Cutting columns...')   

photometric_data.keep_columns(['FLUX_G','FLUX_R','FLUX_Z','FLUX_W1','FLUX_W2',\
                               'FLUX_W3','FLUX_W4','FLUX_IVAR_G','FLUX_IVAR_R',\
                               'FLUX_IVAR_Z','FLUX_IVAR_W1','FLUX_IVAR_W2',\
                               'FLUX_IVAR_W3','FLUX_IVAR_W4','MW_TRANSMISSION_G',\
                               'MW_TRANSMISSION_R','MW_TRANSMISSION_Z','MW_TRANSMISSION_W1',\
                               'MW_TRANSMISSION_W2','MW_TRANSMISSION_W3','MW_TRANSMISSION_W4',\
                               'RA', 'DEC','NOBS_G','NOBS_R', 'NOBS_Z', 'NOBS_W1',\
                               'NOBS_W2', 'MASKBITS', 'TYPE', 'ANYMASK_G', 'ANYMASK_R',\
                                   'ANYMASK_Z', 'ALLMASK_G', 'ALLMASK_R',\
                                   'ALLMASK_Z', 'FRACMASKED_G', 'FRACMASKED_R', \
                                'FRACMASKED_Z', 'FRACIN_G', 'FRACIN_R', 'FRACIN_Z',
                                'FRACFLUX_G', 'FRACFLUX_Z', 'FRACFLUX_R', 'FRACFLUX_W1',
                                'FRACFLUX_W2', 'WISEMASK_W1', 'WISEMASK_W2',
                                'PSFDEPTH_R', 'PSFDEPTH_G', 'PSFDEPTH_Z',
                                'PSFDEPTH_W1', 'PSFDEPTH_W2', 'HEMISPHERE'])

spectroscopic_data.keep_columns(['CLASS','SUBCLASS','Z','Z_ERR','ZWARNING','SURVEY',\
                                'INSTRUMENT', 'COMMENTS_PERSON', 'CLASS_PERSON', \
                                    'PROGRAMNAME', 'PLATEQUALITY', 'PLATESN2', 'ZOFFSET'])    

 
# save the tables separately if needed:
#%%   
# print('Saving photometry...')  
# photometric_data.write('specObj-dr14-photometry-new.csv', format = 'ascii.csv', overwrite = True)
# print('Saving spectroscopy...')
# spectroscopic_data.write('specObj-dr14-spectroscopy-new.csv', format = 'ascii.csv', overwrite = True)

# then stack horizontally together
print('Converting photometry to pandas...')
photo = photometric_data.to_pandas()
print('Converting spectroscopy to pandas...')
spec = spectroscopic_data.to_pandas()

print('Merging...')
data = pd.concat([photo, spec], axis = 1)

#%%  
print('Saving...')
data.to_csv('all_objects.csv', index = False)

