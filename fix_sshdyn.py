import re

with open('D:/devel/sftpplug_src/src/sshdynfunctions.h', 'r') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []

for line in lines:
    if not line.startswith('FUNCDEF('):
        new_lines.append(line)
        continue
    
    # Remove FUNCDEF( prefix and trailing );
    inner = line[len('FUNCDEF('):]
    if inner.endswith(');'):
        inner = inner[:-2]
    
    # Find the parameters - they start with (
    paren_idx = inner.find('(')
    if paren_idx == -1:
        new_lines.append(line)
        continue
    
    params = inner[paren_idx:]
    before = inner[:paren_idx]
    
    # Find the LAST comma in 'before' - this should be between type and name
    comma_idx = before.rfind(',')
    if comma_idx == -1:
        new_lines.append(line)
        continue
    
    ret_type = before[:comma_idx].strip()
    func_name = before[comma_idx+1:].strip()
    
    new_line = f'{ret_type} (WINAPI *{func_name}){params};'
    new_lines.append(new_line)

with open('D:/devel/sftpplug_src/src/sshdynfunctions.h', 'w') as f:
    f.write('\n'.join(new_lines))
    if not content.endswith('\n'):
        f.write('\n')

print("Done")
