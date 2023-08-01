import os.path
import numpy as np
import spectral
from numpy import uint8
from osgeo import gdal
from spectral import envi


def set_byte_order(hdr_file):
    lines = ""
    with open(hdr_file, mode='r', encoding='utf-8') as f:
        line = f.readline()
        while line != "":
            if line.startswith("Wayho"):
                line = "ENVI\n"
            if not line.startswith("ModuleName"):
                lines += line
            line = f.readline()
        if "byte order" not in lines:
            lines += "\nbyte order = 0"
    with open(hdr_file, mode='w', encoding='utf-8') as f:
        f.writelines(lines)


# 读取高光谱文件
def read_img(file_name, set_data_type=True, postfix='.img'):
    file_name = file_name[:-4]
    if set_data_type:
        set_byte_order(file_name + '.hdr')
    try:
        spectral.settings.envi_support_nonlowercase_params = True
        img = envi.open(file_name + '.hdr', file_name + postfix)
    except envi.EnviDataFileNotFoundError:
        print(file_name + ' can not be opened.')
    else:
        return img


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


def get_img(img, bands, height, width):
    with open(img, "rb") as img_file01:
        hyperion_data1 = np.fromfile(img_file01, dtype=uint8)
    img_file01.close()
    # 将一维数据转换为三维数组
    res01 = hyperion_data1.reshape(bands, height, width)

    return res01


if __name__ == '__main__':
    file_dir = "./data/"
    hdr_name = "light_intensity.hdr"
    img_name = "light_intensity.img"
    hdr_path = os.path.join(file_dir, hdr_name)
    img_path = os.path.join(file_dir, img_name)

    data = read_img(file_name=img_path)
    # data = envi.open(hdr_path, img_path)
    # img = spectral.envi.open(hdr_path, img_path)
    print("end")
