import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.graphics.api as smg
from sklearn.preprocessing import RobustScaler
from math import log
from sklearn.metrics import average_precision_score,recall_score

# pd.options.display.float_format = '{:20,.3f}'.format
# pd.set_option('display.width', 170)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 1000) 

test_ind = [210, 117, 116, 146, 114, 364, 305, 730, 819, 893, 324, 670, 903, 74, 309, 955, 622, 757, 336, 790, 242, 873, 529, 747, 677, 655, 817, 661, 627, 516, 431, 97, 761, 430, 400, 287, 923, 338, 922, 335, 616, 25, 355, 217, 707, 131, 174, 692, 279, 280, 474, 455, 629, 669, 860, 656, 932, 554, 58, 124, 714, 829, 968, 120, 215, 254, 167, 675, 142, 892, 154, 78, 122, 492, 110, 90, 408, 221, 611, 597, 80, 71, 614, 915, 992, 662, 931, 347, 683, 538, 682, 73, 435, 824, 549, 550, 252, 238, 608, 756, 857, 372, 930, 79, 358, 738, 246, 163, 720, 476, 989, 650, 797, 140, 521, 543, 195, 326, 264, 107, 631, 138, 953, 787, 239, 443, 55, 445, 995, 987, 226, 380, 482, 964, 43, 13, 978, 41, 344, 694, 868, 885, 425, 958, 804, 731, 648, 660, 169, 632, 566, 18, 813, 214, 173, 636, 256, 76, 59, 779, 179, 417, 267, 997, 263, 229, 717, 96, 420, 166, 798, 235, 192, 472, 742, 5, 137, 567, 739, 250, 27, 385, 48, 184, 973, 754, 381, 874, 61, 784, 710, 884, 859, 276, 69, 232, 518, 846, 825, 193]
train_ind = [129, 303, 89, 807, 586, 172, 598, 602, 794, 53, 799, 679, 939, 391, 54, 162, 982, 438, 475, 198, 980, 398, 534, 357, 548, 681, 615, 288, 1, 178, 311, 354, 988, 849, 141, 605, 831, 285, 297, 165, 666, 157, 508, 111, 841, 741, 459, 863, 346, 593, 620, 490, 33, 186, 296, 446, 19, 805, 628, 785, 500, 663, 504, 379, 861, 402, 282, 427, 769, 333, 907, 921, 540, 882, 795, 527, 34, 727, 888, 112, 564, 81, 827, 377, 685, 470, 816, 786, 778, 213, 243, 734, 101, 765, 927, 733, 536, 85, 514, 647, 152, 881, 331, 156, 456, 858, 478, 258, 266, 985, 559, 125, 838, 935, 983, 386, 539, 28, 551, 396, 99, 843, 585, 170, 936, 618, 703, 10, 993, 205, 240, 190, 736, 589, 395, 542, 726, 147, 965, 38, 15, 981, 723, 835, 304, 556, 972, 918, 50, 528, 241, 47, 755, 604, 511, 175, 830, 233, 544, 780, 637, 294, 393, 908, 211, 132, 359, 772, 87, 561, 109, 760, 390, 594, 505, 812, 826, 92, 145, 572, 810, 133, 573, 67, 23, 716, 509, 796, 292, 623, 293, 415, 224, 153, 762, 187, 510, 405, 36, 896, 933, 6, 833, 735, 84, 583, 461, 37, 422, 644, 724, 272, 207, 668, 22, 552, 502, 872, 424, 212, 811, 66, 850, 837, 678, 102, 367, 954, 466, 822, 349, 991, 35, 194, 371, 763, 612, 188, 970, 704, 397, 744, 853, 486, 209, 375, 312, 944, 912, 130, 20, 624, 520, 998, 941, 519, 113, 560, 856, 452, 432, 990, 634, 227, 976, 498, 867, 277, 940, 24, 580, 501, 26, 144, 495, 237, 949, 945, 806, 382, 105, 228, 926, 204, 325, 473, 222, 865, 376, 626, 2, 581, 994, 457, 499, 181, 934, 30, 774, 876, 487, 373, 588, 545, 139, 265, 412, 323, 641, 676, 956, 689, 270, 906, 706, 300, 437, 571, 370, 809, 802, 201, 51, 820, 603, 946, 691, 613, 977, 404, 236, 625, 635, 901, 479, 315, 862, 775, 406, 409, 854, 423, 82, 387, 877, 698, 889, 307, 392, 910, 384, 485, 686, 880, 855, 197, 203, 770, 789, 578, 963, 441, 852, 244, 60, 199, 454, 401, 260, 442, 574, 449, 98, 621, 230, 697, 7, 289, 823, 356, 771, 283, 957, 599, 832, 776, 718, 52, 506, 525, 883, 818, 847, 947, 653, 909, 699, 206, 348, 298, 630, 273, 42, 321, 302, 768, 961, 39, 640, 845, 737, 904, 290, 526, 537, 439, 879, 844, 220, 341, 782, 245, 91, 143, 878, 801, 753, 713, 870, 471, 565, 223, 553, 286, 948, 45, 758, 639, 493, 488, 507, 960, 155, 951, 462, 248, 150, 177, 269, 808, 31, 411, 17, 587, 447, 444, 483, 569, 388, 651, 971, 161, 329, 749, 361, 399, 752, 894, 917, 979, 330, 793, 9, 579, 966, 491, 249, 403, 32, 900, 115, 434, 617, 440, 93, 777, 975, 748, 159, 68, 665, 126, 920, 690, 255, 134, 171, 646, 674, 803, 721, 563, 4, 369, 700, 839, 0, 383, 871, 582, 259, 421, 158, 711, 136, 929, 464, 75, 429, 515, 208, 14, 3, 119, 489, 649, 728, 46, 751, 911, 781, 609, 343, 94, 450, 558, 103, 897, 557, 202, 828, 458, 70, 523, 168, 688, 180, 619, 284, 702, 576, 353, 916, 234, 584, 547, 135, 328, 460, 394, 274, 352, 866, 366, 64, 938, 643, 715, 600, 185, 638, 851, 62, 100, 378, 368, 308, 314, 869, 764, 905, 389, 842, 149, 16, 532, 345, 800, 601, 436, 477, 428, 788, 924, 996, 318, 106, 928, 791, 652, 610, 821, 56, 891, 95, 680, 480, 530, 546, 160, 306, 465, 725, 196, 986, 898, 659, 123, 745, 590, 295, 671, 919, 719, 225, 555, 63, 49, 962, 750, 410, 191, 57, 313, 365, 271, 451, 942, 568, 319, 708, 712, 902, 840, 967, 340, 746, 943, 118, 952, 44, 342, 83, 645, 299, 657, 219, 350, 886, 414, 513, 40, 320, 301, 684, 524, 128, 895, 913, 503, 316, 374, 257, 562, 705, 836, 337, 783, 463, 281, 577, 914, 251, 426, 591, 899, 848, 216, 11, 984, 151, 268, 253, 767, 339, 522, 729, 607, 481, 148, 875, 484, 887, 416, 633, 360, 687, 363, 531, 890, 317, 176, 327, 743, 658, 925, 759, 606, 322, 695, 189, 494, 672, 231, 218, 570, 773, 72, 332, 709, 433, 183, 86, 291, 261, 974, 12, 469, 88, 999, 448, 937, 334, 792, 278, 104, 362, 673, 127, 496, 541, 21, 467, 595, 8, 575, 732, 262, 654, 517, 533, 453, 766, 418, 407, 693, 512, 419, 275, 864, 413, 121, 497, 642, 722, 108, 200, 950, 696, 834, 182, 596, 969, 959, 247, 701, 815, 814, 664, 77, 164, 535, 351, 29, 310, 468, 65, 740, 592, 667]
# art = pd.read_pickle("art_all_m.pkl")
x = pd.read_pickle("art_idf_m.pkl")

y = x["Response"].astype(float)

# ############################
# #analysis

cols = ["Neg_Score","Pos_Score","Absolute_Diff", "Word_Count","Response","PN_Metric"]
x = x.loc[:,cols]
x = x.astype(float)

# print(np.corrcoef(x.T))
# pd.plotting.scatter_matrix(x)
# plt.show()

model = smf.ols(formula="Response ~ Neg_Score*Pos_Score + Word_Count*Absolute_Diff", data=x).fit()
print(model.summary())

# x = sm.add_constant(x)
# model = sm.OLS(y,x).fit()
# print(model.summary())

# model = sm.OLS(y.iloc[train_ind],x.iloc[train_ind,]).fit()
# print(model.summary())
predict = model.predict(x.iloc[test_ind])

# from scipy.integrate import quad
# from scipy.stats import beta

trans_pred = predict.apply(lambda x: (x+20)/40)
trans_true = y.iloc[test_ind].apply(lambda x: 1 if x>0 else 0)

# def average_meterics(x):
# 	pred = np.array(trans_pred > x, dtype=int)

# 	a,b,c,d = 0,0,0,0
# 	for i,j in zip(pred,trans_true):
# 		if i==0 and j==0:
# 			a += 1
# 		if i==0 and j==1:
# 			b += 1
# 		if i==1 and j==0:
# 			c += 1
# 		if i==1 and j==1:
# 			d += 1

# 	bb = beta.pdf(x,2,2)
# 	ans = bb*c
# 	return(ans)

# ss, _ = quad(average_meterics,0,1,limit=100)
# print(ss)

