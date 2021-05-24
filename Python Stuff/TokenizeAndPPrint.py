import tokenize
from pprint import pprint
from functools import partial

code = """
for i in range(4):
	if not i%2:
		print(i)
""".strip()

codelines = iter(code.splitlines())
code_tokens = list(tokenize.generate_tokens(partial(next, codelines)))

pprint(list(map(tokenize.TokenInfo._asdict, code_tokens)))
