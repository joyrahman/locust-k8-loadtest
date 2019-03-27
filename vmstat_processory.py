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