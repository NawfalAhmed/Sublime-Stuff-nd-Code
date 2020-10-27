import matplotlib.pyplot as plt
import numpy as np
mrks = [
	'90.12', '82.12', '81.30', '78.87', '77.60', '77.21', '76.39', '76.10',
	'75.80', '75.23', '74.63', '74.08', '73.82', '73.20', '72.98', '72.86',
	'72.45', '72.41', '71.92', '71.86', '71.72', '70.47', '70.28', '70.06',
	'69.10', '67.49', '67.13', '66.55', '66.52', '65.93', '65.40', '65.35',
	'64.98', '64.88', '64.27', '64.18', '64.05', '63.90', '63.85', '63.57',
	'62.28', '62.23', '61.58', '61.19', '60.87', '60.79', '56.79', '55.63',
	'54.36', '54.07', '53.17', '51.30', '50.87', '49.64', '49.15', '49.15',
	'44.20', '39.64', '38.56', '34.86', '22.02', '21.99', '20.55', '17.19',
	'15.93', '09.92', '02.63', '01.46', '00.00', '00.00'
]
ids = [
	'01', '47', '14', '29', '15', '22', '54', '03', '10', '26', '50', '51', '23',
	'02', '40', '34', '28', '37', '38', '17', '55', '72', '09', '36', '08', '53',
	'57', '19', '32', '21', '24', '31', '69', '39', '13', '45', '56', '25', '61',
	'62', '04', '42', '41', '64', '58', '70', '63', '12', '59', '43', '44', '33',
	'30', '52', '49', '68', '48', '74', '11', '31', '73', '46', '71', '07', '66',
	'65', '75', '27', '16', '20'
]
mrks = [int(float(x)) for x in mrks]
#print(mrks,ids)
npmarks = np.array(mrks)
npid = np.array(ids)
dd = np.column_stack((npmarks, npid))
print(dd)

plt.xlabel("BSCS18--")
plt.ylabel("Marks")
plt.scatter(npid, npmarks)
plt.yticks([x for x in range(0, 101, 5)])
plt.show()
