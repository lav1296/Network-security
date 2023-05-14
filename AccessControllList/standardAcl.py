class ACL:
    def __init__(self,access_list_number,permit,source_ip,mask):
        self.access_list_number=access_list_number
        self.permit=permit
        self.source_ip=source_ip
        self.mask=mask
        

class Interface:
    def __init__(self,interface_number,interface_in):
        self.interface_number=interface_number
        self.interface_in=interface_in
        self.acls=[]

def process_access_list_file(access_lists):
    i=0
    lines=access_lists.readlines()
    acls=[]
    interfaces=[]
    for line in lines :
        commands=line.split(" ") 
        if commands[0]=="access-list":
            acl_number=int(commands[1])
            acl_permit=commands[2]=="permit"
            acl_source_ip=commands[3]
            acl_mask=commands[4]
            acl=ACL(acl_number,acl_permit,acl_source_ip,acl_mask)
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
            break;
        i=i+1
    return interfaces

def read_packet(packets):
    packetList=[]
    line=str(packets.readline())
    while line:
        packetList.append(line)
    return packetList

def is_packet_permitted(interface,ip):
    acls=interface.acls
    
    for acl in acls:
        match=True
        acl_ip=acl.source_ip
        acl_mask_group=acl.mask.split(".")
        packet_ip_groups=ip.split(".")
        acl_ip_groups=acl_ip.split(".")
        index=0
        for ipGroup in acl_mask_group:
            ipGroup=int(ipGroup)
            if ipGroup==0 and packet_ip_groups[index]!=acl_ip_groups[index]:
                match=False
                break
            index=index+1
        if match:
            return acl.permit
    return False

def main():
    acl_file_reader= open('acl.txt', 'r') 
    interface=process_access_list_file(acl_file_reader)
    packet_file_reader= open('packet.txt', 'r')
    lines=packet_file_reader.readlines()
    for ip in lines:
        if is_packet_permitted(interface[0],ip):
            
            print("packet from "+str(ip).strip()+" permitted")
        else:
            print("packet from "+str(ip).strip()+" denied")

if __name__ == "__main__":
    main()
            


