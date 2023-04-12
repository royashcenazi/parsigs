from parsigs.parse_sig_api import parse_sig

# inp = 'TAKE 1 TABLET TWICE A DAY WITH MEALS for 3 weeks'
# inp = "INHALE 2 PUFFS INTO THE LUNGS EVERY day"

inp = "take up to 3 tablets every day for 2 weeks"
print(parse_sig(inp))
