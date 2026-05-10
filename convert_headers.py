import re
import sys

def process_header(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Pattern to match function declarations starting with LIBSSH2_API
    # This handles multiline declarations ending with ;
    pattern = r'(LIBSSH2_API\s+.*?;)'
    
    def replace_func(match):
        func_decl = match.group(1)
        # Don't wrap if it's just a typedef or forward declaration inside struct
        if '#ifdef staticlinking' in func_decl or '#endif' in func_decl:
            return func_decl
        return f'#ifdef staticlinking\n{func_decl}\n#endif'
    
    # Use DOTALL to match across newlines
    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Processed: {input_file} -> {output_file}")

if __name__ == '__main__':
    process_header('src/libssh2.h', 'src/libssh2.h')
    process_header('src/libssh2_sftp.h', 'src/libssh2_sftp.h')
