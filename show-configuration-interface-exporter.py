import csv # To write exported configuration to CSV

global output_file_location, output_file_name, subnet_masks, headers, data, interfaces, ip_addresses, mask_lengths, subnet_mask_list # Define Gloabl Variables

# Define dictionary & lists the script will use
#Definining subnet masks to map a mask length to a full legnth subnet mask
subnet_masks = ['0.0.0.0','128.0.0.0','192.0.0.0','224.0.0.0','240.0.0.0','248.0.0.0','252.0.0.0','254.0.0.0','255.0.0.0','255.128.0.0','255.192.0.0','255.224.0.0','255.240.0.0','255.248.0.0','255.252.0.0','255.254.0.0','255.255.0.0','255.255.128.0','255.255.192.0','255.255.224.0','255.255.240.0','255.255.248.0','255.255.252.0','255.255.254.0','255.255.255.0','255.255.255.128','255.255.255.192','255.255.255.224','255.255.255.240','255.255.255.248','255.255.255.252','255.255.255.254','255.255.255.255']
headers = ['Interface Name','IP Address','Subnet Mask','Mask Length'] # CSV Headers
data = [] # Data to write to the CSV file
interfaces = [] # Interfaces detected from show configuration file
ip_addresses = {} # IP addresses detected from show configuration file
mask_lengths = [] # Interface mask lengths detected from show configuration file
subnet_mask_list = [] # Subnet masks detected from show configuration file

# Search for interfaces and add them to the interfaces list, also calls on the ip_address_mask_search function and the write_to_csv function
def interface_search(file_path): 
    x = 0 # Define x for use in writing an IP address to the ip_addresses dictionary
    with open(file_path) as file: # Opens interface txt file
        for line in file: # Searches every line in the file
            if line.startswith('set interface '): # Checks the line starts with 'set interface'
                keyword = 'interface'
                before_keyword, keyword, after_keyword = line.partition(keyword) # This specifies all the contents of the line before, after and the word 'interface' itself.
                interface = str(after_keyword.split(' ')[1]) # Splits the line after 'interface' at whitespace, then selects value [1] for the value of interface (this is because the interface name will follow the word interface)
                if interface not in interfaces: # Check interface wasn't already added to interface list
                    interfaces.append(interface) # Add interface to interface list
                    ip_addresses[x] = ('N/A') # Insert 'N/A' to value x in ip_address dictionary (this gets overwritten later)
                    mask_lengths.append('N/A') # Insert 'N/A'  to subnet mask list (gets overwritten later)
                    subnet_mask_list.append('N/A') # Insert 'N/A'  to subnet mask list (gets overwritten later)
                    x += 1
    with open(file_path) as file: # Opens interface txt file
        for line in file: # Searches every line in the file
            ip_address_mask_search(line) # Run function to search for IP addresses within the file
    ip_addresses_list = ip_addresses.values() # Once IP address search has run, convert dictionary into list for use in CSV file
    information = [interfaces,ip_addresses_list,mask_lengths,subnet_mask_list] # Add all data columns to information list
    information = zip(*information) # Zip information list to write to CSV
    write_to_csv(information) # Call write_to_csv function
                
            

def ip_address_mask_search(line):
    if line.startswith ('set interface ') and 'ipv4-address' in line: # Check set interface <interface> ipv4-address is present in line
        keyword = 'interface' # Split line to ensure an exact match (for example, without this when the code executres the following for loop, bond1 would match if bond1.1 was in the line)
        before_keyword, keyword, after_keyword = line.partition(keyword)
        interface = str(after_keyword.split(' ')[1])
        for item in interfaces: # Iterate through interfaces to find which interface is in the line
            if item == interface: # Check chosen interface exactly matches the interface in the line
                x = interfaces.index(item) # Get the location of the interface in the interface list (so that the ipv4-address for the interface will be in the same index in the ipv4-address dictionary)
                before_ip_keyword, ip_keyword, after_ip_keyword = line.partition('ipv4-address') # Split line to get the IP address
                ip_address = str(after_ip_keyword[:17].split(' ')[1])

                before_mask_keyword, mask_keyword, after_mask_keyword = line.partition('mask-length') # Split line to get the subnet mask
                subnet_mask = int(after_mask_keyword[:3].split(' ')[1])
                mask_lengths.insert(x , subnet_mask) # Add subnet mask to subnet mask CIDR notation list
                subnet_mask_list.insert(x, subnet_masks[subnet_mask]) # Convert above CIDR notation to full length subnet mask
                ip_addresses[x] = ip_address # Insert returned IP address to the same location in the ip_addresses dictionary
        
def write_to_csv(information): # Function to write information list to a CSV file
    data.append(information)
    with open(output_file_location, 'w', newline='') as csvfile: # Open CSV file in path specified by user input
        csvwriter = csv.writer(csvfile, delimiter=',') # Create a csvwriter object
        csvwriter.writerow(headers) # Write the header
        csvwriter.writerows(information) # Write the rest of the data
        
input_file_location = input('Input file with full file path: ') # Get user input for input location
output_file_location = input('Desired file output file path (including file name, with .csv extension): ') # Get user input for desired output file name and path
if output_file_location[-4:] != '.csv': # Check user has given a .csv file for file output name and path
    print('Please correct output file name to include .csv extension')
    exit() # Exit code if .csv extension is not added
interface_search(input_file_location) # Run interface search function