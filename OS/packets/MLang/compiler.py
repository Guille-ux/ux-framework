import src.swelcomp.compiler as comp
from src.utils import findutils as find
from src.utils import parser

print(str(find.find_funcs("func hola: {\nprint hola \n}"))) # prueba de findutils [éxito]
print(parser.parse_var("var hola 5 * 5")) # prueba de var_parser [éxito]
