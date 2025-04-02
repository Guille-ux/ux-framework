import re

TOKEN_PATTERNS = [
	("OR", r'\|'),
	("LPAREN", r'\('),
	("RPAREN", r'\)'),
	("ARROW", r'->'),
	("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
	("WHITESPACE", r'\s+')
]

class GramUxLexer:
	def __init__(self, source):
		self.source=source
		self.tokens=self.tokenize()
	def tokenize(self):
		tokens = []
		pos = 0
		while pos < len(self.source):
			match = None
			for pattern, token_type in TOKEN_PATTERNS:
				regex = re.compile(pattern)
				match = regex.match(self.source, pos)
				
