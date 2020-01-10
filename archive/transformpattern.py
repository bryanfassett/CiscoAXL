DNRange = "1-222-333-4441 to 4519"
DNRange = DNRange.replace('-','')
NPANXX = DNRange[1:7]
first7 = str(1) + NPANXX
firstDN = DNRange[:11]
prefix = DNRange[:6]
lastDN = first7 + DNRange[-4:]
firstDNLast5 = firstDN[-5:]
lastDNLast5 = lastDN[-5:]
print(NPANXX)
print(first7)
print(prefix)
print(firstDN)
print(lastDN)
print(firstDNLast5)
print(lastDNLast5)

i = 0
while firstDN[i] == lastDN[i]:
    i += 1
matchinePlaces = i
print (matchinePlaces)
nonMatchingPlaces = 11-i
print (nonMatchingPlaces)

# #THIS PRINTS THE 5 DIGIT TRANSPATTERN FROM A DID RANGE
# print (f'{firstDN[i-11:]}  {lastDN[i-11:]}')
# easyRange = firstDN[:matchinePlaces] + 'X' * nonMatchingPlaces
# easyShortRange = easyRange[-5:]
# print(easyShortRange)

noMatchStart = firstDN[i-11:]
print (noMatchStart)
noMatchEnd = lastDN[i-11:]
print(noMatchEnd)

patternList = []
noMatchDiff = int(noMatchEnd) - int(noMatchStart)
if nonMatchingPlaces == 1:
    exactPattern1 = f"{firstDNLast5[:5-(nonMatchingPlaces)]}[{noMatchStart[-1]}-{noMatchEnd[-1]}]"
    patternList.append(exactPattern1)

# THERE ARE 2 PLACES IN THE RANGE
if nonMatchingPlaces == 2:
    exactPattern1 = f"{firstDNLast5[:6-(nonMatchingPlaces)]}[{noMatchStart[-1]}-9]"
    patternList.append(exactPattern1)
    if int(noMatchEnd[0])-int(noMatchStart[0]) == 1:
        if noMatchEnd[-1] == "0":
            exactPattern3 = f"{lastDNLast5[:6-(nonMatchingPlaces)]}0]"
            patternList.append(exactPattern3)
        else:
            exactPattern3 = f"{lastDNLast5[:6-(nonMatchingPlaces)]}[0-{noMatchEnd[-1]}]"
            patternList.append(exactPattern3)
    elif int(noMatchEnd[0])-int(noMatchStart[0]) == 2:
        exactPattern2 = f"{firstDNLast5[:5-(nonMatchingPlaces)]}{int(noMatchEnd[:1])-1}X"
        patternList.append(exactPattern2)
        if noMatchEnd[-1] == "0":
            exactPattern3 = f"{lastDNLast5[:6-(nonMatchingPlaces)]}0]"
            patternList.append(exactPattern3)
        else:
            exactPattern3 = f"{lastDNLast5[:6-(nonMatchingPlaces)]}[0-{noMatchEnd[-1]}]"
            patternList.append(exactPattern3)
    else:
        exactPattern2 = f"{firstDNLast5[:5-(nonMatchingPlaces)]}[{int(noMatchStart[:1])+1}-{int(noMatchEnd[:1])-1}]X"
        patternList.append(exactPattern2)
        if noMatchEnd[-1] == "0":
            exactPattern3 = f"{lastDNLast5[:6-(nonMatchingPlaces)]}0]"
            patternList.append(exactPattern3)
        else:
            exactPattern3 = f"{lastDNLast5[:6-(nonMatchingPlaces)]}[0-{noMatchEnd[-1]}]"
            patternList.append(exactPattern3)

# print(f"Non Matching Places {nonMatchingPlaces}")
print(patternList)
