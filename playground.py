from parsigs.parse_sig_api import parse_sig

# inp = 'TAKE 1 TABLET TWICE A DAY WITH MEALS for 3 weeks'
# inp = "INHALE 2 PUFFS INTO THE LUNGS EVERY"

inp = "Take 1 tablet of aderol 3 times a week"
inp1 = "Take 1 tablet of ibuprofen 3 times a month"
print(parse_sig(inp1))
