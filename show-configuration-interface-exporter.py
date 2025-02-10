import re
import csv

global data
global headers
global output_file_location


subnet_masks = ['0.0.0.0','128.0.0.0','192.0.0.0','224.0.0.0','240.0.0.0','248.0.0.0','252.0.0.0','254.0.0.0','255.0.0.0','255.128.0.0','255.192.0.0','255.224.0.0','255.240.0.0','255.248.0.0','255.252.0.0','255.254.0.0','255.255.0.0','255.255.128.0','255.255.192.0','255.255.224.0','255.255.240.0','255.255.248.0','255.255.252.0','255.255.254.0','255.255.255.0','255.255.255.128','255.255.255.192','255.255.255.224','255.255.255.240','255.255.255.248','255.255.255.252','255.255.255.254','255.255.255.255']
headers = ['Interface Name','IP Address','Subnet Mask','Mask Length']
data = []

def interface_search(file_path):
    x = 0
    interfaces = []
    ip_addresses = []
    mask_lengths = []
    subnet_mask_list = []
    with open(file_path) as file: #Opens interface txt file
        for line in file: #Searches every line in the file
            if line.startswith('set interface '): #This line will catch any bonds that aren't consecutive with other bonds. E.g: bond5 & bond8.
                keyword = 'interface'
                before_keyword, keyword, after_keyword = line.partition(keyword) #This specifies all the contents of the line before the word bond, the word bond, and after the word bond.
                interface = after_keyword.split(' ')#Updates bondnumber to match the current bond, so VLANs can be checked.
                interface = str(interface[1])
                ip_address_mask_search(line,interface,interfaces,subnet_masks,ip_addresses,mask_lengths,subnet_mask_list,x)
        print(interfaces)
        information = [interfaces,ip_addresses,mask_lengths,subnet_mask_list]
        information = zip(*information)
        write_to_csv(information)
                
            

def ip_address_mask_search(line,interface,interfaces,subnet_masks,ip_addresses,mask_lengths,subnet_mask_list,x):
    if interface not in interfaces and ' ipv4-address' in line:
        before_ip_keyword, ip_keyword, after_ip_keyword = line.partition('ipv4-address')
        ip_address = str(after_ip_keyword[:17].split(' ')[1])
        ip_addresses.append(ip_address)

        before_mask_keyword, mask_keyword, after_mask_keyword = line.partition('mask-length')
        subnet_mask = int(after_mask_keyword[:3].split(' ')[1])
        mask_lengths.append(subnet_mask)
        subnet_mask_list.append(subnet_masks[subnet_mask])
        subnet_mask = subnet_mask.strip()
        #print(subnet_mask)
        #write_to_csv(interfaces[x],ip_addresses[x],mask_lengths[x],subnet_mask_list[x])

    elif interface not in interfaces:
        ip_addresses.append('N/A')
        mask_lengths.append('N/A')
        subnet_mask_list.append('N/A')
        interfaces.append(interface)
        x = interfaces.index(interface)
        #write_to_csv(interfaces[x],ip_addresses[x],mask_lengths[x],subnet_mask_list[x])
    
    elif interface in interfaces and ' ipv4-address' in line:
        before_ip_keyword, ip_keyword, after_ip_keyword = line.partition('ipv4-address')
        ip_address = str(after_ip_keyword[:17].split(' ')[1])
        ip_addresses.insert(x, ip_address)

        before_mask_keyword, mask_keyword, after_mask_keyword = line.partition('mask-length')
        subnet_mask = int(after_mask_keyword[:3].split(' ')[1])
        mask_lengths.insert(x , subnet_mask)
        subnet_mask_list.insert(x, subnet_masks[subnet_mask])
        #write_to_csv(interfaces[x],ip_addresses[x],mask_lengths[x],subnet_mask_list[x])

    
    return(interfaces,ip_addresses,mask_lengths,subnet_mask_list)
        
def write_to_csv(information): #interface,ip_address,mask_length,subnet_mask
    #information = [interface,ip_address,subnet_mask,mask_length]
    data.append(information)
    filename = (output_file_location+'ifconfig.csv')
    with open(filename, 'w', newline='') as file:
        csvwriter = csv.writer(file) # create a csvwriter object
        csvwriter.writerow(headers) # write the header
        for item in data:
            csvwriter.writerow([item]) # write the rest of the data
        
#input_file_location = input('Input file with full file path: ')
#output_file_location = input('Desired file output file path (will be named ifconfig.csv): ')
output_file_location = ''
interface_search('showconfiguration.txt')