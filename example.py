# -*- coding: utf-8 -*-
"""
SHADOW CASTING ALGORITHM EXAMPLE USING PYTHON-DEM-SHADOWS

Dec 2023
Fabio Oriani, fabio.oriani <at> protonmail.com

"""
#%% DEPENDENCIES
import python_dem_shadows.shadows as sh
import python_dem_shadows.solar as so
import matplotlib.pyplot as plt
import rasterio 
import numpy as np
import datetime as dt
from osgeo import ogr
from osgeo import osr

# function for color rescale in a multiband image
def imrisc(im_in,qmin,qmax):
    im_out=im_in.copy()
    for i in range(np.shape(im_in)[2]):
        band=im_in[:,:,i].copy()
        band2=band[~np.isnan(band)]
        vmin=np.percentile(band2,qmin)
        vmax=np.percentile(band2,qmax)
        band[band<vmin]=vmin
        band[band>vmax]=vmax
        band=(band-vmin)/(vmax-vmin)
        im_out[:,:,i]=band
    return im_out

#%% IMPORT TEST DEM IMAGE AND ONE SAT IMAGE (TO CHECK THE CAST SHADOWS)

filename = "data/test_image.tif" # test SAT image
dataset = rasterio.open(filename)
im_extent = dataset.bounds # image limits
im_extent = [im_extent[0],im_extent[2],im_extent[3],im_extent[1]] # good order for plt.imshow
#im_crs = dataset.crs # CRS (same as dem)
im = dataset.read([3,2,1]).transpose([1,2,0]) # multiband raster
im = np.flipud(imrisc(im,3,97))
dataset = None

filename = "data/test_dem.tif" # test DEM image
dataset = rasterio.open(filename)
dem_extent = dataset.bounds # image limits
dem_extent = [dem_extent[0],dem_extent[2],dem_extent[3],dem_extent[1]] # good order for plt.imshow
dem_crs = int(dataset.crs.data['init'][5:]) # CRS code
dem_res = dataset.transform[0] # spatial resolution
dem_xllc = dataset.transform[2] # lower left corner x coord
dem_yllc = dataset.transform[5] # lower left corner y coord
dem_nrows = dataset.height # raster rows
dem_ncols = dataset.width # taster columns
dem = dataset.read(1) # raster
dem = np.flipud(dem)
dataset = None

# display the images
plt.figure(figsize=(8,4)) 
plt.subplot(121)
plt.imshow(im, extent =  im_extent )
plt.title('Landscape RGB')
plt.subplot(122)
plt.imshow(dem, extent = dem_extent)
plt.title('DEM')
plt.tight_layout

#%% COMPUTE THE CAST SHADOW

# a wrapper function to generate the shadow mask
def shadow_mask(dem,lon,lat,date,tzone,dx): 
    jd=so.to_juliandate(d) # transform date to julian date
    sun_vector= so.sun_vector(jd,lat,lon,tzone) # compute the sun position vector
    shad=sh.project_shadows(dem, sun_vector, dx, dy=dx)  # compute cast shadow
    shad[shad==1]=np.nan # make a mask (1 = shadow, nan elsewhere) OPTIONAL
    shad[shad==0]=1
    return shad
    
# image center grid coordinates in WGS84 as reference point for the image location    
cx=dem_xllc+dem_res*int(dem_ncols/2) # center coords 
cy=dem_yllc+dem_res*int(dem_nrows/2)
Point = ogr.Geometry(ogr.wkbPoint) # point object
Point.AddPoint(cx,cy)
InSR = osr.SpatialReference() # target crs WGS84
InSR.ImportFromEPSG(dem_crs) 
Point.AssignSpatialReference(InSR) # assign image crs
OutSR = osr.SpatialReference() # target crs WGS84
OutSR.ImportFromEPSG(4326) 
Point.TransformTo(OutSR)  # transform coords to WGS84
lon=Point.GetY() # get transformed coords
lat=Point.GetX()

# time params
d=dt.datetime(2009,8,6,9,59,30) # acquisition date and time from im metadata
tzone=0 # time zone of the caquisition date (here Zulu = UTM 0)

# shadow computation
shad = shadow_mask(dem,lon,lat,d,tzone,dem_res)

# display the shadow over the image
plt.figure()
plt.imshow(im)
plt.imshow(shad,alpha=0.5)
plt.title('Cast shadow over Landscape')