import portable_popen
import textops


try:
  netstat_process = portable_popen.Popen(["netstat", "-an"])
  netstat_stdout, _ = netstat_process.communicate()
  netstat_lines = textops.textops_rawtexttolines(netstat_stdout)
except Exception, e:
    raise Exception('Netstat failed internally ' + str(e))  
