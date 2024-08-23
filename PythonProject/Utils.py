# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.2f}'.format(input)