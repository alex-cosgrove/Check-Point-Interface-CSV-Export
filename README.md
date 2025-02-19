![GitHub Repo stars](https://img.shields.io/github/stars/alex-cosgrove/Check-Point-Interface-CSV-Export)
# Check-Point-Interface-CSV-Export
A  script to search a Check Point firewall 'show configuration' output for interface configuration, and output interfaces, IP addresses, and subnet masks to a CSV file. This was made to reduce the time spent manually correlating configuration into a useable format. This was an interesting project as I had to ensure the script would be able to process all interface types and map the interface to an IP address when there are an unknown number of interfaces, not all interfaces have IP addresses, and the ordering of interfaces in configuration is not wholly consistent. This means keeping track of data with an unknown position, so it was an interesting challenge to get around.

## Usage
The only library used for this project is csv, no other packages are required to run the script.

Connect to a Check Point firewall or management server, and run 'show configuration' from the clish shell. Either copy this output to a .txt file, export it to a txt file and transfer it from the device, or export the show configuration to a txt file and run this script on the device.

Once the show configuration is exported, the python script can be run. The scripts will prompt for an input file path (the location and filename of the show configuration output), and an output file path (the file path and name of the CSV file). **Note**: The output file patch and file name must end in .csv, or the script will fail.

Once the input & output files have been collected, the script will iterate through the interfaces (including Bonds, VLANs, Aliases), then it will map IP addresses & subnet masks to those interfaces. Once complete, the script will print the CSV file location and exit.

## Test Usage
### Test with existing show configuration file
Use the included show_configuration_test.txt file to follow along with the example.
1. Download Check-Point-Interface-CSV-Export.py and show_configuration_test.txt
2. Ensure python is installed
3. Choose a method below based on if accessing python via the command line or file explorer:
    - If using python in command line:
        - Use the 'cd' command to navigate to the directory with the 2 files in.
        - Run "python3 Check-Point-Interface-CSV-Export.py'
    - If using opening python using file explorer:
        - Double click the python file to run it
4. For input file location, enter /path/to/current/directory/show_configuration_test.txt
5. For output file location, enter /path/to/current/directory/CSV-export-test.csv
6. The script will output the CSV location once complete. Open the CSV and compare it to the one in the repo.


### Example on how to run on a Check Point appliance
This example assumes the script is being run from /home/<user>, however it can be run from most directories.
1. Connect to the device using SSH
2. If not already, log into expert mode using the command 'expert'
3. Copy contents of Check-Point-Interface-CSV-Export.py to a file with the same name using the command 'vi Check-Point-Interface-CSV-Export.py', or copy file over using an SCP client.
4. Run 'clish -c "show configuration" | cat > /home/<user> show_configuration.txt'
5. Run 'python3 Check-Point-Interface-CSV-Export.py'
6. Input /home/<user>/show_configuration.txt for input file, and /home/<user>/output.csv for output file.
7. The script will output 'Interfaces exported to /home/<user>/output.csv'
8. Review output.csv