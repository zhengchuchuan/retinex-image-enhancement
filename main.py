import os.path

from osgeo import gdal
import numpy as np


def read_img_file(path):
    # 打开文件
    dataset = gdal.Open(path)

    # 获取图像的通道数和尺寸
    num_channels = dataset.RasterCount
    width = dataset.RasterXSize
    height = dataset.RasterYSize

    # 逐通道读取图像数据
    channels = []
    for i in range(1, num_channels + 1):
        band = dataset.GetRasterBand(i)
        channel_data = band.ReadAsArray(0, 0, width, height)
        channels.append(channel_data)

    # 关闭图像文件
    dataset = None


if __name__ == '__main__':
    # tif_dir = "data/"
    # tif_name = "Reflectivity.img"
    # tif_path = os.path.join(tif_dir, tif_name)
    read_img_file("data/light intensity.img")
    print("end")
