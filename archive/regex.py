

def regexRangeDigits(start,stop):
  if start == stop:
    return str(start)
  return f'[{start}-{stop}]'

# generate list of regular expressions for the number range [start,end[
def genRangeRegex(start, end):
  if start <= 0:
    raise ValueError('only ranges of positive numbers supported')

  print (f'Creating patterns for {start} to {end}.')
  if start >= end:
    return []

  digitsStart = str(start)
  digitsEnd   = str(end)
  lastDigitStart = start%10

  if start//10 == (end-1)//10: # floor division to drop remainders
    lastDigitStop = (end-1)%10 # find the remainder for the last number
    # Concatenate the last digit in the first range
    regexAll = digitsStart[:-1] + regexRangeDigits(lastDigitStart,lastDigitStop)
    return [regexAll]

  regexListStart = [] # at most one regular expression for going up to first multiple of 10
  if lastDigitStart != 0:
    regexStart = digitsStart[:-1] + regexRangeDigits(lastDigitStart,9)
    regexListStart.append(regexStart)

  regexListEnd = [] # at most one regular expression for going up from last multiple of 10
  lastDigitEnd = end%10
  if lastDigitEnd != 0:
    regexEnd = digitsEnd[:-1] + regexRangeDigits(0,lastDigitEnd)
    regexListEnd.append(regexEnd)

  regexListMidTrunc = genRangeRegex((start+9)//10, end//10)
  regexListMid = [r+'X' for r in regexListMidTrunc]

  return regexListStart + regexListMid + regexListEnd

result = genRangeRegex(55440,55568)
print(result)
