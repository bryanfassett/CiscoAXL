from CiscoAXL import AxlConnection, WSDL


def buildTransformations(conn, Pattern, SiteCode, AbbrevCluster, Carrier, Prefix)
    try:
        Pattern = "1.22233344[4-8]"# DN Range Calculation goes here
        prefixDigits = "111114"
        resp = conn.addCallingPartyTransformationPattern(
            callingPartyTransformationPattern = {
                'pattern' : Pattern,
                'description' : f"{SiteCode} SBC Outbound ANI Transform", #Update this
                'routePartitionName' : f"SBC_{AbbrevCluster}_{Carrier}_Outbound_ANI_xform_PT", #Update this
                'digitDiscardInstructionName' : "PreDot", #If Required
                'callingPartyTransformationMask' : prefixDigits,#string
                'callingPartyPrefixDigits' : True
            }
        )
        transforminfo = resp['return'].strip('{}').lower()
            
        return True, transforminfo
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

results = buildTransformations(conn, )
print(results)
