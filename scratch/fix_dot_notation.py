import re

# Update Lexer
with open('compiler/frontend/lexer.py', 'r') as f:
    lexer = f.read()
    
# Change regex for ID_OR_KEY to include lala. prefix
lexer = lexer.replace(
    "('ID_OR_KEY',   r'[A-Za-z_][A-Za-z0-9_]*')",
    "('ID_OR_KEY',   r'lala\\.[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*')"
)
# Change keywords from lala_ to lala.
lexer = lexer.replace('"lala_', '"lala.')
with open('compiler/frontend/lexer.py', 'w') as f:
    f.write(lexer)

# Update Parser
with open('compiler/frontend/parser.py', 'r') as f:
    parser = f.read()
parser = parser.replace('"lala_', '"lala.')
with open('compiler/frontend/parser.py', 'w') as f:
    f.write(parser)
