import argparse
import sys
import RING.scripts.StageLab as Stage
import RING.lib.Site as New
from datetime import datetime

main_parser = argparse.ArgumentParser()
build_subparsers = main_parser.add_subparsers(title="build actions")

build_parser = build_subparsers.add_parser("build", parents=[main_parser],
                                    add_help=False,
                                    description="Build action",
                                    help="Build action")
build_parser.add_argument("--stage", help="stage N number of clusters in sandbox", dest='stagecount', type=int, default=0)
build_parser.add_argument("--site", help="build a new site", dest='sitecode')
build_parser.add_argument("--cac", help="CAC bandwidth", dest="bandwidth", type=int)
build_parser.add_argument("--carrier", help="Carrier 3 letter code (ATT/VZN/CTL)", dest="carrier")
build_parser.add_argument("--cmrg", help="Call Manager Group (ie: 2A)", dest="cmrg")
build_parser.add_argument("--tz", help="TimeZone", dest="tz", default="CMLocal")

buildargs = build_parser.parse_args()
stagelab = False
if buildargs.stagecount:
    stagelab = True
    Stage.StageLab(buildargs.stagecount)

if buildargs.sitecode:
    if not buildargs.bandwidth:
        build_parser.error("--site requires --cac")
    elif not buildargs.carrier:
        build_parser.error("--site requires --carrier")
    elif not buildargs.cmrg:
        build_parser.error("--site requires --cmrg")
    else:
        startTime = datetime.now()
        print(f"Building {buildargs.sitecode}...")
        site = New.Site(buildargs.sitecode, 1)
        site.AbbreviatedCluster = f"CL{site.ClusterNumber}"
        site.CAC = buildargs.bandwidth # TODO bandwidth calc
        site.Carrier = buildargs.carrier
        site.CallManagerGroup = buildargs.cmrg
        if site.Build():
            endTime = datetime.now() - startTime
            print(f"Build proccess for {buildargs.sitecode} completed in {endTime.total_seconds()} seconds")
elif not stagelab:
    build_parser.print_help()