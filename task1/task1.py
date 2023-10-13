with open('text_1_var_22', 'r') as f:
    lines = f.readlines()
    words_dict = {}
    for line in lines:
        row = (line.strip()
               .replace('\n', '')
               .replace('!', ' ')
               .replace('?', ' ')
               .replace('.', ' ')
               .replace(',', ' ')
               .strip())
        words = row.split()
        for word in words:
            words_dict[word] = words_dict.get(word, 0) + 1

words_dict = dict(sorted(words_dict.items(), key=lambda x: x[1], reverse=True))

with open('output_1_var_22.txt', 'w') as f:
    for key, value in words_dict.items():
        f.write(f'{key}: {value}\n')
