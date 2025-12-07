with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
fix_started = False
fixed_count = 0

for i, line in enumerate(lines):
    # Start fixing after "with st.spinner" which is around line 479
    if i > 475 and 'with st.spinner("Generating efficient frontier' in line:
        fix_started = True
        print(f"Start fixing at line {i+1}")
    
    # Stop fixing at "# Show welcome message"
    if fix_started and '# Show welcome message' in line:
        fix_started = False
        print(f"Stop fixing at line {i+1}, fixed {fixed_count} lines total")
    
    if fix_started:
        # Count leading spaces
        stripped = line.lstrip(' ')
        if not stripped:  # Empty line
            fixed_lines.append(line)
            continue
            
        spaces = len(line) - len(stripped)
        
        # Reduce indentation to 8 spaces (2 levels) for display code
        if spaces > 12:
            fixed_lines.append('            ' + stripped)
            fixed_count += 1
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f'Done - {fixed_count} lines corrected')

