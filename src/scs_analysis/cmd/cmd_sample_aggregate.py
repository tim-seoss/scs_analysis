"""
Created on 24 Oct 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.data.checkpoint_generator import CheckpointGenerator


# --------------------------------------------------------------------------------------------------------------------

class CmdSampleAggregate(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-m] [-t] [-f] [-v] -c HH:MM:SS [PATH_1..PATH_N]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--checkpoint", "-c", type="string", nargs=1, action="store", dest="checkpoint",
                                 help="a time specification as **:/5:00")

        self.__parser.add_option("--min-max", "-m", action="store_true", dest="min_max", default=False,
                                 help="report min and max in addition to midpoint")

        self.__parser.add_option("--include-tag", "-t", action="store_true", dest="include_tag", default=False,
                                 help="include tag field, if present")

        self.__parser.add_option("--fill", "-f", action="store_true", dest="fill", default=False,
                                 help="fill output with checkpoints missing from input")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.checkpoint_generator is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def checkpoint_generator(self):
        try:
            return CheckpointGenerator.construct(self.__opts.checkpoint)

        except (AttributeError, ValueError):
            return None


    @property
    def nodes(self):
        return self.__args if len(self.__args) > 0 else [None]


    @property
    def min_max(self):
        return self.__opts.min_max


    @property
    def include_tag(self):
        return self.__opts.include_tag


    @property
    def fill(self):
        return self.__opts.fill


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdSampleAggregate:{checkpoint:%s, min_max:%s, include_tag:%s, fill:%s, verbose:%s, nodes:%s}" %  \
               (self.__opts.checkpoint, self.min_max, self.include_tag, self.fill, self.verbose, self.nodes)
