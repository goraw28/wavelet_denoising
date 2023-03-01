import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pywt
import glob
from statistics import pvariance

final_list = []
header_list = ['MLII', 'Value', 'VALUE', 'ECG', '0', 'val','V1', 'II', 'noise1', 'noise2','ii']

for i in glob.glob('C:\\Users\\x\\Desktop\\x\\All_files_check\\gdfdh\\*.csv'):
    name = i.split("\\")[-1].split(".csv")[0] 
    # print(i)
    print(name)
    # print(i)
    # count = 0
    # k = 0
    # l= 3750
    
    for header in header_list:
        try:
            df1 = pd.read_csv(i)[header]
        except:
            pass
    
    initial_file = df1.iloc[0:3750]

    # Generate an ECG signal with added high frequency noise
    fs = 700  # Sample rate
    # Perform Wavelet denoising
    coeffs = pywt.wavedec(initial_file, 'db4', level=5)  # Perform wavelet decomposition
    threshold = 20* np.median(np.abs(coeffs[-1]))  # Threshold for denoising
    coeffs_denoised = [pywt.threshold(c, value=threshold, mode='soft') for c in coeffs]  # Denoise the coefficients
    x_filtered = (pywt.waverec(coeffs_denoised, 'db4')*1)
    l = initial_file.shape[0] if initial_file.shape[0] < x_filtered.shape[0] else x_filtered.shape[0]
    z = (initial_file[:l] - x_filtered[:l])
    zz =np.std(z)
    # zzz =pd.DataFrame(zz).to_csv(f'C:\Users\x\Desktop\test_to\{}')
    print(zz)

    # fig, axes = plt.subplots(3, 1, sharex=True)
    # fig.subplots_adjust(hspace=0)
    # axes[0].plot(initial_file, c='r', label='original data')
    # axes[0].legend()
    # axes[1].plot(x_filtered,c='g',label='filter-1')
    # axes[1].legend()
    # axes[2].plot(z,c='b',label='filter-1')
    # axes[2].legend()
    # plt.show()
    final_list.append({"filename":name,"std":zz})
rtr  =pd.DataFrame(final_list)
rtr.to_csv('C:\\Users\\x\\Desktop\\x\\check.csv',index=False)