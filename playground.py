

from parse_sig_api import parse_sig

import requests
inp = 'TAKE 1 TABLET TWICE A DAY WITH MEALS for 3 weeks'
# inp = "INHALE 2 PUFFS INTO THE LUNGS EVERY day"
print(parse_sig(inp))
