import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
import numpy as np
from ecgdetectors import Detectors
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w
def normalize(x):
  max = 0
  min = 999999
  for i in range(len(x)):
    if x[i] > max:
      max = x[i]
    if x[i] < min:
      min = x[i]
  for i in range(len(x)):
    x[i] = (x[i] - min) / max

  return x

detectors = Detectors(119)
columns = ['user','activity','timestamp', 'x-axis', 'y-axis', 'z-axis']
df_har = pd.read_csv('Walking_right91.txt', header = None, names = columns)
print(df_har[0:2])
print(df_har.size)
# removing null values
df_har = df_har.dropna()
print(df_har.shape)
# transforming the z-axis to float
# df_har['z-axis'] = df_har['z-axis'].str.replace(';', '')
# df_har['z-axis'] = df_har['z-axis'].apply(lambda x:float(x))
# drop rows where timestamp is 0
df = df_har[df_har['timestamp'] != 0]
# arrange data in ascending order of user and timestamp
df = df.sort_values(by = ['user', 'timestamp'], ignore_index=True)
print(df)
activities=['Walking']
plt.figure(figsize=(12, 10))
for index,i in enumerate(activities):
  # plt.subplot(2,3,index+1)
  data36=df[(df['user']==18)&(df['activity']==i)][:]
#   print(data36)
#   sns.lineplot(y='x-axis',x=range(3000) ,data=data36)
#   sns.lineplot(y='y-axis',x=range(3000) ,data=data36)
#   sns.lineplot(y='z-axis',x=range(3000) ,data=data36)
#   plt.legend(['x-axis','y-axis','z-axis'])
#   plt.ylabel(i)
#   plt.title(i,fontsize=15)
#   plt.savefig(i+'.png')
  
#   plt.show()
# plt.show()
# b = [-0.0027,-0.0018,0.0034,0.0209,0.0551,0.1017,0.1475,0.1760,0.1760,0.1475,0.1017,0.0551,0.0209,0.0034,-0.0018,-0.0027]
# b = [-0.0022,-0.0045,0.0088,0.0211,-0.0362,-0.0718,0.1346,0.4501,0.4501,0.1346,-0.0718,-0.0362,0.0211,0.0088,-0.0045,-0.0022]
b = [0.00885425387835770,0.0137493826554715,0.0274888535961056,0.0483032392489433,0.0728372897377215,0.0967921500066679,0.115791366464563,0.126283193657644,0.126283193657644,0.115791366464563,0.0967921500066679,0.0728372897377215,0.0483032392489433,0.0274888535961056,0.0137493826554715,0.00885425387835770]
print(data36['x-axis'][:])
plt.plot(data36['y-axis'][:3000])
plt.show()
filterd = np.convolve(data36['y-axis'][:], b, mode='full')
plt.plot(filterd[120:])
plt.show()
# a = filterd[120:]
# plt.plot(a)
# plt.plot(r_peaks,a[r_peaks],'or')
# plt.show()
# ma = moving_average(filterd,8)
ma = filterd
plt.plot(ma[120:])
plt.show()
for i in range(len(ma)):
  ma[i] = ma[i] / 10
  ma[i] = ma[i] * ma[i]
plt.plot(ma[120:])
plt.show()
xint = []
sum = 0
for i in range(len(ma)-8):
  sum = 0
  for j in range(8):
    sum = sum + ma[i+j]
  xint.append(sum)
xint = normalize(xint)
plt.plot(xint[120:])
plt.show()
diff1 = np.diff(xint,1)
plt.plot(diff1[120:])
plt.show()
# for i in range(len(diff1)):
#   if diff1[i] < 0:
#     diff1[i] = 0
r_peaks = detectors.pan_tompkins_detector(xint[120:])
plt.plot(np.power(diff1[120:],2))
plt.show()
diff2 = np.power(diff1,2)
ma = moving_average(diff2,8)
plt.plot(ma)
plt.show()

step = []
count = 0
max = 0
p = 0
for i in range(150):
  if max < ma[i]:
    max = ma[i]
    p = i
step.append(p)
count = p + 45
max = max * 0.3
while count < len(ma) - 150:
  first = 0
  for i in range(150):
    if max < ma[count + i]:
      max = ma[count + i]
      p = count + i
      first = 1
  if first ==0:
    count = count + 150
    print('a')
  else:
    count = p + 40
    max = max * 0.3
    step.append(p)
    print('b')

  first = 0
first = 0
max = max * 2.5 * 0.6
for i in range(count,len(ma)):
  if max < ma[i]:
    first = 1
    max = ma[i]
    p = i
if first == 1:
  step.append(p)
print(step)
plt.title("Walking_right91")
plt.plot(ma)
plt.plot(step,ma[step],'or')
plt.plot(step,ma[step] * 0.4,'og')
plt.show()

    
