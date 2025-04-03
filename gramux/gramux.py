# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# 
# Copyright (c) 2025 Guillermo Leira Temes

TOKEN_PATTERNS = [
	("OR", '|'),
	("LPAREN", '('),
	("RPAREN", ')'),
	("ARROW", '->'),
	("AND", "&"),
	("NAME", "$")
]

class Token:
	def __init__(self, token_type, lexeme, value):
		self.type = token_type
		self.lexeme = lexeme
		self.value = value
	def __repr__(self):
		return f"{self.type} : {self.lexeme} : {self.value}"
	def __str__(self):
		return f"{self.type} : {self.lexeme} : {self.value}"
	def __eq__(self, other):
		return self.type == other.type and self.value == other.value

class GramUxLexer:
	def __init__(self, source):
		self.source=source
		self.tokens=self.tokenize()
	def tokenize(self):
		tokens = []
		lines = self.source.split("\n")
		for rule in lines:
			expr = rule.split()
			token_expr = []
			for word in expr:
				trigger = False
				for token_type, identity in TOKEN_PATTERNS:
					if identity == word:
						token_expr.append(Token(token_type, word, None))
						trigger = True
						break
				if not trigger:
					token_expr.append(Token("IDENTIFIER", word, word))
			tokens.append(token_expr)
		return tokens
# solo lo tokenizo, para facilitar el tratamiento, pero el usuario se encarga de procesar muchas cosas, como que puede ser cada identifier, esto es solo para las estructuras de como tiene que estar conformado cierta cosa.
