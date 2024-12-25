from dataclasses import dataclass
from enum import Enum, auto
import ply.lex as lex
import ply.yacc as yacc

# Data structures
class PatternType(Enum):
    STANDARD = auto()
    ADVANCED = auto()  # Changed SPECIAL to ADVANCED

class AddType(Enum):
    STANDARD = auto()
    EXTENDED = auto()

@dataclass
class Pattern:
    name: str
    module_id: str
    command1: str
    command2: str
    pattern_type: PatternType
    add_type: AddType
    use_zdd: bool
    has_rb_wait: bool  # New field
    register_type: str  # New field

# Lexer
class PatternLexer:
    tokens = (
        'PATTERN', 'READ', 'HEX_ID', 'LBRACE', 'RBRACE', 'COLON',
        'MODULE_ID', 'COMMAND1', 'COMMAND2', 'TYPE',
        'ADD_TYPE', 'USE_ZDD', 'HAS_RB_WAIT', 'REGISTER_TYPE',
        'HEX', 'STANDARD', 'ADVANCED', 'EXTENDED',
        'TRUE', 'FALSE', 'REG_TYPE'  # Changed STRING to REG_TYPE
    )

    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_COLON = r':'

    def t_PATTERN(self, t):
        r'PATTERN'
        return t
        
    def t_READ(self, t):
        r'READ_[0-9A-Fa-f]+'  # READ_ 다음의 16진수를 포함
        t.value = t.value[5:]  # READ_ 제거
        return t



    def t_COMMAND1(self, t):
        r'COMMAND[12]'  # COMMAND1과 COMMAND2를 하나의 규칙으로
        return t

    def t_COMMAND2(self, t):
        r'COMMAND2'
        return t

    def t_MODULE_ID(self, t):
        r'MODULE_ID'
        return t

    def t_TYPE(self, t):
        r'TYPE'
        return t

    def t_ADD_TYPE(self, t):
        r'ADD_TYPE'
        return t

    def t_USE_ZDD(self, t):
        r'USE_ZDD'
        return t

    def t_HAS_RB_WAIT(self, t):
        r'HAS_RB_WAIT'
        return t

    def t_REGISTER_TYPE(self, t):
        r'REGISTER_TYPE'
        return t

    def t_STANDARD(self, t):
        r'STANDARD'
        return t

    def t_ADVANCED(self, t):
        r'ADVANCED'
        return t

    def t_EXTENDED(self, t):
        r'EXTENDED'
        return t

    def t_TRUE(self, t):
        r'true|TRUE'
        return t

    def t_FALSE(self, t):
        r'false|FALSE'
        return t

    def t_HEX(self, t):
        r'\#[0-9A-Fa-f]+'
        t.value = t.value[1:]  # Remove '#' prefix
        return t

    def t_REG_TYPE(self, t):
        r'D[1-9][A-Z]?_D[1-9][A-Z]?(?:_D[1-9][A-Z]?)?'
        return t

    # 토큰 우선순위를 위해 정렬된 순서로 배치
    tokens = (
        'PATTERN', 'READ', 'LBRACE', 'RBRACE', 'COLON',
        'MODULE_ID', 'COMMAND1', 'COMMAND2', 'TYPE',
        'ADD_TYPE', 'USE_ZDD', 'HAS_RB_WAIT', 'REGISTER_TYPE',
        'HEX', 'STANDARD', 'ADVANCED', 'EXTENDED',
        'TRUE', 'FALSE', 'REG_TYPE'
    )

    t_ignore = ' \t\n'

    def t_error(self, t):
        raise SyntaxError(f"Illegal character '{t.value[0]}' at position {t.lexpos}")

    def __init__(self, **kwargs):
        self.lexer = None
        
    def build(self, **kwargs):
        try:
            self.lexer = lex.lex(module=self, **kwargs)
        except Exception as e:
            print(f"Error building lexer: {str(e)}")
            raise


class PatternParser:
    def __init__(self):
        self.lexer = PatternLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.patterns = []

    def p_patterns(self, p):
        '''patterns : patterns pattern_def
                   | pattern_def'''
        if len(p) == 2:
            self.patterns = [p[1]]
        else:
            self.patterns.append(p[2])
        p[0] = self.patterns

    def p_pattern_def(self, p):
        '''pattern_def : PATTERN READ LBRACE fields RBRACE'''
        p[0] = Pattern(name=f"READ_{p[2]}", **p[4])


    def p_fields(self, p):
        '''fields : field_list'''
        p[0] = {
            'module_id': '',
            'command1': '',
            'command2': '',
            'pattern_type': PatternType.STANDARD,
            'add_type': AddType.STANDARD,
            'use_zdd': False,
            'has_rb_wait': False,
            'register_type': 'D1_D2',
            **p[1]
        }

    def p_field_list(self, p):
        '''field_list : field_list field
                     | field'''
        if len(p) == 3:
            p[1].update(p[2])
            p[0] = p[1]
        else:
            p[0] = p[1]

    def p_field(self, p):
        '''field : MODULE_ID COLON HEX
                | COMMAND1 COLON HEX
                | COMMAND2 COLON HEX
                | TYPE COLON type_value
                | ADD_TYPE COLON add_type_value
                | USE_ZDD COLON bool_value
                | HAS_RB_WAIT COLON bool_value
                | REGISTER_TYPE COLON REG_TYPE'''  # Updated this line
        key = p[1].lower()
        if key in ['module_id', 'command1', 'command2']:
            p[0] = {key: p[3]}
        elif key == 'type':
            p[0] = {'pattern_type': p[3]}
        elif key == 'add_type':
            p[0] = {'add_type': p[3]}
        elif key == 'use_zdd':
            p[0] = {'use_zdd': p[3]}
        elif key == 'has_rb_wait':
            p[0] = {'has_rb_wait': p[3]}
        elif key == 'register_type':
            p[0] = {'register_type': p[3]}

    def p_type_value(self, p):
        '''type_value : STANDARD
                     | ADVANCED'''
        p[0] = PatternType[p[1]]

    def p_add_type_value(self, p):
        '''add_type_value : STANDARD
                         | EXTENDED'''
        p[0] = AddType[p[1]]

    def p_bool_value(self, p):
        '''bool_value : TRUE
                     | FALSE'''
        p[0] = p[1] in ['TRUE', 'true']

    def p_error(self, p):
        if p:
            raise SyntaxError(f"Syntax error at '{p.value}'")
        else:
            raise SyntaxError("Syntax error at EOF")
        
    def generate_code(self, pattern: Pattern) -> str:
        output = []
        output.append("MODULE BEGIN")
        output.append(f"\tSTART #{pattern.module_id}")
        
        if pattern.pattern_type == PatternType.ADVANCED:
            output.append("\tJNI7 .\t\t\t\t\t  TS12")
            
        output.append(f"\tJSR G_LF001_CMDI                CE0  TP<#{pattern.command1}       TS2")
        
        # Add command based on type and register_type
        if pattern.add_type == AddType.STANDARD:
            output.append(f"\tJSR G_LF001_ADD5_{pattern.register_type}          CE0               TS1")
        else:  # EXTENDED
            output.append(f"\tJSR G_LF001_ADD6_{pattern.register_type}_D3B          CE0               TS1")
            
        if pattern.use_zdd:
            output.append("\tJSR G_LF001_ZDD5_D1B_D2B          CE0               TS1")
            
        output.append(f"\tJSR G_LF001_CMDI_100NS           CE0  TP<#{pattern.command2}       TS2")
        
        if pattern.pattern_type == PatternType.ADVANCED:
            output.append("\tJNI6 .\t\t\t\t\t TS12")
        elif pattern.has_rb_wait:
            output.append("\tJNC1 G_LF000_RBWAT              CE0              TS1")
            
        output.append("\tSTPS  TS1")
        output.append("MODULE END")
        return "\n".join(output)


def parse_pattern_file(filename: str) -> list[Pattern]:
    with open(filename, 'r') as f:
        content = f.read()
    parser = PatternParser()
    return parser.parser.parse(content, lexer=parser.lexer.lexer)

def main():
    try:
        patterns = parse_pattern_file("001_pattern.txt")
        parser = PatternParser()
        
        with open("002_final_result.txt", "w") as f:
            for i, pattern in enumerate(patterns):
                code = parser.generate_code(pattern)
                f.write(code)
                if i < len(patterns) - 1:
                    f.write("\n\n")
                    
        print("Patterns generated successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()