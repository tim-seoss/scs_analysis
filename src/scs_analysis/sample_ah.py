#!/usr/bin/env python3

"""
Created on 11 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The sample_airwatch utility is used to

SYNOPSIS
sample_airwatch.py { -z | TIMEZONE_NAME }

EXAMPLES
aws_topic_history.py south-coast-science-dev/production-test/loc/1/climate -s 2018-10-28T00:00:00+00:00 \
-e 2018-10-28T03:00:00+00:00 | sample_airwatch.py -n Europe/Paris

DOCUMENT EXAMPLE - INPUT
{"val": {"hmd": 49.7, "tmp": 17.5}, "rec": "2018-10-28T00:00:46.037+00:00", "tag": "scs-be2-2"}

DOCUMENT EXAMPLE - OUTPUT
{"val": {"hmd": 49.7, "tmp": 17.5}, "rec": "2018-10-28T01:00:46.037+01:00", "tag": "scs-be2-2"}

RESOURCES
https://en.wikipedia.org/wiki/ISO_8601
http://pytz.sourceforge.net
"""

import json
import sys

from collections import OrderedDict

from scs_analysis.cmd.cmd_sample_airwatch import CmdSampleAirwatch

from scs_core.data.airwatch import AirwatchRecord
from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_core.climate.absolute_humidity import AbsoluteHumidity

from scs_core.location.timezone import Timezone


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    timezone = None
    zone = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSampleAirwatch()

    # if not cmd.is_valid():
    #     cmd.print_help(sys.stderr)
    #     exit(2)

    if cmd.verbose:
        print("sample_ah: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        path = 'val.sht'


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                break

            target = PathDict()

            if datum.has_path('rec'):
                target.copy(datum, 'rec')

            target.copy(datum, path)

            rh = datum.node(path + '.hmd')
            t = datum.node(path + '.tmp')

            ah = AbsoluteHumidity.from_rh_t(rh, t)

            target.append(path + '.ah', round(ah, 1))

            # target.append(path + '.src', value)
            # target.append(self.__path + '.avg', round(avg, self.__precision))

            # report...
            print(JSONify.dumps(target.node()))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("sample_ah: KeyboardInterrupt", file=sys.stderr)
