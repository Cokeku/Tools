#!/usr/bin/env python3

import sys
import os
import psutil
from psutil._common import bytes2human

def cpu_info():
    temp1 = "CPU Number: %s \t CPU Used: %s%%  CPU Load: %.2f %.2f %.2f "
    cpu_num = str(psutil.cpu_count())
    cpu_sum_per = str(psutil.cpu_percent(interval=1))
    cpu_load_avg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    cpt = psutil.cpu_times_percent(percpu=False)
    
    '''
    CPU Number: 8 	 CPU Used: 0.5%  CPU Load: 0.00 0.38 0.62 
    '''

    print( temp1 % ( 
        cpu_num, 
        cpu_sum_per,
        cpu_load_avg[0],
        cpu_load_avg[1],
        cpu_load_avg[2]))

    '''
    %CPU(s)	user	nice	system	idle	iowait	irq	sirq	steal	guest	guest_nice
	0.10	0.00	0.20	99.60	0.00	0.00	0.00	0.00	0.00	0.00
    '''
    temp2 = "\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f"
    print("%CPU(s)\tuser\tnice\tsystem\tidle\tiowait\tirq\tsirq\tsteal\tguest\tguest_nice")
    print( temp2 % (
        cpt.user,
        cpt.nice,
        cpt.system,
        cpt.idle,
        cpt.iowait,
        cpt.irq,
        cpt.softirq,
        cpt.steal,
        cpt.guest,
        cpt.guest_nice
    ))


def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        print('%-10s : %7s' % (name.capitalize(), value))

def disk_usage():
    templ = "%-17s %8s %8s %8s %8s%% %9s  %s"
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                   "Mount"))
    for part in psutil.disk_partitions(all=False):
        # if os.name == 'nt':
        #     if 'cdrom' in part.opts or part.fstype == '':
        #         continue
        usage = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))

def main():
    cpu_info()
    print('\nMEMORY\n------')
    pprint_ntuple(psutil.virtual_memory())
    print('\nSWAP\n------')
    pprint_ntuple(psutil.swap_memory())
    print('\n------')
    disk_usage()
    

if __name__ == '__main__':
    main()
