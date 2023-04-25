from parsigs.parse_sig_api import parse_sig

# inp = 'TAKE 1 TABLET TWICE A DAY WITH MEALS for 3 weeks'
# inp = "INHALE 2 PUFFS INTO THE LUNGS EVERY"

# inp1 = "Take 10 units of once every day at night"

# inp1 = "Take 50 mcg of eltroxin 5 times a week and than take 100 mcg twice a week"

inp1 = "1 TAB BID"

print(parse_sig(inp1))
