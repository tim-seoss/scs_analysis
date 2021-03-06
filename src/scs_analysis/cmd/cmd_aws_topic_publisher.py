"""
Created on 6 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSTopicPublisher(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -t TOPIC [-v]",
                                              version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--topic", "-t", type="string", nargs=1, action="store", dest="topic",
                                 help="topic path")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__opts.topic


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAWSTopicPublisher:{topic:%s, verbose:%s}" % (self.topic, self.verbose)
