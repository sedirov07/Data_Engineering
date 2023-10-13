with open('text_2_var_22', 'r') as f:
    lines = f.readlines()
    totals = []
    for line in lines:
        nums = list(map(int, line.split('/')))
        totals.append(sum(nums))

with open('output_2_var_22.txt', 'w') as f:
    for total in totals:
        f.write(f'{total}\n')
