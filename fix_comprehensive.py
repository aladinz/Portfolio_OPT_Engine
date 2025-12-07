"""
Comprehensive fix for simulate_drift block indentation.
The structure should be:
- if simulate_drift: (16 spaces - level 4)
  - st.markdown (20 spaces - level 5)
  - with st.spinner: (20 spaces - level 5)
    - spinner content (24 spaces - level 6)
    - with col1/col2: (24 spaces - level 6)
      - col content (28 spaces - level 7)
      - if/else blocks: (28 spaces - level 7)
        - content (32 spaces - level 8)
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the simulate_drift block and fix it line by line
lines = content.split('\n')
fixed_lines = []

in_simulate = False
in_spinner = False
in_col2 = False
in_if_monitoring = False
in_alerts_if = False
in_for_loop = False

for i, line in enumerate(lines):
    stripped = line.lstrip()
    
    # Track block entry/exit
    if 'if simulate_drift:' in line and i > 570:
        in_simulate = True
        fixed_lines.append(line)
        continue
    
    if in_simulate and 'with st.spinner(' in line:
        in_spinner = True
        fixed_lines.append(line)
        continue
        
    if in_spinner and 'with col2:' in line:
        in_col2 = True
        fixed_lines.append(line)
        continue
    
    if in_col2 and "if monitoring['Needs Rebalancing']:" in line and 'Display status' in lines[i-1]:
        in_if_monitoring = True
        fixed_lines.append(line)
        continue
        
    if in_if_monitoring and "if monitoring['Alerts']:" in line:
        in_alerts_if = True
        fixed_lines.append(line)
        continue
        
    if in_alerts_if and 'for alert in' in line:
        in_for_loop = True
        fixed_lines.append(line)
        continue
    
    # Exit tracking
    if in_for_loop and ('}' in stripped and 'append' in lines[i-1]):
        in_for_loop = False
        
    if in_simulate and '# Show welcome message' in line:
        in_simulate = False
        fixed_lines.append(line)
        continue
    
    # Fix indentation based on current context
    if in_simulate and stripped:
        if in_for_loop:
            fixed_lines.append(' ' * 36 + stripped)
        elif in_alerts_if and ('alert_data' in stripped or 'alert_df' in stripped):
            fixed_lines.append(' ' * 32 + stripped)
        elif in_if_monitoring:
            if stripped.startswith('st.') or 'trades' in stripped or 'display_trades' in stripped:
                fixed_lines.append(' ' * 32 + stripped)
            elif 'if ' in stripped or 'else:' in stripped:
                fixed_lines.append(' ' * 28 + stripped)
            else:
                fixed_lines.append(' ' * 32 + stripped)
        elif in_col2:
            fixed_lines.append(' ' * 24 + stripped)
        elif in_spinner:
            fixed_lines.append(' ' * 20 + stripped)
        else:
            fixed_lines.append(' ' * 16 + stripped)
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(fixed_lines))

print('Comprehensive fix applied')
