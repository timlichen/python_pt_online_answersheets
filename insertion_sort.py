my_arr = [9,3,78,12,76,0,-2]

for idx in range(1, len(my_arr)): 
    temp = my_arr[idx] 
    prev_idx = idx-1
    while prev_idx >= 0 and temp < my_arr[prev_idx]: 
        my_arr[prev_idx + 1] = my_arr[prev_idx] 
        prev_idx -= 1
    my_arr[prev_idx + 1] = temp 

print(my_arr)