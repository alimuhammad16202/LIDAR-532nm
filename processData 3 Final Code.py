import numpy as np
import os
import matplotlib.pyplot as plt

######################## backgroundCorrection function #########################

def backgroundCorrection(t_data_content, loc_VIP_list):
    data_start_loc, data_end_loc, bg_start_loc, bg_end_loc = loc_VIP_list
    data_wanted = t_data_content[data_start_loc: data_end_loc]
    data_background = \
      t_data_content[bg_start_loc: bg_end_loc].mean(axis = 0).tolist()
    dataBgC = data_wanted - data_background
    return dataBgC

######################## rangeCorrection function ##############################

def rangeCorrection(dataBgC, h_data, loc_VIP_list):
    ## h_data 'm', so we /1000 to 'km'
    data_start_loc, data_end_loc, _, _ = loc_VIP_list
    standard_h_data = h_data[data_start_loc: data_end_loc] / 1000
    dataRC = dataBgC * standard_h_data * standard_h_data
    return dataRC


###########读取数据文件##############

topDir = 'Peshawar'
dataChannelList = ['532p', '532s', ]
targetDate = '20240801'
loc_VIP_list = [0, 2666, 6666, 8000]
dataNum = 100000 #100000 #1
polorK = 1
timeStrT = '202408010312'


dataDict = {}
##for date in dateList:
    
dataDict[targetDate] = {}
for dataChannel in dataChannelList:
    print(f'dataChannel = {dataChannel}')
    dataDir = f'{topDir}/{dataChannel}/{targetDate}'
    if os.path.exists(f'result/{dataChannel}_correction') == 0:
        os.makedirs(f'result/{dataChannel}_correction')
##    num = 0
    for file in os.listdir(dataDir):
        timeStr = file[: 12]
##        if timeStr != timeStrT:
##            continue
##        num += 1
##        if num > dataNum:
##            continue
        if timeStr not in dataDict[targetDate]:
            dataDict[targetDate][timeStr] = {}
        dataPath = f'{dataDir}/{file}'
##        print(f'{dataPath} is found')
        dataAllContent = np.loadtxt(dataPath)
        heightAll = dataAllContent.T[0]
        dataContent = dataAllContent.T[1]
##        dataDict[targetDate][timeStr][f'{dataChannel}_raw_data'] = dataContent
##        dataDict[targetDate][timeStr][f'{dataChannel}_raw_height'] = heightAll
##        print(f'dataAllContent = {dataAllContent}')
##        print(f'heightAll = {heightAll}')
##        print(f'dataContent = {dataContent}')
##        plt.plot(heightAll, dataContent)
##        plt.ylim(0.012, 0.013)
##        plt.xlim(0, 30000)
##        plt.show()
        # for correction
        height = heightAll[loc_VIP_list[0]: loc_VIP_list[1]]
        dataBgC = backgroundCorrection(dataContent, loc_VIP_list)
##        print(f'dataBgC = {dataBgC}')
##        plt.plot(height, dataBgC)
##        plt.ylim(0, 0.00001)
##        plt.xlim(1000, 10000)
##        plt.show()
        dataRC = rangeCorrection(dataBgC, height, loc_VIP_list)
##        print(f'dataRC = {dataRC}')
##        plt.plot(height, dataRC)
##        plt.ylim(0, 0.00001)
##        plt.xlim(1000, 10000)
##        plt.show()
        dataDict[targetDate][timeStr][f'{dataChannel}_correction_data'] = dataRC
##        dataDict[targetDate][timeStr][f'{dataChannel}_correction_height'] = height
##        print(f'dataDict = {dataDict}')
        resultPath = f'result/{dataChannel}_correction/{timeStr}.txt'
        np.savetxt(resultPath, dataRC, '%.16f')

##print(f'dataDict = {dataDict}')


if os.path.exists(f'result/figs') == 0:
    os.makedirs(f'result/figs')
if os.path.exists(f'result/total_backscatter_intensity') == 0:
    os.makedirs(f'result/total_backscatter_intensity')
if os.path.exists(f'result/volume_depolorization_ratio') == 0:
    os.makedirs(f'result/volume_depolorization_ratio')
for date in dataDict:
##    print(f'date = {date}')
    for time in dataDict[date]:
        
##        if '532p_correction_height' not in dataDict[date]:
##            print(f'111 time = {time}')
##            continue
        if '532p_correction_data' not in dataDict[date][time]:
            print(f'222 time = {time}')
            continue
        elif '532s_correction_data' not in dataDict[date][time]:
            print(f'333 time = {time}')
            continue
##        height = dataDict[date][time]['532p_correction_height']
        # for total_backscatter_intensity
        dataTBI = dataDict[date][time]['532p_correction_data'] + \
                  polorK * dataDict[date][time]['532s_correction_data']
        resultPath = f'result/volume_depolorization_ratio/{time}.txt'
        np.savetxt(resultPath, dataTBI, '%.16f')
        plt.plot(height, dataTBI)
        plt.savefig(f'result/figs/tbi_{time}.png')
##        plt.show()
        # for volume_depolorization_ratio
        dataVdr = polorK * dataDict[date][time]['532s_correction_data'] / \
                  dataDict[date][time]['532p_correction_data']
        resultPath = f'result/volume_depolorization_ratio/{time}.txt'
        np.savetxt(resultPath, dataVdr, '%.16f')
        plt.plot(height, dataVdr)
        plt.savefig(f'result/figs/vdr_{time}.png')
##        plt.show()






