#!/usr/bin/env python3

"""
Created on 20 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis

DESCRIPTION
The csv_collator utility is used to separate the input JSON documents according to the upper and lower bounds of a
sequence of bins. For each bin, assignment follows the rule:

lower bound <= value < upper bound

The upper and lower bounds for the data set should be specified, along with a step size. The number of bins required
to service this domain is calculated automatically. Additionally, a file (and path) prefix for the generated CSV files
must be specified, along with the path identifying the leaf node in the input document where the value is to be found.

Documents that do not contain a field at the specified path, or have values that cannot be evaluated as a float, are
ignored. Likewise, values outside the upper and lower bounds are ignored.

If the --verbose flag is used, a summary of the bin assignments is written to stderr.

SYNOPSIS
csv_collator.py -l LOWER_BOUND -u UPPER_BOUND -d DELTA -f FILE_PREFIX [-v] PATH

EXAMPLES
csv_reader.py alphasense_303_2018-08.csv |
csv_collator.py -l 5.0 -u 21.0 -d 1.0 -f collation/alphasense_303_2018-08 -v val.sht.hmd.aH
"""

import sys

from scs_analysis.cmd.cmd_csv_collator import CmdCSVCollator
from scs_analysis.helper.csv_collator import CSVCollator

from scs_core.data.path_dict import PathDict


# TODO: collate by datetime interval?

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    collator = None

    document_count = 0
    processed_count = 0

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdCSVCollator()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("csv_collator: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        collator = CSVCollator.construct(cmd.lower, cmd.upper, cmd.delta, cmd.file_prefix)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            jstr = line.strip()
            datum = PathDict.construct_from_jstr(jstr)

            if datum is None:
                break

            document_count += 1

            if cmd.path not in datum.paths():
                continue

            try:
                value = float(datum.node(cmd.path))
            except (TypeError, ValueError):
                continue

            if not collator.collate(value, jstr):
                continue

            processed_count += 1


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("csv_collator: KeyboardInterrupt", file=sys.stderr)

    finally:
        if collator is not None:
            collator.close()

            if cmd.verbose:
                for b in collator.bins:
                    print("csv_collator: lower: %4.1f upper: %4.1f count: %5d" % (b.lower, b.upper, b.count),
                          file=sys.stderr)

            print("csv_collator: documents: %d processed: %d" % (document_count, processed_count), file=sys.stderr)
