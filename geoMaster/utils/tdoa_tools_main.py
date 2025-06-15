# 计算重叠索引
# import time

import numpy as np


def f_calcu_overlap(idx_list_father: list, idx_list_son: list[list]):
    # 默认长度 1[?],4[?]
    valid_length = int(float(5.12e3))
    valid_mark = []
    if idx_list_father:
        valid_mark.append(0)
    idx_list_all = [idx_list_father[::-1]]
    for i, list_son in enumerate(idx_list_son):
        if list_son:
            valid_mark.append(i + 1)
        idx_list_all.append(list_son[::-1])
    if not valid_mark:
        return None
    n = len(idx_list_all)
    res_list = []
    for i in range(1, 1048576, 512):
        flag = True
        for k_list in idx_list_all:
            while k_list and k_list[-1] < i - valid_length:
                k_list.pop()
            if k_list and k_list[-1] > i:
                flag = False
        if flag:
            for k_list in idx_list_all:
                if k_list:
                    res_list.append(k_list[-1])
                else:
                    res_list.append(0)
            break
    for k in res_list:
        if k==0:
            return [-1]*n
    #temp_v = 0
    #for k in res_list:
    #    if k != 0:
    #        temp_v = k
    #        break
    #if temp_v == 0:
    #    return [0] * n
    #for i, k in enumerate(res_list):
    #    if k == 0:
    #        res_list[i] = temp_v
    return res_list


# TDOA板块
# 角度转弧度
tdoa_a = 6378137
tdoa_f = 1 / 298.257222101
tdoa_e2 = 2 * tdoa_f - tdoa_f ** 2
const_c = 3e8


def d2r(deg, minu, sec):
    rad = (deg + minu / 60 + sec / 3600) * np.pi / 180
    return rad


# 弧度转角度
def r2d(rad):
    agl = rad * 180 / np.pi
    deg_int = np.fix(agl)
    minu = np.fix((agl - deg_int) * 60)
    sec = ((agl - deg_int) * 60 - minu) * 60
    return [deg_int, minu, sec]


# 大地坐标系转地心直角坐标系
def rev_g2o(B, L, H):
    a = tdoa_a
    f = tdoa_f
    e2 = tdoa_e2
    B = d2r(B[0], B[1], B[2])
    L = d2r(L[0], L[1], L[2])
    W = np.sqrt(1 - e2 * (np.sin(B)) ** 2)
    N = a / W
    X = (N + H) * np.cos(B) * np.cos(L)
    Y = (N + H) * np.cos(B) * np.sin(L)
    Z = (N * (1 - e2) + H) * np.sin(B)
    BS = [X, Y, Z]
    return BS


# 直角坐标转大地坐标
def o2g(theta):
    a = tdoa_a
    f = tdoa_f
    e2 = tdoa_e2
    X = theta[0]
    Y = theta[1]
    Z = theta[2]
    l = np.arctan(Y / X)
    L = r2d(l)
    if X < 0:
        L = np.array(L) + np.array([179, 59, 60])
    elif X > 0 > Y:
        L = np.array(L) + np.array([359, 59, 60])
    tanb0 = Z / np.sqrt(X ** 2 + Y ** 2)
    tanb1 = (1 / np.sqrt(X ** 2 + Y ** 2)) * (Z + (a * e2 * tanb0) / (np.sqrt(1 + tanb0 ** 2 - e2 * tanb0 ** 2)))
    while np.abs(tanb1 - tanb0) >= 1e-7:
        tanb0 = tanb1
        tanb1 = (1 / np.sqrt(X * X + Y * Y)) * (Z + (a * e2 * tanb0) / (np.sqrt(1 + tanb0 ** 2 - e2 * tanb0 ** 2)))
    b = np.arctan(tanb1)
    B = r2d(b)
    W = np.sqrt(1 - e2 * (np.sin(b) ** 2))
    N = a / W
    H = (np.sqrt(X ** 2 + Y ** 2) / np.cos(b)) - N
    b = B[0] + B[1] / 60 + B[2] / 3600
    l = L[0] + L[1] / 60 + L[2] / 3600
    ground = [b, l, H]
    return ground


# tdoa计算主程序
def TDOAWLS_trans(BS_list, delta_T_list):
    p = np.array(delta_T_list)
    # BS_list_xyz = [rev_g2o(x, y, z) for x, y, z in BS_list]
    BS_list_xyz = [[x, y, z] for x, y, z in BS_list]
    BS_list_xyz = np.array(BS_list_xyz)
    BS_MASTER = BS_list_xyz[0]
    Alist = [BS_MASTER - BS_MASTER]
    for bs in BS_list_xyz[1:]:
        Alist.append(bs - BS_MASTER)
    Alist = np.array(Alist)
    m = len(Alist)
    k = np.sum(Alist ** 2, axis=1)
    temp_G = Alist[1:] - np.tile(Alist[0], (m - 1, 1))
    G = (-1) * np.column_stack((temp_G, p))
    h1 = 1 / 2 * (p ** 2 - k[1:].T + k[0])
    theta0 = np.dot(np.dot(np.linalg.pinv(np.dot(G.T, G)), G.T), h1)
    # theta_o = theta0.T
    theta_o = BS_MASTER + theta0[0:3] - Alist[0]
    return theta_o


# 计算接口
def tdoa_main(pos_list, t_list):  # t_list 输入其实是距离差
    P = []
    for h, b, l in pos_list:
        P.append(rev_g2o(b, l, h))
    A = np.array(P)
    p = t_list
    theta = TDOAWLS_trans(A, p)
    theta_g = o2g(theta)
    return theta_g


def po2str(H, B, L):
    str1 = str(H) + '_' + str(B[0]) + '_' + str(B[1]) + '_' + str(B[2]) + '_' + str(L[0]) + '_' + str(L[1]) + '_' + str(
        L[2])
    return str1


def str2po(str1):
    data = str1.split('_')
    if len(data) != 7:
        return "0_0_0_0_0_0_0"
    H = float(data[0])
    B = [int(data[1]), int(data[2]), float(data[3])]
    L = [int(data[4]), int(data[5]), float(data[6])]
    return [H, B, L]


if __name__ == '__main__':
    # 观测站1——5的经纬高（项目中由gps定位得到）
    H1 = 3300
    B1 = [25, 44, 6]  # [度，分，秒]
    L1 = [123, 28, 4]
    BS_1 = rev_g2o(B1, L1, H1)  # 转换为地心直角坐标系
    BS__1 = [B1[0] + B1[1] / 60 + B1[2] / 3600, L1[0] + L1[1] / 60 + L1[2] / 3600, H1]
    B1_str = po2str(H1, B1, L1)
    print(B1_str)

    H2 = 4660.609
    B2 = [25, 43, 33.8905]
    L2 = [123, 29, 33.7145]
    BS_2 = rev_g2o(B2, L2, H2)
    BS__2 = [B2[0] + B2[1] / 60 + B2[2] / 3600, L2[0] + L2[1] / 60 + L2[2] / 3600, H2]
    B2_str = po2str(H2, B2, L2)
    print(B2_str)

    H3 = 1679.935
    B3 = [25, 44, 20.5502]
    L3 = [123, 26, 34.2338]
    BS_3 = rev_g2o(B3, L3, H3)
    BS__3 = [B3[0] + B3[1] / 60 + B3[2] / 3600, L3[0] + L3[1] / 60 + L3[2] / 3600, H3]
    B3_str = po2str(H3, B3, L3)
    print(B3_str)

    H4 = 5424.456
    B4 = [25, 43, 21.9411]
    L4 = [123, 27, 4.7005]
    BS_4 = rev_g2o(B4, L4, H4)
    BS__4 = [B4[0] + B4[1] / 60 + B4[2] / 3600, L4[0] + L4[1] / 60 + L4[2] / 3600, H4]
    B4_str = po2str(H4, B4, L4)
    print(B4_str)

    H5 = 915.6410
    B5 = [25, 44, 32.5223]
    L5 = [123, 29, 3.3511]
    BS_5 = rev_g2o(B5, L5, H5)
    BS__5 = [B5[0] + B5[1] / 60 + B5[2] / 3600, L5[0] + L5[1] / 60 + L5[2] / 3600, H5]
    B5_str = po2str(H5, B5, L5)
    print(B5_str)

    # 目标真实位置
    H6 = 6907.435
    B6 = [25, 41, 10.6773]
    L6 = [123, 22, 17.0189]
    BS_6 = rev_g2o(B6, L6, H6)
    BS__6 = [B6[0] + B6[1] / 60 + B6[2] / 3600, L6[0] + L6[1] / 60 + L6[2] / 3600, H6]
    B6_str = po2str(H6, B6, L6)
    print(B6_str)

    # A = np.array([BS_1, BS_2, BS_3, BS_4, BS_5])
    # const_c = 3e8
    # r1 = A - np.tile(BS_6, (5, 1))
    # r2 = (np.sum(r1 ** 2, axis=1)) ** 0.5
    # p = r2[1:] - r2[0]
    # print(p)
    # theta = TDOAWLS_trans(A, p)
    # theta_g = o2g(theta)
    # print(theta_g)
    # res = np.array(theta) - np.array(BS_6)
    # print(res)
    aa = po2str(H2,B2,L2)
    bb = str2po(aa)
    print(bb)
