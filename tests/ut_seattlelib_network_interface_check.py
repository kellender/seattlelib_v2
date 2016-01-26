import portable_popen
import textops


def get_available_interfaces():
  """
  <Purpose>
    Returns a list of available network interfaces.
  
  <Returns>
    An array of string interfaces
  """
  # Common headers
  # This list contains common header elements so that they can be stripped
  common_headers_list = ["Name", "Kernel", "Iface"]
  
  # Netstat will return all interfaces, but also has some duplication.
  # Cut will get the first field from each line, which is the interface name.
  # Sort prepares the input for uniq, which only works on sorted lists.
  # Uniq, is somewhat obvious, it will only return the unique interfaces to remove duplicates.
  # Launch up a shell, get the feedback

  network_status_process = None

  if(network_status_process == None):
    try:
      netstat_process = portable_popen.Popen(["netstat", "-i"])
      netstat_stdout, _ = netstat_process.communicate()
      netstat_lines = textops.textops_rawtexttolines(netstat_stdout)

      target_lines = textops.textops_cut(netstat_lines, delimiter=" ", fields=[0])

      unique_lines = set(target_lines)

      # Create an array for the interfaces
      interfaces_list = []
  
      for line in unique_lines:
        # Strip the newline
        line = line.strip("\n")
        # Check if this is a header
        if line in common_headers_list:
          continue
        interfaces_list.append(line)
  
      # Done, return the interfaces
      return interfaces_list
    except Exception, e:
      pass

  if(network_status_process == None):
    try:
      netstat_process = portable_popen.Popen(["ip", "addr"])
      netstat_stdout, _ = netstat_process.communicate()
      netstat_lines = textops.textops_rawtexttolines(netstat_stdout)

      target_lines = textops.textops_cut(netstat_lines, delimiter=" ", fields=[1])

      unique_lines = set(target_lines)

      # Create an array for the interfaces
      interfaces_list = []
  
      for line in unique_lines:
        # Strip the newline
        line = line.strip("\n")
        # Check if this is a header
        if line in common_headers_list:
          continue
        if line == '': #for the tab charecters that ss has
          continue
        interfaces_list.append(line[0:-1])
 
      # Done, return the interfaces
      return interfaces_list
    except Exception, e:
      raise Exception('Both Netstat and SS and failed internally ' + str(e)) 

print(get_available_interfaces())