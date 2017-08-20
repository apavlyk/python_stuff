#! /usr/bin/python

"""
# Class to read, update host file on Win, Mac, Linux OS
"""

import sys
import os
import os.path

# Global OS constants
IS_NT = (os.name == 'nt')
IS_POSIX = (os.name == 'posix')
IS_MAC = (sys.version.find("Apple") != -1)
IS_OSX = (IS_MAC and IS_POSIX)
IS_LINUX = (sys.platform.find('linux') != -1)

# Import that requires third party packages
try:
    if IS_NT:
        import win32api
except ImportError:
    print("Fulfillment canceled. Win32api package has not been installed")
    input("Press <ENTER> to close")
    sys.exit(1)

#TODO: add ability to take parameters from command line


class HostsFile(object):
    HOST_FILE = 'hosts'
    WIN_HOST_PATH = 'drivers\\etc'
    NIX_HOST_PATH = 'etc'

    # ENV_VAR = "windir"
    # WIN_HOST_PATH = 'System32\\drivers\\etc'

    def raise_exception_from_io_error(funct):
        def decorator(self, *args, **kwargs):
            try:
                return funct(self, *args, **kwargs)
            except IOError as excn:
                if funct.__name__ == "add_data":
                    error_text = "An '{}' error occurs during write to " \
                                 "file: {}.".format(excn.strerror, self.file_path)
                elif funct.__name__ == "get_content":
                    error_text = "An '{}' error occurs during read from "\
                                 "file: {}.".format(excn.strerror, self.file_path)
                if excn.errno == 13:
                    if IS_NT:
                        print("{} Run script as Administrator".format(error_text))
                    else:
                        print("{} Use 'sudo' command to run script".format(error_text))
                else:
                    print("{}".format(error_text))
                sys.exit(1)


        return decorator

    def __init__(self):
        self.file_path = self.__get_path()

    def __get_path(self):
        if IS_NT:
            sys_path = win32api.GetSystemDirectory()
            host_file_path = os.path.join(os.path.join(sys_path,
                                                       self.WIN_HOST_PATH),
                                                       self.HOST_FILE)
#            host_file_path = os.path.join(os.getenv(self.ENV_VAR), self.WIN_HOST_PATH)
        else:
            host_file_path = os.path.join(self.NIX_HOST_PATH, self.HOST_FILE)

        return host_file_path

    def __remove_already_existing_records_from_input_data(self, initial_data,
                                                          data_to_add):
        """
        # Method to compare initial hosts file content and data which are going
        # to be added to hosts file
        # Method returns dictionary with ip address, host name pairs which have
        # not existed in hosts file yet.
        """
        coinciding_data = {}
        actual_input_data = {}
        if not initial_data:
            actual_input_data = data_to_add
        else:
            for ip_address, host_name in data_to_add.items():
                if ip_address in initial_data:
                    if initial_data[ip_address] == host_name:
                        coinciding_data[ip_address] = host_name
            if coinciding_data:
                for ip_address, host_name in data_to_add.items():
                    if ip_address not in coinciding_data:
                        actual_input_data[ip_address] = host_name
            else:
                actual_input_data = data_to_add

        return actual_input_data

    @raise_exception_from_io_error
    def get_content(self):
        """
        # Method returns dictionary where keys are ip addresses, values are appropriate host names
        # NOTE: commented items are not included to the dictionary
        """
        with open(self.file_path) as fd:
            ip_addresses_hosts = {}
            actual_lines = []
            file_content = fd.readlines()

            if len(file_content) > 0:
                for line in file_content:
                    if not line.startswith("#"):
                        actual_lines.append(line.replace("\n", ""))
                # Convert each host line file in dictionary
                for item in actual_lines:
                    if item != '':
                        ip_address = item.split()[0]
                        host_name = item.split()[1].strip()
                        ip_addresses_hosts[ip_address] = host_name

        return ip_addresses_hosts

    @raise_exception_from_io_error
    def add_data(self, input_ip_data_dict):
        """
        # Method to update hosts file with new records
        # input_ip_data_dict parameter is dictionary where keys are ip_addresses
        # and values are corresponding host names
        """
        success = False
        if len(input_ip_data_dict) > 0:
            initial_hosts_data = self.get_content()
            actual_data_to_add = self.__remove_already_existing_records_from_input_data(initial_hosts_data,
                                                                                        input_ip_data_dict)
            if actual_data_to_add:
                with open(self.file_path, mode="a") as fd:
                        for ip_address, host_name in actual_data_to_add.items():
                            host_record_to_add = "\n{} {}".format(ip_address.strip(),
                                                                  host_name.strip())
                            print("'{}' record will be added to hosts file".format(host_record_to_add))
                            fd.write(host_record_to_add)

                if not self.__remove_already_existing_records_from_input_data(self.get_content(),
                                                                            input_ip_data_dict):
                    success = True
            else:
                print("All input data: '{}' is already in host file".format(input_ip_data_dict))
                success = True
        else:
            print("Input data is empty. Please, check the input parameters.")
            sys.exit(1)

        return success

if __name__ == "__main__":
    ip_address = input("Please, insert ip address: ")
    host = input("Please, insert host: ")
    dict = {ip_address: host}

    host_file = HostsFile()
    if host_file.add_data(dict):
        print("Added successfully!")
        sys.exit(0)
    else:
        print("FAIL! Check file/code.")
        sys.exit(1)
