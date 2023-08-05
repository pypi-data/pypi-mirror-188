from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import gc

#读图像文件
def read_img(filename):
    dataset = gdal.Open(filename) #打开文件
    im_width = dataset.RasterXSize  #栅格矩阵的列数
    im_height = dataset.RasterYSize  #栅格矩阵的行数
    im_bands = dataset.RasterCount   #波段数
    im_geotrans = dataset.GetGeoTransform()  #仿射矩阵，左上角像素的大地坐标和像素分辨率
    im_proj = dataset.GetProjection() #地图投影信息，字符串表示
    im_data = dataset.ReadAsArray(0,0,im_width,im_height).astype('float')
 
    del dataset 
 
    return im_width, im_height, im_bands, im_proj, im_geotrans, im_data


    #写GeoTiff文件
def write_img(filename, im_proj, im_geotrans, im_data):
 
    #判断栅格数据的数据类型
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
 
    #判读数组维数
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
       im_bands, (im_height, im_width) = 1, im_data.shape
 
    #创建文件
    driver = gdal.GetDriverByName("GTiff") 
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)
 
    dataset.SetGeoTransform(im_geotrans)       #写入仿射变换参数
    dataset.SetProjection(im_proj)          #写入投影
 
    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data) #写入数组数据
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i+1).WriteArray(im_data[i])
 
    del dataset