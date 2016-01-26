import portable_popen
import textops


try:
  # Grab netstat output.
  netstat_process = portable_popen.Popen(["ss", "-a"])
  netstat_stdout, _ = netstat_process.communicate()
  netstat_lines = textops.textops_rawtexttolines(netstat_stdout)
except Exception, e:
    raise Exception('SS failed internally ' + str(e)) 

