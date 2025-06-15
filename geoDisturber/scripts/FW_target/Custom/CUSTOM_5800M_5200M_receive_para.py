
import math

def calculate_split_size(start, end):    
    # 计算最小分割间隔，确保间隔小于30000000    
    interval_length = end - start    
    if interval_length <= 0:  
        return 0  # 如果区间长度为0或负数，返回0作为分割间隔  
    max_splits = math.ceil(interval_length / 30000000.0)    
    if max_splits == 0:    
        max_splits = 1    
    split_size = max(1, interval_length // max_splits)  # 确保分割间隔至少为1  
    return split_size



def work(A, B, C, D):    
    # 检查参数是否合法    
    if not (0 <= A <= B) or not (0 <= C <= D):    
        print("A, B, C, D必须满足条件：0 <= A <= B 且 0 <= C <= D")    
        return None, None    
    
    # 计算两个区间的最小分割间隔  
    split_size_AB = calculate_split_size(A, B)  
    split_size_CD = calculate_split_size(C, D)  
  
    # 取两个间隔中的较大值作为统一的间隔大小  
    unified_split_size = max(split_size_AB, split_size_CD, 1000000)  
  
    # 划分区间(A, B)  
    centers_AB = []  
    if B-A < unified_split_size:
        current_position = (A + B) / 2
        centers_AB.append(int(current_position)) 
    else:
        current_position = A + unified_split_size / 2  
        while current_position < B:  
            centers_AB.append(int(current_position))  
            current_position += unified_split_size  
        if centers_AB[-1] > B:  
            centers_AB[-1] = B 
  
    # 最后一个中心值可能需要微调以确保它落在区间内  
    #if centers_AB and centers_AB[-1] > B - unified_split_size / 2:  
    #    centers_AB[-1] = B  
  
    # 划分区间(C, D)  
    centers_CD = []  
    if D-C < unified_split_size:
        current_position = (C + D) / 2
        centers_CD.append(int(current_position)) 
    else:
        current_position = C + unified_split_size / 2  
        while current_position < D:  
            centers_CD.append(int(current_position))  
            current_position += unified_split_size  
        if centers_CD[-1] > D:  
            centers_CD[-1] = D 
  
    # 最后一个中心值可能需要微调以确保它落在区间内  
    #if centers_CD and centers_CD[-1] > D - unified_split_size / 2:  
    #    centers_CD[-1] = D   
 
    out = [unified_split_size, centers_AB, centers_CD]
    return out
