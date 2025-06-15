
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



def work(A, B):    
    # 检查参数是否合法    
    if not (0 <= A <= B):    
        print("A, B必须满足条件：0 <= A <= B")    
        return None, None    
    
    # 计算区间的最小分割间隔  
    split_size_AB = calculate_split_size(A, B)  
  
    # 取两个间隔中的较大值作为统一的间隔大小  
    unified_split_size = max(split_size_AB, 1000000)  
  
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
 
    out = [unified_split_size, centers_AB]
    return out
