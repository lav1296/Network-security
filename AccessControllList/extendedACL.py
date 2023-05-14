class ACL:
    def __init__(self,access_list_number,permit,source_ip,source_ip_mask,destination_ip,destination_ip_mask):
        self.access_list_number=access_list_number
        self.permit=permit
        self.source_ip=source_ip
        self.source_ip_mask=source_ip_mask
        self.destination_ip=destination_ip
        self.destination_ip_mask=destination_ip_mask
        self.all_ports_access=True
        self.ports=[]
        

class Interface:
    def __init__(self,interface_number,interface_in):
        self.interface_number=interface_number
        self.interface_in=interface_in
        self.acls=[]
class Packet:
    def __init__(self,source,destination,port):
        self.source_ip=source
        self.destination_ip=destination
        self.port=port

def process_extended_access_list_file(access_lists):
    i=0
    lines=access_lists.readlines()
    acls=[]
    interfaces=[]
    for line in lines :
        commands=line.split(" ") 
        if commands[0]=="access-list":
            acl_number=int(commands[1])
            acl_permit=commands[2]=="permit"
            acl_source_ip=commands[4]
            acl_source_ip_mask=commands[5]
            acl_destination_ip=commands[6]
            acl_destination_ip_mask=commands[7]
            ports=[]
            allPorts=True
            if len(commands)>8:
                if commands[8]=="range":
                    acl_port_range=commands[9].split("-")
                    allPorts=False
                    for j in range (int(acl_port_range[0]),int(acl_port_range[1])+1):
                        ports.append(j)
            acl=ACL(acl_number,acl_permit,acl_source_ip,acl_source_ip_mask,acl_destination_ip,acl_destination_ip_mask)
            acl.all_ports_access=allPorts
            acl.ports=ports
            acls.append(acl)
        elif commands[0]=="interface":
            interface_name=commands[1]
            line=lines[i+1]
            i=i+1
            commands=line.split(" ") 
            interface_in=commands[3]=="in"
            interface_acl_number=int(commands[2])
            interface=Interface(interface_name,interface_in)

            for acl in acls:
                if acl.access_list_number==interface_acl_number:
                    interface.acls.append(acl)
            interfaces.append(interface)
            break
        i=i+1
    return interfaces

def read_packet(packets):
    packetList=[]
    lines=packets.readlines()
    for line in lines:
        packet_details=line.split(" ")
        packet_source_ip=packet_details[0]
        packet_destination_ip=packet_details[1]
        packet_port=packet_details[2]
        packet=Packet(packet_source_ip,packet_destination_ip,packet_port)
        packetList.append(packet)
    
    return packetList

def is_packet_permitted(interface,packet):
    acls=interface.acls
    for acl in acls:
        source_ip_match=ip_match(packet.source_ip,acl_ip=acl.source_ip,acl_mask=acl.source_ip_mask)
        destination_ip_match=ip_match(packet.destination_ip,acl_ip=acl.destination_ip,acl_mask=acl.destination_ip_mask)
        port_match=is_port_match(packet.port,acl.all_ports_access,acl.ports)
        if source_ip_match and destination_ip_match and port_match:
            return acl.permit
    return False

def ip_match(packetIp,acl_ip,acl_mask):
    packet_ip_groups=packetIp.split(".")
    acl_ip_groups=acl_ip.split(".")
    acl_mask_groups=acl_mask.split(".")
    index=0
    for ipGroup in acl_mask_groups:
        ipGroup=int(ipGroup)
        if ipGroup==0 and packet_ip_groups[index]!=acl_ip_groups[index]:
            return False
        index=index+1
    return True

def is_port_match(packet_port,all_ports,aclPorts):
    if all_ports:
        return True
    else:
        for port in aclPorts:
            if(int(packet_port)==port):
                return True
        return False

def main():
    acl_file_reader= open('extendedacl.txt', 'r') 
    interface=process_extended_access_list_file(acl_file_reader)
    packet_file_reader= open('extendedpacket.txt', 'r')
    packets=read_packet(packet_file_reader)
    for packet in packets:
        if is_packet_permitted(interface[0],packet):
            print("packet from "+str(packet.source_ip)+" on port "+str(packet.port).strip()+" permitted")
        else:
            print("packet from "+str(packet.source_ip)+" on port "+str(packet.port).strip()+" denied")

if __name__ == "__main__":
    main()
            


