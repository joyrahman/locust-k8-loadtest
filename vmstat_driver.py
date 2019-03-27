#format: python <script.py> exp_name total_duration output_dir

#from pssh.clients import ParallelSSHClient
from pprint import pprint
from pssh.clients.native import ParallelSSHClient
import sys
from pssh.utils import enable_logger, logger
from gevent import joinall
import time
import os
#from vmstat_sftp import copy_remote_to_local

import paramiko
paramiko.util.log_to_file('/tmp/paramiko.log')
paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))


def copy_remote_to_local(host,infile,outfile,local_path):
    username = "cloudsys"
    port = 22
    remote_images_path="/home/cloudsys/"
    #local_path="./"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username)
    sftp = ssh.open_sftp()

    file_remote = os.path.join(remote_images_path,infile)
    file_local = os.path.join(local_path,outfile)

    sftp.get(file_remote, file_local)
    
    sftp.close()
    ssh.close()




def process_vmstat():
    vmfile = sys.argv[1]
    start_pos = int(sys.argv[2])
    end_pos = int(sys.argv[3])
    out_file = sys.argv[4]
    averaging_factor = end_pos - start_pos

    #containers = {'carts':0,'carts-db':0,'front-end':0,'orders':0}
    containers = {}
    dictionary = {}
    hostname = vmfile.split(_)[0] #kb-w12
    vm_cpu_average=0

    # do processing of the vmstat file

    f_out = open(out_file,'a')

    with open(vmfile,'r') as f1:
        #field12 for user cpu
        vm_cpu_sum = 0
        count = 0
        #escape = 0
        for line in f1:

            if ("procs" in line) or ("swpd" in line):
                pass
            else:
                if count>=start_pos and count <= end_pos:
                    vm_cpu_sum += int(line.split()[13])
                count += 1
        vm_cpu_average = vm_cpu_sum*1.0/averaging_factor

    #write output to file
    output_record="{}:{},".format(hostname,vm_cpu_average)
    output_record = output_record.rstrip(',')
    output_record += "\n"
    f_out.write(output_record)
    f_out.close()

#from post_process_perfstat import post_process_perfstat

def main():
    exp_name = sys.argv[1]
    total_duration = int(sys.argv[2])
    output_dir = sys.argv[3]
    interval=5
    cpu_frequency = total_duration //5
    user="cloudsys"



    hosts = []
    for i in xrange(1,5):
        for j in xrange(1,5):
            hosts.append("kb-w{}{}".format(i,j))

    client = ParallelSSHClient(hosts,user)

    try:
        output = client.run_command('vmstat  {} {} > {}_vmfile.tmp '.format(interval, cpu_frequency, exp_name))
    except Exception as e:
        print(e)


    time.sleep(total_duration)



    #create the dir if not exist

    if not os.path.exists(output_dir)==True:
        os.makedirs(output_dir)

    for vm in hosts:
        infile_name = "{}_vmfile.tmp".format(exp_name)
        outfile_name = "{}_vmfile.tmp".format(vm)
        print("trying to copy: {} {} {}".format(vm,infile_name,outfile_name,output_dir))
        copy_remote_to_local(vm,infile_name, outfile_name, output_dir)
    #call the post processing here



if __name__ == "__main__":
    main()