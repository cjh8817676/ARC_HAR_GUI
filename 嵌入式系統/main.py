import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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


data_name = "Walking_right91"
columns = ['user', 'activity', 'timestamp', 'x-axis', 'y-axis', 'z-axis']
df_har = pd.read_csv(f'../{data_name}.txt', header=None, names=columns)
df_har = df_har.dropna()
df = df_har[df_har['timestamp'] != 0]
df = df.sort_values(by=['user', 'timestamp'], ignore_index=True)
activities = ['Walking']
for index, i in enumerate(activities):
    # plt.subplot(2,3,index+1)
    data36 = df[(df['user'] == 18) & (df['activity'] == i)][:]

# sample rate: 119hz
# b = [
#     0.00885425387835770, 0.0137493826554715, 0.0274888535961056,
#     0.0483032392489433, 0.0728372897377215, 0.0967921500066679,
#     0.115791366464563, 0.126283193657644, 0.126283193657644, 0.115791366464563,
#     0.0967921500066679, 0.0728372897377215, 0.0483032392489433,
#     0.0274888535961056, 0.0137493826554715, 0.00885425387835770
# ]

# sample rate: 50hz
b = [
    -0.00471176836965914, -0.00482758937955231, -0.00520880682926177,
    -0.00604086022606615, -0.00583949526972992, -0.00406362873876691,
    2.3701923210152e-18, 0.00685159196374912, 0.0166649335666207,
    0.0292159358894133, 0.0438671932652295, 0.0596142483286541,
    0.0751895963188574, 0.0892111597395131, 0.100352057014991,
    0.107524228069510, 0.109998113892460, 0.107524228069510, 0.100352057014991,
    0.0892111597395131, 0.0751895963188574, 0.0596142483286541,
    0.0438671932652295, 0.0292159358894133, 0.0166649335666207,
    0.00685159196374912, 2.3701923210152e-18, -0.00406362873876691,
    -0.00583949526972992, -0.00604086022606615, -0.00520880682926177,
    -0.00482758937955231, -0.00471176836965914
]
# print(data36['x-axis'][:])
data36 = data36['y-axis'].to_numpy()

sample50 = pd.read_csv("Walking_180_20220607081043.txt",
                       header=None).to_numpy()

plt.plot(sample50[:, 1])
plt.show()
sample50 = sample50[:, 1] * 4 / 32768

filterd = np.convolve(sample50, b, mode='full')

enlarging = np.copy(filterd)
enlarging = enlarging / 10
enlarging = np.power(enlarging, 2)

norm = np.copy(enlarging)
norm = normalize(norm)

diff = np.copy(norm)
diff = np.diff(diff, 1)
diff = np.power(diff, 2)

ma = moving_average(diff, 8)

# print(data36[3000:4000])
# print(filterd[3000:4000])
# plt.plot(data36[3000:3500], label="source")
# plt.plot(filterd[3000:3500], label="filterd")
# plt.legend()
# plt.show()
# plt.plot(enlarging[3000:3500], label="enlarging")
# plt.plot(norm[3000:3500], label="norm")
# plt.legend()
# plt.show()
plt.plot(diff[3000:3500], label="diff")
plt.plot(ma[3000:3500], label="ma")
plt.legend()
plt.show()
np.savetxt('./output/preprocessed.csv', ma[2900:3400], delimiter=",")

# ma[3000:3500].to_csv("./output/preprocessed.csv")
plt.plot(data36[3000:3500], label="source")
plt.title(f"{data_name}_y_axis")
plt.xlabel("sample rate: 119Hz")
# plt.show()
plt.savefig("./output/source.png")
plt.close('')
plt.plot(ma[3000:3500], label="ma")
plt.title(f"{data_name}_preprocessed")
plt.xlabel("sample rate: 119Hz")
# plt.show()
plt.savefig("./output/preprocessed.png")
plt.close('')
# plt.plot(ma[3000:4000], label="ma")
# plt.show()

step = []
count = 0
max = 0
p = 0
WINDOW_SIZE = 70
SHIFT_LEN = 20
# init max
for i in range(WINDOW_SIZE):
    if max < ma[i]:
        max = ma[i]
        p = i
step.append(p)
count = p + SHIFT_LEN
max = max * 0.3
while count < len(ma) - WINDOW_SIZE:
    first = 0
    for i in range(WINDOW_SIZE):
        if max < ma[count + i]:
            max = ma[count + i]
            p = count + i
            first = 1
    if first == 0:
        count = count + WINDOW_SIZE
        print('a')
    else:
        count = p + SHIFT_LEN
        max = max * 0.3
        step.append(p)
        print('b')

    first = 0
first = 0
max = max * 1.5
for i in range(count, len(ma)):
    if max < ma[i]:
        first = 1
        max = ma[i]
        p = i
if first == 1:
    step.append(p)
print(step)
print(len(step))
plt.title(f"{data_name}")
plt.plot(ma)
plt.plot(step, ma[step], 'or')
plt.plot(step, ma[step] * 0.3, 'og')
plt.show()