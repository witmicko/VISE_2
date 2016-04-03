import numpy as np
xp2 = [296.0, 244.0, 204.0, 173.0, 148.0, 126.0, 103.0, 78.0]
xp = xp2[::-1]
fp2 = [10.0,  30.0,  50.0,  70.0,  90.0,  110.0, 130.0, 150.0]
fp = fp2[::-1]
yy = np.array
x = np.interp(244.0, xp=xp, fp=fp, period=360)
print(x)
