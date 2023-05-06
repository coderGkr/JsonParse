'''This program accepts a json file as input and prints out the IP addresses, which are the values of
all the keys inside the "value" object one per line. If the file also contains
a "network" object, then you should also print out a second IP address on the same line
that corresponds to the same "name".'''

import sys
import re
import json


# check if IP addrress is valid
def validateIp(ip):
    if not isinstance(ip, str):
        return False
    match = re.findall(r"^(?:\d{1,3}\.){3}\d{1,3}$", ip)
    if not match:
        return False
    for i in match[0].split("."):
        if int(i) > 255:
            return False
    return True


def main(jsonfile):
    contents = {}
    final_dict = {}
    try:
        with open(jsonfile, 'r') as ifil:
            contents = json.load(ifil)
    except FileNotFoundError:
        raise FileNotFoundError("Unable to find the file")
    except json.JSONDecodeError:
        raise ValueError("Unable to decode json file")

    assert isinstance(contents, dict), "json should be of dictionary type"
    assert contents != {}, "Parsed json file is empty"

    ip_dict = {}
    value_dict = {}

    assert "vm_private_ips" in contents, "Missing required key: vm_private_ips for attributes in JSON"
    # assuming vm_private_ips is mandatory
    ip_dict = contents['vm_private_ips']

    assert "value" in ip_dict, "value not present for vm_privage_ips in JSON"
    value_dict = ip_dict['value']

    for name, ip in value_dict.items():
        assert validateIp(ip), f"Invalid IP address detected in the JSON file"

    # network is not mandatory
    if "network" in contents:
        assert "vms" in contents['network'], "vms key not present for network key in JSON"
        vm_list = contents['network']['vms']
        for vm in vm_list:
            assert "id" in vm, "Missing required key: id for VM in JSON"
            assert "attributes" in vm, "Attributes not present for VM key under network in JSON"
            assert "name" in vm["attributes"], "Missing required key: name for attributes in JSON"
            assert "access_ip_v4" in vm["attributes"], "Missing required key: access_ip_v4 for attributes in JSOn"
            assert "availability_zone" in vm[
                "attributes"], "Missing required key: availability_zone for attributes in JSON"

            attribute_dict = vm["attributes"]
            ip = attribute_dict['access_ip_v4']
            assert validateIp(ip), f"Invalid IP address {ip} detected in the JSON file"
            name = attribute_dict['name']
            assert name in value_dict.keys(), f"{name} not present in vm_private_ips sections"
            final_dict[name] = [value_dict[name], ip]


    else:
        final_dict = {key: [value] for key, value in value_dict.items()}

    for key, value in final_dict.items():
        print(" ".join(value))
    return 0


if __name__ == '__main__':
    # have a logic to see if the input file is json itself here itself assert
    main(sys.argv[1])
