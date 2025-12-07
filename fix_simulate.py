with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []

for i, line in enumerate(lines):
    # Lines 615-827 need fixing (inside with col2 and nested blocks)
    if i >= 614 and i < 700:
        stripped = line.lstrip(' ')
        if not stripped:  # Empty line
            fixed_lines.append(line)
            continue
        
        # Determine proper indentation based on content
        spaces = len(line) - len(stripped)
        
        # If line has way too many spaces (20+), reduce to proper level
        if spaces >= 20:
            # Inside col2 block should be 24 spaces (6 levels)
            # Inside if/else should be 28 spaces (7 levels)
            # Inside nested loops should be 32+ spaces
            
            # Check what kind of line this is
            if stripped.startswith('monitoring =') or stripped.startswith('# Display') or stripped.startswith('if monitoring'):
                fixed_lines.append(' ' * 24 + stripped)
            elif stripped.startswith('st.error') or stripped.startswith('st.success') or stripped.startswith('st.metric') or stripped.startswith('st.markdown'):
                fixed_lines.append(' ' * 28 + stripped)
            elif stripped.startswith('alert_data') or stripped.startswith('for alert') or stripped.startswith('if monitoring['):
                fixed_lines.append(' ' * 28 + stripped)
            elif 'alert_data.append' in stripped or "'Asset':" in stripped:
                fixed_lines.append(' ' * 32 + stripped)
            else:
                fixed_lines.append(line)  # Keep as is if uncertain
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print('Fixed simulate block indentation')
