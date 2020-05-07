import re
import subprocess

class Httperf(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.args = []
        self.parser = False

        # Popping path from kwargs if exist
        if 'path' in kwargs:
            self.path = kwargs['path']
            del kwargs['path']
        else:
            self.path = 'httperf'

        # Args for each argument which is not key:value based (hog, ssl...)
        for argument in args:
            if argument not in set(self.__params().keys()):
                raise Exception("Invalid httperf option passed: {}".format(argument))
            self.args.append("--%s" % argument)

        # Arguments passed to httperf
        for key in kwargs:
            if key not in set(self.__params().keys()):
                raise Exception("Invalid httperf option passed:: " + key)
            self.params[key] = kwargs[key]

    def update_option(self, key, val):
        self.params[key] = val

    def run(self):
        try:
            self.results = subprocess.check_output(self.__cmd(),
                                                   shell=True,
                                                   stderr=subprocess.STDOUT,
                                                   close_fds=True)
            if self.parser:
                return HttperfParser.parse(self.results)
            else:
                return self.results
        except subprocess.CalledProcessError as er:
            return {"error": er.output}

    def display_params(self):
        h = Httperf()
        for param in list(h.__params().keys()):
            print(param)

    def __cmd(self):
        args = [self.path]
        if self.args:
            args += self.args

        for key in list(self.params.keys()):
            val = str(self.params[key])
            key_dash = key.replace('_', '-')
            if key in self.__boolean_params():
                args.append('--%s' % key_dash)
            else:
                args.append('--%s="%s"' % (key_dash, val))

        return ' '.join(args)

    def __boolean_params(self):
        return [
            "hog",
            "no_host_hdr",
            "retry_on_failure",
            "session_cookies",
            "ssl",
            "ssl_no_reuse",
            "verbose",
            "version"
        ]

    def __params(self):
        return {
            "add_header": None,
            "burst_length": None,
            "client": None,
            "close_with_reset": None,
            "debug": None,
            "failure_status": None,
            "hog": None,
            "http_version": None,
            "max_connections": None,
            "max_piped_calls": None,
            "method": None,
            "no_host_hdr": None,
            "num_calls": None,
            "num_conns": None,
            "period": None,
            "port": None,
            "print_reply": None,
            "print_request": None,
            "rate": None,
            "recv_buffer": None,
            "retry_on_failure": None,
            "send_buffer": None,
            "server": None,
            "server_name": None,
            "session_cookies": None,
            "ssl": None,
            "ssl_ciphers": None,
            "ssl_no_reuse": None,
            "think_timeout": None,
            "timeout": None,
            "uri": None,
            "verbose": None,
            "version": None,
            "wlog": None,
            "wsess": None,
            "wsesslog": None,
            "wset": None
        }

class HttperfParser(object):

    def parse(self, result_string, options = {}):
        # constants for the parse
        self.exps = self.__expressions()
        vexpression = re.compile(
            "^Connection lifetime = ([-+]?[0-9]*\.?[0-9]+)")

        # items that are accumulated during the parse
        verbose_connection_times = []
        verbose_output_lines = []
        unknown_lines = []
        xtrace_headers = []

        # helper functions for oddball lines. they're mostly
        # oddball because i don't know where they can appear
        # in the output so i check each line for them.
        def get_verbose_connection_time(line):
            if (vexpression.match(line)):
                verbose_connection_times.append(match.group(1))
            else:
                unknown_lines.append(line)

        def get_verbose_output_line(line):
            verbose_output_lines.append(line)

        special_starts = {
            "Connection lifetime =": get_verbose_connection_time,
            "httperf: ": get_verbose_output_line
        }

        # the return value - httperf's output, parsed, as a dict
        self.matches = {}

        # standard states with transitions
        transitions = self.__transitions()

        # initial state
        want = 'command'

        def change_want(new_want):
            nonlocal want
            if ('state-changes' in options and options['state-changes']):
                print("state change {} => {}".format(want, new_want))
            want = new_want


        lines = result_string.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i]
            i += 1

            if line == "":
                continue

            found = False
            for start in special_starts:
                if line.startswith(start):
                    special_starts[start](line)
                    found = True
                if (found):
                    break
            if found:
                continue

            # if it's an unconditional transition, handle it here.
            if (want in transitions):
                if (self.__find_and_store(want, line)):
                    change_want(transitions[want])
                    continue

            # keep processing header lines until a non-header lines
            # shows up.
            if (want == 'maybe_headers'):
                if (line.startswith('RH')):
                    match = self.exps['header_xtrace'].match(line)
                    if (match):
                        xtrace_headers.append(match.group(1))
                    continue
                elif (line.startswith('RS')):
                    continue
                else:
                    # it's a little awkward but we have to go past the
                    # headers to know that there are no more, so back up
                    # and move to the next state.
                    change_want('total')
                    i -= 1
                    continue

            # when done any leftover lines are unknown. currently
            # session lines are not parsed for some reason.
            if (want == 'done'):
                unknown_lines.append(line)
                continue

        # the following ifs add the keys only if they are not empty.
        if (len(verbose_connection_times)):
            self.matches['connection_times'] = verbose_connection_times
            for pct in self.__percentiles():
                self.matches["connection_time_" + str(pct) + "_pct"] = \
                    self.__calculate_percentiles(pct, verbose_connection_times)

        if (len(xtrace_headers)):
            self.matches['header_xtrace'] = xtrace_headers

        if (len(unknown_lines)):
            self.matches['unknown_lines'] = unknown_lines

        if (len(verbose_output_lines)):
            self.matches['verbose_output_lines'] = verbose_output_lines

        return self.matches
    # end parse

    def __find_and_store(self, want, line):
        regex = self.exps[want]
        prefix = want
        if isinstance(regex, dict):
            prefix = regex['prefix']
            regex = regex['re']
        match = regex.match(line)
        if (match):
            self.__store_matches(prefix, match)
            return True

        return False

    def __store_matches(self, prefix, match):
        # do the matches have names?
        mapping = match.groupdict()
        if (len(mapping)):
            for key in mapping:
                self.matches[prefix + '_' + key] = mapping[key]
        else:
            self.matches[prefix] = match.group(1)


    def __calculate_percentiles(self, pct, vct):
        if len(vct) == 1:
            return vct[0]

        sorted_vct = sorted(vct)

        if len(vct) == 2:
            return sorted_vct[1]

        sorted_vct = sorted(vct)
        index = int((float(len(vct))/100 * float(pct)))
        return sorted(vct)[index]

    def __percentiles(self):
        return [75, 80, 85, 90, 95, 99]


    @staticmethod
    def __transitions():
        # each key is a state and each value is the state to
        # transition to when the key state has been matched.
        return {
            'command': 'maybe_headers',
            'total': 'connection',
            'connection': 'connection_time',
            'connection_time': 'connection_time_connect',
            'connection_time_connect': 'connection_length',
            'connection_length': 'request',
            'request': 'request_size',
            'request_size': 'reply_rate',
            'reply_rate': 'reply_time',
            'reply_time': 'reply_size',
            'reply_size': 'reply_status',
            'reply_status': 'cpu_time',
            'cpu_time': 'net_io',
            'net_io': 'errors1',
            'errors1': 'errors2',
            'errors2': 'done',
        }

    @staticmethod
    def __expressions():
        # abstract the integer and floating point regex patterns
        i = "[0-9]+"
        fp = "[-+]?[0-9]*\.?[0-9]+"
        redict = {'i': i, 'fp': fp}

        #
        # each key is the name of a parsing state, known in the parser as
        # "want". the value is either a compiled regular expression or it
        # is a dict containing a regular expression and a prefix.
        #
        # the regular expression either has a single group or has multiple
        # named groups. the key for the parsing state is used as name of
        # the value when there is a single group. when there are multiple
        # groups the key is combined with the group name to make the name
        # of the value (and "_" is inserted between).
        #
        # when the value is a dict, not a compiled regular expression, then
        # the prefix is used instead of the key/parsing state name.
        #
        return {
            "command": re.compile("^(httperf .+)$"),

            # Maximum connect burst length:
            "max_connect_burst_length": re.compile("Maximum connect burst length: ({fp})$"),

            # Total: connections 1 requests 30 replies 30 test-duration 0.060 s
            "total": re.compile((
                "^Total: connections (?P<connections>{i}) "
                "requests (?P<requests>{i}) "
                "replies (?P<replies>{i}) "
                "test-duration (?P<test_duration>{fp})"
            ).format(**redict)),

            # Connection rate: 16.6 conn/s (60.4 ms/conn, <=1 concurrent connections)
            "connection": re.compile("^Connection rate: (?P<rate_per_sec>{fp}) conn/s \((?P<rate_ms_conn>{fp}) ms/conn, .+ concurrent connections\)".format(**redict)),

            # Connection time [ms]: min 60.5 avg 60.5 max 60.5 median 60.5 stddev 0.0
            "connection_time": re.compile((
                "^Connection time \[ms\]: min (?P<min>{fp}) "
                "avg (?P<avg>{fp}) "
                "max (?P<max>{fp}) "
                "median (?P<median>{fp}) "
                "stddev (?P<stddev>{fp})"
            ).format(**redict)),

            # Connection time [ms]: connect 0.1
            "connection_time_connect": re.compile("^Connection time \[ms\]: connect ({fp})$".format(**redict)),

            # Connection length [replies/conn]: 30.000
            "connection_length": re.compile("^Connection length \[replies\/conn\]: ({fp})$".format(**redict)),

            # Request rate: 496.6 req/s (2.0 ms/req)
            "request": re.compile((
                "^Request rate: (?P<rate_per_sec>{fp}) req\/s "
                "\((?P<rate_ms_request>{fp}) ms\/req\)"
            ).format(**redict)),

            # Request size [B]: 121.0
            "request_size": re.compile("^Request size \[B\]: ({fp})$".format(**redict)),

            # Reply rate [replies/s]: min 0.0 avg 0.0 max 0.0 stddev 0.0 (0 samples)
            "reply_rate": re.compile((
                "^Reply rate \[replies\/s\]: min (?P<min>{fp}) "
                "avg (?P<avg>{fp}) "
                "max (?P<max>{fp}) "
                "stddev (?P<stddev>{fp}) "
                "\((?P<samples>{fp}) samples\)"
            ).format(**redict)),

            # Reply time [ms]: response 2.0 transfer 0.0
            "reply_time": re.compile((
                "^Reply time \[ms\]: response (?P<response>{fp}) "
                "transfer (?P<transfer>{fp})"
            ).format(**redict)),

            # Reply size [B]: header 287.0 content 871.0 footer 0.0 (total 1158.0)
            "reply_size": re.compile((
                "^Reply size \[B\]: header (?P<header>{fp}) "
                "content (?P<content>{fp}) "
                "footer (?P<footer>{fp}) "
                "\(total (?P<total>{fp})\)"
            ).format(**redict)),

            # Reply status: 1xx=0 2xx=29 3xx=0 4xx=0 5xx=1
            "reply_status": {
                're': re.compile((
                    "^Reply status: 1xx=(?P<status_1xx>{i}) "
                    "2xx=(?P<status_2xx>{i}) "
                    "3xx=(?P<status_3xx>{i}) "
                    "4xx=(?P<status_4xx>{i}) "
                    "5xx=(?P<status_5xx>{i})"
                ).format(**redict)),
                'prefix': 'reply'
            },

            # CPU time [s]: user 0.03 system 0.03 (user 52.3% system 47.1% total 99.3%)
            "cpu_time": re.compile((
                "^CPU time \[s\]: user (?P<user_sec>{fp}) "
                "system (?P<system_sec>{fp}) \("
                "user (?P<user_pct>{fp})% "
                "system (?P<system_pct>{fp})% "
                "total (?P<total_pct>{fp})%"
                "\)"
            ).format(**redict)),

            # Net I/O: 621.0 KB/s (5.1*10^6 bps)
            "net_io": re.compile((
                "^Net I\/O: (?P<kb_sec>{fp}) KB\/s "
                "\((?P<bps>{fp}.+) bps\)"
            ).format(**redict)),

            # Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
            # Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
            "errors1": {
                're': re.compile((
                    "^Errors: total (?P<total>{i}) "
                    "client-timo (?P<client_timeout>{i}) "
                    "socket-timo (?P<socket_timeout>{i}) "
                    "connrefused (?P<conn_refused>{i}) "
                    "connreset (?P<conn_reset>{i})"
                ).format(**redict)),
                'prefix': 'errors'
            },
            "errors2": {
                're': re.compile((
                    "^Errors: fd-unavail (?P<fd_unavail>{i}) "
                    "addrunavail (?P<addr_unavail>{i}) "
                    "ftab-full (?P<ftab_full>{i}) "
                    "other (?P<other>{i})"
                ).format(**redict)),
                'prefix': 'errors'
            },


            # consider session lines?
            # Session rate [sess/s]: min 0.00 avg 14.42 max 0.00 stddev 0.00 (1/1)
            # Session: avg 1.00 connections/session
            # Session lifetime [s]: 0.1
            # Session failtime [s]: 0.0
            # Session length histogram: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1

            # Headers of interest
            "header_xtrace": re.compile("^RH[0-9]+:X-Trace: ([0-9A-F]{59}1)", re.I)
        }

if (__name__ == '__main__'):
    import timeit
    import sys

    f = open(sys.argv[1])

    data = f.read()

    h = HttperfParser()

    def test():
        h.parse(data)

    print('timeit {}', timeit.timeit('test()', number = 100, globals = globals()))
    #print(h.parse(data))
