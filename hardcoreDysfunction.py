#!/usr/bin/env python3

import subprocess
import re
import os
import sys
from optparse import OptionParser

class Device:
    def __init__(self, mediaType, storageDevice, aliasName)
        self.m_type = mediaType
        self.s_device = storageDevice
        self.alias = aliasName

class Zpool_settings:
    #def __init__(self):
    devices = []
    name = None
    drives_count = 0
    vdevs_count = 0
    raid_level = None
    Settings.commands = []
    subprocess_keywords = {"universal_newlines": True}
    
    def elim_HDDS():
        for device in self.devices:
            if stuff.devices == "HDD":
                self.devices.insert(0, None)        
        if len(self.devices) != 0:
            while self.devices[self.devices.count(None)-1] == None:
                self.devices.pop(self.devices.count(None)-1)
                if len(self.devices) == 0:
                    break
    def elim_SSDS():
        for device in self.devices:
            if stuff.devices == "SSD":
                self.devices.insert(0, None)        
        if len(self.devices) != 0:
            while self.devices[self.devices.count(None)-1] == None:
                self.devices.pop(self.devices.count(None)-1)
                if len(self.devices) == 0:
                    break
                    
    def set_drives_count():
        self.drives_count = len(self.devices)
        
        
class Commands():
    def set_ashift(option, opt_str, value, parser, *args, **kwargs)

class Zpool():
    devices = []
    name = None
    drives_count = 0
    vdevs_count = 0
    raid_level = None
    
                 
    
def init_zpool_settings():
    Settings = zpool_settings()
    #options.drive_tpyes = options.drive_types.strip()
    #options.drive_types = options.drive_types.lower()
    lsdev = subprocess.Popen(["lsdev", "-tdn"], stdout=subprocess.PIPE, universal_newlines=True).stdout
    for line in lsdev:
        regex += re.findall("(\d+-\d+)\s+\(/dev/([a-z]+),(a-zA-Z)\)", line)  
    if regex.group(1) and regex.group(2) and regex.group(3):
        Settings.devices.append(Device(regex.group(3), regex.group(2), regex.group(1)))
    return Settings
    

    
def get_path_variables():
    # get the alias config path, if it fails, assume /etc
    # get the device path, if it fails, assume /dev
    
    conf_path = os.getenv('ALIAS_CONFIG_PATH')
    if conf_path == None:
        log("No alias config path set in profile.d ... Defaulting to /etc")
        conf_path = "/etc"
    dev_path = os.getenv('ALIAS_DEVICE_PATH')
    if dev_path == None:   
        log("No device path set in profile.d ... Defaulting to /etc")
        dev_path = "/dev"
    
    return conf_path, dev_path

def getBAYSCOUNT(DEVICE_PATH): # Fills array DRIVES with physical slot number, only if there is a drive present (creates array of all drive slots, whether a is drive present or not)
    BAYS_COUNT = 0
    allDRIVES=subprocess.Popen(["cat", "/etc/zfs/vdev_id.conf"], stdout = subprocess.PIPE, universal_newlines = True).stdout
    for line in allDRIVES:
        regex = re.search("^alias\s(\S+)\s", line)
        if regex != None:
            BAYS_COUNT += 1
        
    return BAYS_COUNT

def setvdevcount(Settings, BAYS_COUNT): # Starting at default vdevs_count for chassis size, if drives_count is indivisible by vdevs_count, increment vdevs_count by one and keep checking until it is.
    drives_count = len(Settings.devices)
    Settings.vdevs_count=1 
    if BAYS_COUNT==30:
        Settings.vdevs_count=3
        
    if BAYS_COUNT==45:
        Settings.vdevs_count=5
     
    if BAYS_COUNT==60:
        Settings.vdevs_count=5
	
    while drives_count%Settings.vdevs_count != 0:
        if drives_count%Settings.vdevs_count == 0:
            break
            Settings.vdevs_count=Settings.vdevs_count+1
   

def autosort( vdevs_count, drivespVDEV, autos): 
    #if subprocess.run(["test", "-e", options.mount_point+"/z.tmp" ], stdout = subprocess.PIPE, universal_newlines = True).stdout == 0:
     #   subprocess.run(["rm", "-f", options.mount_point+"/z.tmp"], stdout=subprocess.PIPE, universal_newlines=True)
    
    
    VDEVS = [options.zpool_name]
    
    INDEX = 0
    for j in range(vdevs_count):
        temp_list = [options.raid_level]
        for i in range(drivespVDEV):
            temp_list.append(autos.[INDEX][1]) 
            INDEX += 1
        VDEVS+=temp_list  
    
    if options.build == True:
        createpool(Settings.commands, VDEVS, kwargs_for_subprocess)    
    else:
        print("Use -b flag to build the above pool" '\n'"Use -h flag for more options")
        
def customsort(options, Settings.commands, kwargs_for_subprocess): 
    #if subprocess.run(["test", "-e", options.mount_point+"/z.tmp" ], stdout = subprocess.PIPE, universal_newlines = True).stdout == 0:
     #   subprocess.run(["rm", "-f", options.mount_point+"/z.tmp"], stdout=subprocess.PIPE, universal_newlines=True)
    subprocess.run(["lsdev"], universal_newlines=True)
    vdevs_count = int(input("number of vdevs: "))
    options.raid_level = [input("RAID level: ")] 
    options.zpool_name = input("Pool name: ")
    
    i=0
    VDEVS = [options.zpool_name]
    while i < vdevs_count:  
        devices = input("VDEV_{index}: ".format(index = i))
        devices = devices.split()
        VDEVS+=options.raid_level+devices
        i+=1
    
    if options.build == true:
        createpool(Settings.commands, VDEVS, kwargs_for_subprocess)    
    else:
        print("Use -b flag to build the above pool" '\n'"Use -h flag for more options") 
        
def createpool(Settings.commands, VDEVS, kwargs_for_subprocess): # Reads z.tmp file and writes zpool creation command and saves in z.conf
    
    commandLine = Settings.commands+VDEVS
    subprocess.run(commandLine, **kwargs_for_subprocess).stdout
 """ 
def getCommandOptions(options, Settings, vdevs_count):
    kwargs_for_subprocess = { "universal_newlines": True}
    Settings.commands = []
    if options.force:
        # add the -f option to Settings.commands. 
        Settings.commands.append("-f")
    if options.quiet:
        # for the subprocess.run([], stdout=subprocess.PIPE) <- use that 
        kwargs_for_subprocess["stdout"] = "subprocess.PIPE"
        
    if options.destroy:
        #call the createpool function with the command [zpool destroy "zpool_name"]
        Settings.commands.extend(["zpool", "destroy", options.zpool_name])
    if options.mount_point != None:
    #    # change mount_point 
        Settings.commands.extend(["-m", options.mount_point])
    
    if options.ashift != None:
        Settings.commands.extend(["-o", "ashift="+options.ashift]) 
    if options.custom == True:
        #call the customsort function
        Settings.commands[0:0] = ["zpool", "create"]
        customsort(options, Settings.commands, kwargs_for_subprocess)

    #if options.build:
        #build the zpool, this might have to be a flag. can just use the value from the options object as the flag
        #BUILD_FLAG=True
    #if options.drive_types != None:
     #   getDriveTypes(options, DRIVES)
    #if -l in args:
        # change raid_level.  raid_level = options.raid_level so no further action required
    #if -n in args:
        # change zpool_name. n.f.a.r. because I can just use the options.zpool.name for the name whenever a name is needed.
    #if -t in args:
        # Settings.commands.append(options.) i am confused   
    if options.vdev_quantity != 0:
        # change the vdevs_count
        vdevs_count = options.vdev_quantity
        
    drivespVDEV=int(len(autos.devices)/vdevs_count)
    
    if options.drive_quantity != 0:
        drivespVDEV = int(options.drive_quantity/vdevs_count)
    if options.custom != True and options.destroy == False:
        Settings.commands[0:0] = ["zpool", "create"]
        autosort(options, vdevs_count, drivespVDEV, autos, Settings.commands, kwargs_for_subprocess)
        
    if options.debug:
        print("drive count: {dc} '/n'raid level: {rl} '/n'zpool name: {zpn} '/n'vdev count: {vdc} '/n'driveTypes/vdev: {dpd} '/n'driveTypes array: {da}".format(dc=drives_count, \
        rl=options.raid_level, zpn=options.zpool_name, vdc=vdevs_count, dpd=int(drives_count/vdevs_count), da= options.drive_types))
    return(vdevs_count, Settings.commands, kwargs_for_subprocess)
"""   
    
    
def main():
    
    (CONFIG_PATH, DEVICE_PATH) = get_path_variables()
    
    Settings = init_zpool_settings()
    Commands = Commands()
        
    parser = OptionParser()
    parser.add_option("-a", "--set-ashift-value", action="callback", type=int, callback=Commands.set_ashift(), help="[-a] Set ashift value")
    parser.add_option("-b", "--build", action="callback", callback=Commands.set_build_flag, help="-b: Build Flag. Include to build the array")
    parser.add_option("-C", "--create-using-drive-type", action="store", type=str, dest="drive_types", default=None, help="[-C] Device class. Only use this type of device. \
            '\n' Default: Use all drive '\n' Options: hdd, ssd")
    parser.add_option("-c", "--custom",action="store_true", default=False, dest="custom", help="[-c] Custom Flag. Include for manual pool configuration")
    parser.add_option("-D", "--destroy", action="store_true", default=False, dest="destroy", help="[-D] Destroys zpool")
    parser.add_option("-d", "--quantify-driveTypes", action="store", type=int, default=0, dest="drive_quantity", help="[-d] Specify how many driveTypes to use. '\n'      Default is every drive attached to HBA controller")
    parser.add_option("-f", "--force", action="store_true", default=False, dest="force", help="[-f] Force Flag. Use if bricks are already present on zpool")
    parser.add_option("-l", "--RAID level", action="store", type=str, default="raidz2", dest="raid_level", help="[-l] Specify RAID level '\n'     Default is raidz2 '\n'    Options: raidz[123], mirror, stripe")
    parser.add_option("-m", "--mount-point", action="store", type=str, default="/", dest="mount_point", help="[-m] Specify alternate mount point '\n'		Default: /{pool}")
    parser.add_option("-n", "--name-pool", action="store", type=str, default="pool", dest="zpool_name", help="[-n] Specify zpool name. Defaults to zpool")
    parser.add_option("-q", "--quiet", action="store_true", default=False, dest="quiet", help="[-q] Quiet Mode")
    parser.add_option("-t", "--tunable", action="store_false", default=True, dest="tunable", help="[-t] IF flag is present, DO NOT apply default ZFS tuneables")
    parser.add_option("-v", "--quantify-vdevs", action="store", type=int, default=0, dest="vdev_quantity", help="[-v] Specify number of VDEVs to use")
    parser.add_option("-z", "--debug", action="store_true", default=False, dest="debug", help="[-z] Debug flag. Prints all varibles&temp files to terminal")
    (options, args) = parser.parse_args()
    
    BAYS_COUNT = getBAYSCOUNT(DEVICE_PATH)
    setvdevcount(Settings, BAYS_COUNT)
    getCommandOptions(options, Settings, vdevs_count)
    
if __name__ == "__main__":
    main()