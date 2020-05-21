import os, sys

localpath = os.path.join(os.path.dirname(__file__), "..", "httperfpy")
# make this path first so the local version is used even if there
# is another version on the system.
sys.path.insert(0, localpath)

from httperfpy import *

global httperf_path, httperf_results, httperf_verbose_results

httperf_path = str.strip(os.popen("which httperf").read())

if httperf_path == '':
    raise Exception("httperf must be install")

httperf_results = """
httperf --client=0/1 --server=localhost --port=80 --uri=/ --send-buffer=4096 --recv-buffer=16384 --num-conns=1 --num-calls=1
httperf: warning: open file limit > FD_SETSIZE; limiting max. # of open files to FD_SETSIZE
Maximum connect burst length: 0

Total: connections 1 requests 1 replies 1 test-duration 0.000 s

Connection rate: 2114.1 conn/s (0.5 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 0.6 avg 0.6 max 0.6 median 0.5 stddev 0.0
Connection time [ms]: connect 0.1
Connection length [replies/conn]: 1.000

Request rate: 2114.1 req/s (0.5 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 0.6 avg 0.7 max 0.8 stddev 0.0 (4 samples)
Reply time [ms]: response 0.4 transfer 0.0
Reply size [B]: header 216.0 content 151.0 footer 0.0 (total 367.0)
Reply status: 1xx=0 2xx=1 3xx=0 4xx=0 5xx=0

CPU time [s]: user 0.00 system 0.00 (user 0.0% system 0.0% total 0.0%)
Net I/O: 885.7 KB/s (7.3*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
"""

httperf_results_parsed = {
    'command': 'httperf --client=0/1 --server=localhost --port=80 --uri=/ --send-buffer=4096 --recv-buffer=16384 --num-conns=1 --num-calls=1',
    'max_connect_burst_length': '0', 'total_connections': '1', 'total_requests': '1', 'total_replies': '1',
    'total_test_duration': '0.000', 'connection_rate_per_sec': '2114.1', 'connection_rate_ms_conn': '0.5',
    'connection_time_min': '0.6', 'connection_time_avg': '0.6', 'connection_time_max': '0.6',
    'connection_time_median': '0.5', 'connection_time_stddev': '0.0', 'connection_time_connect': '0.1',
    'connection_length': '1.000', 'request_rate_per_sec': '2114.1', 'request_rate_ms_request': '0.5',
    'request_size': '62.0', 'reply_rate_min': '0.6', 'reply_rate_avg': '0.7', 'reply_rate_max': '0.8',
    'reply_rate_stddev': '0.0', 'reply_rate_samples': '4', 'reply_time_response': '0.4', 'reply_time_transfer': '0.0',
    'reply_size_header': '216.0', 'reply_size_content': '151.0', 'reply_size_footer': '0.0',
    'reply_size_total': '367.0', 'reply_status_1xx': '0', 'reply_status_2xx': '1', 'reply_status_3xx': '0',
    'reply_status_4xx': '0', 'reply_status_5xx': '0', 'cpu_time_user_sec': '0.00', 'cpu_time_system_sec': '0.00',
    'cpu_time_user_pct': '0.0', 'cpu_time_system_pct': '0.0', 'cpu_time_total_pct': '0.0', 'net_io_kb_sec': '885.7',
    'net_io_bps': '7.3*10^6', 'errors_total': '0', 'errors_client_timeout': '0', 'errors_socket_timeout': '0',
    'errors_conn_refused': '0', 'errors_conn_reset': '0', 'errors_fd_unavail': '0', 'errors_addr_unavail': '0',
    'errors_ftab_full': '0', 'errors_other': '0',
    'header_xtrace': [],
    'httperf_colon_lines':
        ['httperf: warning: open file limit > FD_SETSIZE; limiting max. # of open files to FD_SETSIZE']
}

_f = open('./unit/input-data/httperf-output-long.txt')
httperf_headers_results = _f.read()

httperf_headers_parsed = {'command': 'httperf --verbose --print-reply=header --timeout=10 --client=0/1 --server=127.0.0.1 --port=8088 --uri=/ --send-buffer=4096 --recv-buffer=16384 --wsesslog=2,0.000,endpoints/todo-transactions',
'max_connect_burst_length': '1', 'total_connections': '2', 'total_requests': '60', 'total_replies': '60',
'total_test_duration': '0.109', 'connection_rate_per_sec': '18.4', 'connection_rate_ms_conn': '54.3',
'connection_time_min': '48.5', 'connection_time_avg': '54.3', 'connection_time_max': '60.1',
'connection_time_median': '48.5', 'connection_time_stddev': '8.2', 'connection_time_connect': '0.0',
'connection_length': '30.000', 'request_rate_per_sec': '552.8', 'request_rate_ms_request': '1.8',
'request_size': '121.0', 'reply_rate_min': '0.0', 'reply_rate_avg': '0.0', 'reply_rate_max': '0.0',
'reply_rate_stddev': '0.0', 'reply_rate_samples': '0', 'reply_time_response': '1.8', 'reply_time_transfer': '0.0',
'reply_size_header': '287.0', 'reply_size_content': '871.0', 'reply_size_footer': '0.0', 'reply_size_total': '1158.0',
'reply_status_1xx': '0', 'reply_status_2xx': '58', 'reply_status_3xx': '0', 'reply_status_4xx': '0',
'reply_status_5xx': '2', 'cpu_time_user_sec': '0.08', 'cpu_time_system_sec': '0.03', 'cpu_time_user_pct': '71.2',
'cpu_time_system_pct': '28.8', 'cpu_time_total_pct': '100.0', 'net_io_kb_sec': '691.4', 'net_io_bps': '5.7*10^6',
'errors_total': '0', 'errors_client_timeout': '0', 'errors_socket_timeout': '0', 'errors_conn_refused': '0',
'errors_conn_reset': '0', 'errors_fd_unavail': '0', 'errors_addr_unavail': '0', 'errors_ftab_full': '0',
'errors_other': '0',
'header_xtrace': [
    #'2BA1266E6432D0F7263002D5B8E119FBA6196E9CDFBE08A3F70D840D2A01',
    '2B8777FD199A1FBA2DF831FE3F05F0914D0C8264D2ECAEF087878802F601',
    '2B493C558C1AFE67E616F0EEAFD8F91AB1080E4C28526FA16E46533ED101',
    '2B6159DA0D8C68DEA4E9BB8BD0E166EAFFA48609A57A18BB670105EF9E01',
    '2B3B51B77ADD74C4685D0F3D6F51EB52949E1BEBCF95C2F5A1238E4CC201',
    '2B39CDD12765A8CB0BE12704ECAA708B92C96BA9F991F6A646B4DB070F01',
    '2B5C01F5B99AEFC08ECA7AFB5E36C9E302A766B5123A91678852D3D23D01',
    '2B79C073B09B902C137EE2E552453B617127E0DF49FBA20F8C343C02FF01',
    '2BFFB77734FC4AE7D77A85280764008B0EB674070F1BC3C93B5BFBC33C01',
    '2B846607C3BDF4685C6F513DB086C9328D680421EB3A07E1E4F45FCB1601',
    '2B4C7AEF23093A53A72FDC4B6D5E47921122119B4E4B7E2F8929FD258901',
    '2BE84DDA379707FEED7E7EC7A44786A2956DD0A550819D247BA401AFB201',
    '2B1A6642574078B7F95B8F15782D4B53BA6FCB4287DE15A466B0A0D4EA01',
    '2B9C610F48F18386D48EE0B0A3CEFA46419875D051C7B112C6E9E86E4F01',
    '2BDB84413B62AA8CB63F7BD73DF2994DCA7C0D97C2A78442AD0A8634FC01',
    '2B4DFD7CF41FA4AF89F1BC9902C2529727DBB18DED29E89B95B87A1E8B01',
    '2B3153462E322D86D4580869E12B43A9C899627FE1D5915A21CBF09D9201',
    '2B81D0F518809B01BC532294E40C16C0A31B5F7D0E510FBDD7082F304D01',
    '2B6037FAF95042D8857D5D9AEE9FBD110CFB06CB02E0AD9CCC8514CF9C01',
    '2B0DD244830D3EA4CDA293B4E21F165345A34CA0D02CB38A508E574E7201',
    '2B5C067302E89D5678EEA0780B903FDC14C3D6699CA7E457E5915F2E2F01',
    '2B1651AD758D9C6942B0C647964FD218BC1B9E3BDFED4BADC7B92DF0C101',
    '2B83A2EB32B6CBB91F80E92FE192134A605EAE4892165B33C0C91C948A01',
    '2B8AE4149E22B9F8A3A81A9032FB7A45761E88D4DC00805F3D8770C2A901',
    '2BA7B85A0E4EF43A1130C4F9B18FCBD084F48AF20C73FB6EB0A7426AC501',
    '2B7F66A3C5FA8B0D31C5CECF44A5DE9BA0F142A139552FED0D6A5DF1D901',
    '2B0D408BE40115F42452A62889F4E837B94AED1FE78D309D7E483C32FD01',
    '2B36221D1904FBFF73B5305CDC5132C43205EA027BD142AC991A5C661101',
    '2BC919508802C22E26D3B63A0D84F413CF1A1C5ABF6323C03A06ABE98701',
    '2B06C9B3D15C330E3854C6C5D79C31C476995AD8977FA4B887A58C201801',
    '2B592D1D0A0B5577A5ACCD8C6A4B86528AD9073F6245D3D743BEA6978101',
    '2BD58DD2EDCAF6295F2F069B4EAAE5A68C5F912432B5C3031F0370593701',
    '2BAA6A05427C6B5B47D9F80DB35E90249FE5708FCD05D6A722FD043D7601',
    '2B0C40C86C6DA9C1870BA200A9B04BA90BAEAEAA0E1916EAF544FFEA1701',
    '2BF779EA00D9D010E4354886C5C141BB14D37100A3FF5F8F78F18DABE601',
    '2BDD3B69428883040AAAF45BC6E5C31EE2167914AD7D690AD2473858FE01',
    '2B97774B58FACD19A6CB184DD2F5A3C27FF24FC60BD87EBF8713FFE85101',
    '2B0FDE5A232847537392892FC88AD7629F833C2D426FD9CD8B61D86B7701',
    '2B6F3032FF73B6B3432BB456AAF15836039E815E97BE0CDB7EEA71269501',
    '2BDE5ED2A8EC8AE9DD95DED7D4AE6669B29FC30A226E2A73BA87D1EFF201',
    '2B3CD2CC0749CBB0BFB98544A8AED4B20C8C4A7E4494CB7E41F3DCB7A501',
    '2B35FD3811BC20BEC82C4052C03E30B8F1A0E63F6B176986D9E769A43A01',
    '2B8C78D1725FADD0D8FC986D4F757B8FE71FBD96F4ACEBAF87B770E52901',
    '2B3ECD6B60D5F1F83BDAA0C8FC6F2CC4C3B4D11FB4F8D5F729A17F9EB301',
    '2B0500D61B95F6049942B4D333BE45DD803AE0ACAF96B0CCBAA4760D9F01',
    '2BB06F3EF64562EF782D6CFCA203670BCB21912C9784F7336BB71FFA5501',
    '2B45BC80AF335184A139CC5680A563B40A0F1570D5617A5F95F4D383DE01',
    '2B78DDEC421F455CD7F6CA3B38E27647139023D32AE6810E109922889601',
    '2B600343B674E6AC3B98386F4EB6530B925BB9508D711A65B9027B9CC501',
    '2B20AF38E3C9A09B0AC64E11C7D3CDB392BFF6E89CA3A70F69E480739B01',
    '2B752B1CC2BABDAFC05D2B676732402E2CD0CC261D4D22E0E02C58EAAB01',
    '2B6E690AA0D52438EF29D5D930176F2EA3A3304B66CD6B1CD7CA35A9D001',
    '2BC4FA32873A1D40BD032FE5F6A465C605CB049D9E3597AE696034E96A01',
    '2BBB8834A170A855113D1620F33E01AC551A3631F70D1D27C470B0693001',
    '2B9E0493B0A1FC1404CB1424F2C88079F9A89AFCA6366E5C76407F4EF101',
    '2BC177A58EBB98E0111E1C4B795085F6F58C1FAEEE7F1C351F925D133A01',
    '2B6F3B65C0C07EF6B463BC364FF5E08BFA09FFFA2F5EB969A862C230C601',
    '2B4955E611459325111AE2572DAED8C9C51A1A0B4E19E600502877786701',
    '2BECA2829F0F2AF2B447B850D9EB7FB67A89829AE642627683BDCE6E1A01',
    '2BFBCCFC6957E8902F74982ACE49610C005EFBE5CD227DB0C23088C97C01'
],
'unknown_lines': [
    'Session rate [sess/s]: min 0.00 avg 18.43 max 0.00 stddev 0.00 (2/2)',
    'Session: avg 1.00 connections/session',
    'Session lifetime [s]: 0.1',
    'Session failtime [s]: 0.0',
    'Session length histogram: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2'
],
'httperf_colon_lines': ['httperf: maximum number of open descriptors = 1048576']
}

httperf_verbose_results = """
httperf --verbose --client=0/1 --server=localhost --port=80 --uri=/ --send-buffer=4096 --recv-buffer=16384 --num-conns=10 --num-calls=1
httperf: warning: open file limit > FD_SETSIZE; limiting max. # of open files to FD_SETSIZE
httperf: maximum number of open descriptors = 1024
Connection lifetime = 0.56
Connection lifetime = 0.35
Connection lifetime = 0.34
Connection lifetime = 0.33
Connection lifetime = 0.75
Connection lifetime = 0.42
Connection lifetime = 0.31
Connection lifetime = 0.31
Connection lifetime = 0.30
Connection lifetime = 0.29
Maximum connect burst length: 1

Total: connections 10 requests 10 replies 10 test-duration 0.005 s

Connection rate: 2150.6 conn/s (0.5 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 0.3 avg 0.4 max 0.7 median 0.5 stddev 0.1
Connection time [ms]: connect 0.1
Connection length [replies/conn]: 1.000

Request rate: 2150.6 req/s (0.5 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 0.0 avg 0.0 max 0.0 stddev 0.0 (0 samples)
Reply time [ms]: response 0.3 transfer 0.0
Reply size [B]: header 216.0 content 151.0 footer 0.0 (total 367.0)
Reply status: 1xx=0 2xx=10 3xx=0 4xx=0 5xx=0

CPU time [s]: user 0.00 system 0.00 (user 0.0% system 86.0% total 86.0%)
Net I/O: 901.0 KB/s (7.4*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
"""
