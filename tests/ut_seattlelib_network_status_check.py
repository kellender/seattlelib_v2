import portable_popen
import textops




def exists_outgoing_network_socket(localip, localport, remoteip, remoteport):

  """
  <Purpose>
    Determines if there exists a network socket with the specified unique tuple.
    Assumes TCP.

  <Arguments>
    localip: The IP address of the local socket
    localport: The port of the local socket
    remoteip:  The IP of the remote host
    remoteport: The port of the remote host
    
  <Returns>
    A Tuple, indicating the existence and state of the socket. E.g. (Exists (True/False), State (String or None))

  """
  # This only works if all are not of the None type
  if not (localip and localport and remoteip and remoteport):
    return (False, None)

  #set to none to check if process will run
  network_status_process = None
  socket_state = None

  if(network_status_process == None):
    try:
      # Grab netstat output.
      network_status_process = portable_popen.Popen(["netstat", "-an"])
      netstat_stdout, _ = network_status_process.communicate()
      netstat_lines = textops.textops_rawtexttolines(netstat_stdout)

      # Search for things matching the local and remote ip+port we are trying to get
      # information about.
      target_lines = textops.textops_grep(localip + ':' + str(localport), netstat_lines) + \
        textops.textops_grep(localip + '.' + str(localport), netstat_lines)

      target_lines = textops.textops_grep(remoteip + ':' + str(remoteport), target_lines) + \
        textops.textops_grep(remoteip + '.' + str(remoteport), target_lines)

      if len(target_lines) > 0:
        line = target_lines[0]

        # Replace tabs with spaces, explode on spaces
        parts = line.replace("\t","").strip("\n").split()


        # Get the state
        socket_state = parts[-1]
        return (True, socket_state)

    except Exception, e:
      pass

  if(network_status_process == None):
    try:
      # Grab SS output.
      network_status_process = portable_popen.Popen(["ss", "-a"])
      netstat_stdout, _ = network_status_process.communicate()
      netstat_lines = textops.textops_rawtexttolines(netstat_stdout)

      # Search for things matching the local and remote ip+port we are trying to get
      # information about.
      if(localip == "0.0.0.0"):
        ip = "*"
      target_lines = textops.textops_grep(localip + ':' + str(localport), netstat_lines) + \
        textops.textops_grep(localip + '.' + str(localport), netstat_lines)

      target_lines = textops.textops_grep(remoteip + ':' + str(remoteport), target_lines) + \
        textops.textops_grep(remoteip + '.' + str(remoteport), target_lines)

      if len(target_lines) > 0:
        line = target_lines[0]

        # Replace tabs with spaces, explode on spaces
        parts = line.replace("\t","").strip("\n").split()

        # Get the state
        socket_state = parts[1]
        return (True, socket_state)



    except Exception, e:
      raise Exception('Both Netstat and SS and failed internally ' + str(e)) 

  return (False, None)


localip = "*" # local host on ss and netsta
localport = 12345
remoteip = "*"
remoteport = "*"
print (exists_outgoing_network_socket(localip, localport, remoteip, remoteport))