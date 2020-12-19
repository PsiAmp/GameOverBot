import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import json



np.random.seed(1)

d = defaultdict(list)
d['abc'].append((1, 2, 3))
d['cab'].append((3, 2, 1))
d['abc'].append((4, 5, 6))
d['cab'].append((6, 5, 4))
d['cab'].append((1, 1, 1))

d['abc'].sort(key=lambda tup: tup[0])
d['cab'].sort(key=lambda tup: tup[0])

#write the data to a file
json.dump(d, open("dumpFile", 'w'))
dd = json.load(open("dumpFile", 'r'))
print(dd)


total = [(0, 1, 1.0), (44, 30, 0.78), (48, 34, 0.79), (52, 38, 0.79), (58, 43, 0.79), (64, 49, 0.79), (72, 57, 0.77), (84, 64, 0.77), (92, 72, 0.78), (102, 80, 0.77), (112, 92, 0.78), (120, 104, 0.79), (128, 119, 0.79), (138, 134, 0.8), (162, 149, 0.8), (172, 166, 0.81), (194, 187, 0.82), (218, 211, 0.82), (244, 235, 0.84), (300, 262, 0.84), (354, 293, 0.83), (0, 1, 1.0), (19, 3, 1.0), (33, 6, 0.88), (35, 9, 0.91), (53, 7, 0.77), (55, 9, 0.8), (59, 12, 0.83), (65, 16, 0.86), (73, 18, 0.84), (79, 22, 0.86), (85, 25, 0.87), (93, 28, 0.85), (103, 32, 0.86), (125, 37, 0.82), (139, 44, 0.81), (143, 50, 0.82), (153, 57, 0.83), (175, 64, 0.83), (189, 73, 0.83), (215, 83, 0.82), (253, 93, 0.82), (279, 104, 0.82), (327, 117, 0.82), (0, 1, 1.0), (2, 3, 1.0), (8, 6, 0.88), (10, 8, 0.9), (12, 11, 0.92), (16, 13, 0.93), (18, 16, 0.94), (28, 18, 0.9), (38, 20, 0.88), (54, 25, 0.86), (66, 29, 0.87), (82, 33, 0.85), (100, 38, 0.86), (126, 44, 0.85), (152, 50, 0.85), (174, 56, 0.86), (198, 65, 0.86), (210, 73, 0.85), (232, 85, 0.86), (266, 96, 0.83), (324, 107, 0.82), (0, 1, 1.0), (5, 3, 0.8), (21, 5, 0.64), (39, 8, 0.64), (45, 11, 0.66), (47, 13, 0.68), (51, 16, 0.7), (55, 18, 0.72), (59, 20, 0.73), (65, 24, 0.75), (75, 28, 0.76), (83, 33, 0.77), (91, 39, 0.79), (103, 44, 0.76), (109, 50, 0.78), (115, 56, 0.79), (137, 66, 0.78), (147, 74, 0.77), (163, 83, 0.78), (183, 95, 0.78), (199, 106, 0.78), (233, 120, 0.78), (279, 134, 0.76), (315, 149, 0.78), (359, 166, 0.78), (0, 1, 1.0), (1, 3, 1.0), (5, 8, 1.0), (11, 12, 0.93), (15, 14, 0.94), (17, 17, 0.94), (25, 19, 0.87), (33, 17, 0.81), (37, 19, 0.82), (41, 22, 0.82), (57, 26, 0.8), (61, 29, 0.81), (75, 35, 0.81), (91, 41, 0.79), (97, 47, 0.81), (117, 56, 0.81), (125, 63, 0.83), (135, 70, 0.81), (149, 79, 0.82), (171, 88, 0.81), (189, 98, 0.81), (223, 110, 0.82), (255, 124, 0.82), (309, 138, 0.83), (0, 1, 1.0), (7, 4, 0.83), (11, 6, 0.8), (13, 8, 0.83), (19, 10, 0.77), (23, 12, 0.8), (27, 14, 0.81), (31, 16, 0.83), (35, 19, 0.85), (39, 22, 0.86), (47, 28, 0.85), (53, 32, 0.83), (57, 37, 0.85), (63, 43, 0.85), (69, 49, 0.86), (79, 55, 0.85), (91, 63, 0.84), (103, 70, 0.82), (107, 79, 0.82), (119, 88, 0.81), (135, 98, 0.82), (147, 109, 0.83), (157, 123, 0.82), (171, 137, 0.83), (185, 156, 0.85), (203, 177, 0.84), (227, 197, 0.83), (261, 220, 0.85), (297, 245, 0.86), (339, 273, 0.87), (0, 1, 1.0), (5, 3, 1.0), (11, 6, 1.0), (13, 8, 1.0), (19, 12, 0.93), (23, 14, 0.94), (31, 17, 0.94), (35, 19, 0.95), (41, 23, 0.96), (43, 26, 0.96), (47, 29, 0.93), (51, 34, 0.91), (55, 38, 0.92), (63, 43, 0.92), (73, 48, 0.91), (83, 54, 0.9), (87, 61, 0.9), (99, 68, 0.86), (121, 76, 0.81), (131, 86, 0.83), (147, 97, 0.83), (169, 108, 0.83), (193, 124, 0.84), (237, 139, 0.86), (297, 155, 0.87), (0, 1, 1.0), (7, 3, 1.0), (17, 5, 1.0), (19, 7, 1.0), (29, 10, 1.0), (37, 14, 1.0), (43, 16, 1.0), (47, 19, 1.0), (59, 22, 0.96), (69, 27, 0.93), (75, 30, 0.94), (79, 34, 0.94), (83, 38, 0.94), (91, 44, 0.93), (97, 51, 0.91), (105, 57, 0.91), (115, 64, 0.9), (127, 76, 0.92), (141, 85, 0.88), (155, 98, 0.88), (159, 110, 0.89), (181, 123, 0.88), (191, 142, 0.89), (215, 158, 0.89), (233, 176, 0.89), (255, 200, 0.89), (291, 227, 0.88), (317, 255, 0.89), (0, 1, 1.0), (4, 3, 0.8), (10, 5, 0.86), (14, 8, 0.9), (18, 10, 0.86), (28, 13, 0.81), (30, 17, 0.83), (32, 19, 0.82), (42, 17, 0.72), (44, 19, 0.73), (48, 22, 0.74), (54, 25, 0.76), (60, 28, 0.76), (68, 35, 0.77), (76, 40, 0.77), (82, 45, 0.78), (92, 51, 0.76), (104, 58, 0.75), (122, 67, 0.74), (138, 77, 0.74), (148, 86, 0.75), (166, 98, 0.74), (186, 110, 0.74), (200, 125, 0.75), (214, 141, 0.75), (234, 159, 0.77), (256, 178, 0.78), (278, 198, 0.78), (308, 221, 0.78), (0, 1, 1.0), (6, 3, 0.8), (8, 6, 0.88), (16, 8, 0.79), (20, 11, 0.82), (24, 13, 0.84), (28, 16, 0.86), (30, 19, 0.88), (38, 22, 0.84), (44, 20, 0.78), (46, 23, 0.79), (54, 26, 0.78), (66, 30, 0.78), (72, 34, 0.78), (80, 38, 0.78), (108, 43, 0.74), (112, 49, 0.76), (122, 56, 0.78), (142, 63, 0.78), (168, 71, 0.77), (194, 81, 0.79), (214, 93, 0.79), (248, 104, 0.79), (274, 117, 0.8), (300, 130, 0.78), (0, 1, 1.0), (18, 3, 0.71), (22, 5, 0.78), (30, 7, 0.77), (38, 9, 0.76), (48, 11, 0.73), (56, 14, 0.76), (58, 12, 0.71), (62, 15, 0.74), (66, 17, 0.75), (70, 21, 0.77), (72, 24, 0.8), (76, 28, 0.79), (88, 33, 0.79), (96, 40, 0.79), (106, 45, 0.78), (115, 50, 0.79), (141, 56, 0.79), (180, 65, 0.8), (198, 75, 0.81), (210, 85, 0.82), (230, 95, 0.8), (260, 106, 0.79), (298, 120, 0.8), (326, 134, 0.81), (0, 1, 1.0), (6, 3, 0.8), (16, 5, 0.73), (18, 7, 0.73), (20, 10, 0.78), (24, 12, 0.77), (36, 15, 0.75), (44, 17, 0.74), (48, 19, 0.74), (54, 22, 0.74), (64, 27, 0.75), (68, 31, 0.75), (74, 35, 0.76), (98, 39, 0.71), (116, 44, 0.69), (130, 51, 0.71), (134, 59, 0.72), (154, 66, 0.73), (176, 80, 0.73), (206, 90, 0.73), (222, 100, 0.73), (238, 112, 0.74), (278, 126, 0.76), (314, 142, 0.77), (0, 1, 1.0), (7, 3, 1.0), (11, 6, 1.0), (19, 8, 0.83), (25, 11, 0.87), (31, 13, 0.84), (33, 15, 0.86), (37, 17, 0.84), (39, 19, 0.85), (41, 22, 0.84), (51, 26, 0.81), (53, 30, 0.82), (59, 34, 0.83), (67, 39, 0.84), (73, 44, 0.83), (77, 49, 0.84), (83, 55, 0.85), (93, 63, 0.83), (103, 70, 0.84), (109, 78, 0.83), (117, 87, 0.82), (135, 97, 0.8), (147, 108, 0.81), (157, 124, 0.81), (173, 139, 0.81), (211, 156, 0.78), (257, 174, 0.78), (279, 196, 0.79), (307, 222, 0.79), (343, 247, 0.8), (0, 1, 1.0), (3, 3, 1.0), (5, 5, 1.0), (7, 7, 1.0), (9, 9, 1.0), (11, 14, 0.94), (17, 17, 0.95), (19, 20, 0.95), (21, 24, 0.96), (27, 28, 0.88), (31, 33, 0.84), (33, 37, 0.85), (39, 43, 0.81), (49, 49, 0.81), (53, 55, 0.81), (71, 63, 0.77), (81, 73, 0.78), (91, 82, 0.79), (99, 94, 0.8), (121, 107, 0.76), (137, 119, 0.75), (151, 133, 0.77), (169, 148, 0.77), (191, 165, 0.76), (219, 184, 0.77), (251, 205, 0.78), (275, 233, 0.79), (307, 267, 0.8), (339, 298, 0.81), (0, 1, 1.0), (7, 3, 1.0), (11, 6, 1.0), (15, 9, 1.0), (19, 11, 1.0), (21, 14, 1.0), (25, 17, 1.0), (31, 21, 1.0), (35, 25, 1.0), (41, 28, 0.96), (53, 32, 0.9), (59, 36, 0.88), (69, 42, 0.87), (79, 47, 0.84), (89, 53, 0.81), (95, 59, 0.82), (109, 67, 0.8), (119, 76, 0.75), (137, 85, 0.76), (147, 95, 0.75), (165, 106, 0.74), (183, 119, 0.74), (201, 135, 0.76), (223, 152, 0.77), (239, 169, 0.78), (271, 188, 0.8), (313, 213, 0.81), (0, 1, 1.0), (3, 4, 1.0), (11, 7, 1.0), (15, 11, 1.0), (23, 16, 0.94), (25, 19, 0.95), (29, 22, 0.92), (31, 25, 0.93), (37, 28, 0.93), (45, 32, 0.89), (55, 37, 0.85), (61, 42, 0.86), (89, 48, 0.83), (101, 54, 0.83), (119, 60, 0.84), (131, 67, 0.85), (147, 76, 0.85), (157, 87, 0.85), (171, 100, 0.86), (207, 113, 0.86), (225, 129, 0.87), (247, 145, 0.88), (311, 167, 0.86), (0, 1, 1.0), (4, 5, 1.0), (6, 7, 1.0), (8, 9, 1.0), (14, 11, 1.0), (16, 14, 1.0), (22, 19, 1.0), (24, 23, 0.96), (34, 27, 0.91), (48, 30, 0.83), (56, 37, 0.82), (64, 42, 0.82), (68, 49, 0.84), (74, 55, 0.83), (80, 62, 0.83), (88, 69, 0.82), (96, 78, 0.83), (106, 89, 0.83), (112, 99, 0.84), (126, 110, 0.83), (142, 123, 0.84), (158, 138, 0.83), (172, 154, 0.85), (192, 174, 0.84), (222, 196, 0.84), (252, 219, 0.84), (268, 245, 0.85), (302, 273, 0.86), (346, 307, 0.86), (0, 1, 1.0), (2, 3, 1.0), (6, 5, 1.0), (12, 7, 1.0), (20, 10, 0.92), (24, 12, 0.93), (30, 15, 0.94), (36, 17, 0.9), (50, 20, 0.85), (54, 24, 0.86), (62, 29, 0.88), (80, 34, 0.85), (88, 39, 0.87), (104, 45, 0.85), (112, 52, 0.87), (124, 60, 0.86), (136, 67, 0.87), (146, 78, 0.87), (168, 90, 0.88), (262, 101, 0.82), (350, 113, 0.81), (0, 1, 1.0), (3, 3, 1.0), (4, 6, 1.0), (7, 8, 0.9), (9, 10, 0.86), (13, 14, 0.89), (17, 18, 0.91), (19, 20, 0.91), (26, 25, 0.9), (32, 30, 0.86), (35, 36, 0.88), (38, 42, 0.88), (42, 48, 0.89), (49, 56, 0.9), (56, 64, 0.87), (67, 72, 0.86), (73, 80, 0.86), (81, 90, 0.86), (88, 100, 0.86), (100, 112, 0.84), (114, 126, 0.85), (134, 140, 0.82), (151, 158, 0.84), (181, 178, 0.83), (212, 199, 0.84), (244, 226, 0.86), (295, 252, 0.86), (349, 280, 0.88), (0, 1, 1.0), (3, 4, 1.0), (11, 6, 1.0), (19, 8, 0.9), (27, 10, 0.85), (43, 12, 0.83), (51, 15, 0.85), (53, 17, 0.86), (57, 21, 0.88), (63, 24, 0.89), (73, 28, 0.86), (87, 32, 0.86), (93, 36, 0.85), (97, 40, 0.87), (109, 45, 0.86), (119, 51, 0.87), (133, 58, 0.86), (145, 65, 0.87), (163, 73, 0.86), (173, 82, 0.87), (195, 97, 0.86), (219, 109, 0.88), (251, 122, 0.86), (277, 137, 0.86), (341, 153, 0.86), (0, 2, 1.0), (17, 4, 0.7), (21, 6, 0.75), (29, 8, 0.72), (33, 10, 0.73), (37, 13, 0.76), (39, 15, 0.78), (41, 17, 0.79), (43, 19, 0.8), (47, 24, 0.8), (51, 28, 0.82), (57, 32, 0.83), (61, 36, 0.84), (71, 41, 0.83), (85, 46, 0.81), (93, 53, 0.83), (107, 62, 0.84), (117, 69, 0.84), (127, 77, 0.85), (141, 86, 0.86), (153, 96, 0.85), (167, 108, 0.87), (179, 122, 0.88), (195, 136, 0.89), (211, 155, 0.87), (231, 173, 0.86), (267, 194, 0.85), (301, 220, 0.86), (331, 251, 0.87), (0, 1, 1.0), (17, 3, 0.66), (21, 5, 0.72), (25, 7, 0.77), (33, 9, 0.76), (37, 12, 0.79), (43, 15, 0.81), (51, 18, 0.78), (63, 20, 0.77), (69, 23, 0.78), (73, 27, 0.8), (77, 30, 0.81), (85, 35, 0.79), (91, 40, 0.79), (103, 45, 0.78), (107, 50, 0.79), (115, 56, 0.8), (129, 63, 0.8), (139, 70, 0.8), (151, 79, 0.8), (161, 89, 0.82), (173, 99, 0.81), (193, 115, 0.81), (213, 132, 0.82), (223, 147, 0.83), (249, 164, 0.83), (271, 183, 0.83), (309, 209, 0.85), (337, 238, 0.85), (0, 1, 1.0), (14, 3, 0.64), (20, 7, 0.74), (22, 9, 0.77), (30, 12, 0.75), (46, 16, 0.76), (52, 18, 0.78), (62, 20, 0.76), (68, 24, 0.78), (78, 27, 0.8), (94, 32, 0.78), (102, 36, 0.79), (110, 40, 0.8), (124, 45, 0.81), (134, 50, 0.82), (154, 59, 0.82), (164, 66, 0.83), (180, 75, 0.84), (212, 84, 0.82), (232, 98, 0.82), (312, 110, 0.82), (354, 123, 0.83), (0, 1, 1.0), (13, 3, 0.71), (23, 5, 0.69), (31, 7, 0.71), (37, 9, 0.71), (43, 11, 0.73), (45, 9, 0.69), (47, 11, 0.72), (53, 9, 0.68), (63, 11, 0.69), (71, 13, 0.69), (77, 15, 0.7), (83, 17, 0.7), (87, 15, 0.68), (89, 19, 0.72), (103, 22, 0.73), (115, 25, 0.75), (121, 22, 0.7), (123, 27, 0.74), (131, 32, 0.76), (137, 36, 0.76), (145, 42, 0.78), (155, 47, 0.79), (161, 54, 0.8), (173, 60, 0.8), (199, 67, 0.79), (215, 75, 0.78), (233, 86, 0.79), (273, 97, 0.78), (299, 110, 0.8), (329, 126, 0.8), (0, 1, 1.0), (2, 3, 1.0), (8, 6, 0.87), (10, 8, 0.9), (16, 10, 0.81), (22, 13, 0.78), (26, 11, 0.7), (34, 13, 0.7), (42, 17, 0.71), (48, 20, 0.7), (56, 24, 0.71), (60, 28, 0.72), (66, 32, 0.72), (74, 36, 0.73), (84, 42, 0.73), (100, 47, 0.73), (108, 54, 0.73), (120, 60, 0.72), (130, 67, 0.73), (140, 77, 0.73), (152, 86, 0.72), (178, 96, 0.71), (204, 111, 0.72), (222, 124, 0.74), (238, 138, 0.73), (266, 159, 0.75), (292, 182, 0.76), (356, 204, 0.73), (0, 1, 1.0), (7, 7, 0.89), (11, 9, 0.91), (13, 7, 0.77), (17, 9, 0.76), (25, 13, 0.81), (27, 15, 0.82), (31, 21, 0.86), (37, 24, 0.87), (43, 28, 0.88), (49, 34, 0.88), (52, 39, 0.88), (73, 44, 0.83), (87, 50, 0.83), (103, 56, 0.82), (111, 64, 0.82), (119, 73, 0.81), (141, 84, 0.78), (167, 95, 0.78), (179, 109, 0.79), (203, 124, 0.8), (233, 138, 0.81), (265, 159, 0.82), (303, 177, 0.84)]
total.sort(key=lambda tup: tup[0])

x = []
y = []
for t in total:
    x.append(t[0])
    y.append(t[1])

xhat = scipy.signal.savgol_filter(x, 51, 3) # window size 51, polynomial order 3
yhat = scipy.signal.savgol_filter(y, 51, 3) # window size 51, polynomial order 3

plt.plot(x,y)
plt.plot(xhat,yhat, color='red')
plt.show()