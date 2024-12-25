import re
from typing import Optional

class ModulePattern:
    def __init__(self):
        self.module_id: str = ""
        self.command1: str = "00"
        self.command2: str = "30"
        self.type: str = "STANDARD"
        self.add_type: str = "STANDARD"
        self.use_zdd: bool = False
        self.has_rb_wait: bool = False
        self.register_type: str = "D1_D2"  # default register type

    def to_string(self) -> str:
        return f"""PATTERN READ_{self.module_id} {{
    MODULE_ID : #{self.module_id}
    COMMAND1 : #{self.command1}
    COMMAND2 : #{self.command2}
    TYPE : {self.type}
    ADD_TYPE : {self.add_type}
    USE_ZDD : {str(self.use_zdd).lower()}
    HAS_RB_WAIT : {str(self.has_rb_wait).lower()}
    REGISTER_TYPE : {self.register_type}
}}"""

def identify_register_type(module_text: str) -> str:
    register_patterns = {
        "D1_D2": r"ADD5_D1_D2",
        "D1B_D2B": r"ADD5_D1B_D2B",
        "D1C_D2C": r"ADD5_D1C_D2C",
        "CUSTOM": r"ADD5_([A-Za-z0-9]+_[A-Za-z0-9]+)"
    }
    
    for reg_type, pattern in register_patterns.items():
        if reg_type != "CUSTOM":
            if re.search(pattern, module_text):
                return reg_type
    
    custom_match = re.search(register_patterns["CUSTOM"], module_text)
    if custom_match:
        return custom_match.group(1)
    
    return "D1_D2"

def parse_module(module_text: str) -> Optional[ModulePattern]:
    pattern = ModulePattern()
    
    # Extract START address
    start_match = re.search(r'START #([0-9A-F]+)', module_text)
    if not start_match:
        return None
    
    pattern.module_id = start_match.group(1)
    
    # Extract commands
    commands = re.findall(r'TP<#([0-9A-F]+)\s+TS2', module_text)
    if commands:
        pattern.command1 = commands[0]
        if len(commands) > 1:
            pattern.command2 = commands[1]
    
    # Check for RB wait
    pattern.has_rb_wait = 'JNC1 G_LF000_RBWAT' in module_text
    
    # Determine type based on presence of JNI6/JNI7
    if 'JNI6' in module_text or 'JNI7' in module_text:
        pattern.type = "ADVANCED"
    
    # Identify register type
    pattern.register_type = identify_register_type(module_text)
    
    return pattern

def convert_file(input_file: str, output_file: str, include_rb_wait: bool = True):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        
        # Split into modules
        modules = content.split('MODULE BEGIN')
        
        # Process each module
        patterns = []
        for module in modules[1:]:  # Skip first empty split
            pattern = parse_module(module)
            if pattern:
                # Remove RB wait filtering - process all patterns
                patterns.append(pattern.to_string())
        
        # Write to output file
        with open(output_file, 'w') as f:
            f.write('\n\n'.join(patterns))
            
        print(f"Successfully converted {len(patterns)} patterns to {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")

# Example usage
convert_file('000_origin_pattern.txt', '001_pattern.txt')