import portable_popen
import textops






def exists_listening_network_socket(ip, port, tcp):
  """
  <Purpose>
    Determines if there exists a network socket with the specified ip and port which is the LISTEN state.
  
  <Arguments>
    ip: The IP address of the listening socket
    port: The port of the listening socket
    tcp: Is the socket of TCP type, else UDP
    
  <Returns>
    True or False.
  """
  # This only works if both are not of the None type
  if not (ip and port):
    print "executed\n"
    print ip
    print "\n"
    print port
    print "\n"
    return False
  
  # UDP connections are stateless, so for TCP check for the LISTEN state
  # and for UDP, just check that there exists a UDP port
  if tcp:
    grep_terms = ["tcp", "LISTEN"]
  else:
    grep_terms = ["udp"]

  #set to none to check if process will run
  network_status_process = None

  if(network_status_process == None):
    try:

      # Launch up a shell, get the feedback
      netstat_process = portable_popen.Popen(["netstat", "-an"])
      netstat_stdout, _ = netstat_process.communicate()
      netstat_lines = textops.textops_rawtexttolines(netstat_stdout)
      # Search for things matching the ip+port we are trying to get
      # information about.
      target_lines = textops.textops_grep(ip + ':' + str(port), netstat_lines) + \
          textops.textops_grep(ip + '.' + str(port), netstat_lines)

      for term in grep_terms:
        target_lines = textops.textops_grep(term, target_lines)

      number_of_sockets = len(target_lines)
      return (number_of_sockets > 0)
    except Exception, e:
      pass
  

  if(network_status_process == None):
    try:

      # Launch up a shell, get the feedback
      netstat_process = portable_popen.Popen(["ss", "-a"])
      netstat_stdout, _ = netstat_process.communicate()
      netstat_lines = textops.textops_rawtexttolines(netstat_stdout)
      # Search for things matching the ip+port we are trying to get
      # information about.
      if(ip == "0.0.0.0"):
      	ip = "*"
      target_lines = textops.textops_grep(ip + ':' + str(port), netstat_lines) + \
          textops.textops_grep(ip + '.' + str(port), netstat_lines)

      for term in grep_terms:
        target_lines = textops.textops_grep(term, target_lines)

      number_of_sockets = len(target_lines)
      return (number_of_sockets > 0)
    except Exception, e:
      raise Exception('Both Netstat and SS and failed internally ' + str(e)) 

# tested with nc -l 12345
ip = '*' # localhost on ss and netstat if -n is not used else netstat will be 0.0.0.0
port = 12345
print (exists_listening_network_socket(ip, port, (1)))