with open('text_3_var_22', 'r') as f:
    lines = f.readlines()
    result = []
    for line in lines:
        nums = line.strip().split(',')
        i = 0
        while i < len(nums) - 1:
            if nums[i] == 'NA':
                nums[i] = str((float(nums[i-1]) + int(nums[i + 1])) / 2)
            if float(nums[i])**1/2 < 50 + 22:
                nums.pop(i)
            else:
                i += 1
        result.append(','.join(nums))

print(result)
with open('output_3_var_22.txt', 'w') as f:
    for res in result:
        f.write(f'{res}\n')
