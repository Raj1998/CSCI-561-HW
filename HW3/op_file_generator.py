with open('homework3.py', 'r') as fr:
    with open('auto_submit.py', 'w') as fo:
        line = fr.readline()
        while line:
            line1 = line.strip()
            if line1.startswith("print("):
                line = "#"+line
            fo.write(line)
            # arr.append(line.replace('\n', ''))
            line = fr.readline()