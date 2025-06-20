import math

def calculate_split_size(start, end):    
    # 计算区间大小  
    interval_length = end - start    
    if interval_length <= 0:  
        return 0  # 如果区间长度为0或负数，返回0作为分割间隔  
    
    # 如果区间的长度大于60，则每个区间的大小为30
    if interval_length > 120000000:
        return 30000000  # 强制每个区间的大小为30M
    
    # 如果区间长度小于等于60，直接将其等分为两个区间
    return interval_length // 4 if interval_length > 1 else 1  # 处理小区间，最小分割间隔为1

def work(A, B):    
    # 检查参数是否合法    
    if not (0 <= A <= B):    
        print("A, B必须满足条件：0 <= A <= B")    
        return None, None    
    
    # 计算区间的分割间隔  
    split_size_AB = calculate_split_size(A, B)  
    
    # 计算两个子区间的中心位置
    centers_AB = []  
    
    if B - A > 120000000:
        # 如果区间大于60，按照30M来分割
        # 第一个子区间的中心点
        first_center = A + 15000000
        centers_AB.append(int(first_center))

        # 第二个子区间的中心点
        second_center = A + 45000000
        centers_AB.append(int(second_center))

        third_center = A + 75000000
        centers_AB.append(int(third_center))

        fourth_center = A + 105000000
        centers_AB.append(int(fourth_center))
    else:
        # 如果区间小于等于60，平分区间并计算中心点
        # 第一个子区间的中心点
        first_center = A + split_size_AB / 2
        centers_AB.append(int(first_center))

        # 第二个子区间的中心点
        second_center = A + split_size_AB + split_size_AB / 2
        centers_AB.append(int(second_center))

        third_center = A + 2*split_size_AB + split_size_AB / 2
        centers_AB.append(int(third_center))
	
        fourth_center = A + 3*split_size_AB + split_size_AB / 2
        centers_AB.append(int(fourth_center))

    # 输出结果，包括分割间隔和中心点
    out = [split_size_AB, centers_AB[0], centers_AB[1], centers_AB[2], centers_AB[3]]
    return out

