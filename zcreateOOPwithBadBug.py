#!/usr/bin/env python3
import subprocess
import re
import os
import sys
from optparse import OptionParser

g_commandLine = ["zpool"]
g_keywords = {"universal_newlines": True}

##############################################################################################################################################################################
#Functionality_settings class:
#    Set up the way the options available to the user are supposed to work. 
#    The 'order' attribute is the order in which any entered command line arguments will be called. 
#    The 'needed_opts' attribute lists the options that are NEEDED for each option to work, or else the program breaks down 
#    The 'needed_args' attribute lists how many arguments are expected for each option
#    The 'stand_alone_opts' attribute lists arguments, which, if entered by the user, are the only options ultimately used, throwing everything else on the command line out
#    Options present in 'order' and 'stand_alone_opts' should be listed in the same order, i.e. -D takes precedence over -c so if they are both on the command line, only -D 
#    will be used
#    
#    The idea is that the behaviour of the script can be changed with minimal headaches
#    class methods:
#                   sortCMD
#                   deleteDuplicates
#                   destroyCommandLine
##############################################################################################################################################################################
class Functionality_settings: # the hard coded precedence of what operations to carry out
    def __init__(self):
        self.order = ['-n', '-D', '-c','-C', '-d', '-v', '-l', '-q', '-f', '-b', '-a', '-m', '-z']
    
        self.needed_opts = {
                   '-n': [None], 
                   '-D': ['-n'], 
                   '-c': [None], 
                   '-C': [None], 
                   '-d': [None],
                   '-v': [None], 
                   '-l': [None],
                   '-q': [None],
                   '-f': [None],
                   '-b': [None], 
                   '-a': [None], 
                   '-m': [None], 
                   '-z': [None]
                   }
                   
        self.needed_args =  {'-n': 1, '-D': 0, '-c': 0, '-C': 1, '-d': 1, '-v': 1, '-l': 1, '-q': 0, '-f': 0, '-b': 0, '-a': 1, '-m': 1, '-z': 0}   
        self.unallowed_opts = {
                   '-n': ['-c'], 
                   '-D': ['-c', '-C', '-d', '-v', '-l', '-q', '-f', '-b', '-a', '-m', '-z'], 
                   '-c': ['-n', '-D', '-C', '-d', '-v', '-l', '-b'], 
                   '-C': ['-D', '-c'], 
                   '-d': ['-D', '-c'],
                   '-v': ['-D', '-c'], 
                   '-l': ['-D', '-c'],
                   '-q': ['-D'],
                   '-f': ['-D'],
                   '-b': ['-D', '-c'], 
                   '-a': ['-D'], 
                   '-m': ['-D'], 
                   '-z': ['-D']
                   }
        
##############################################################################################################################################################################
#sortCMD function:
#    reorder the arguments in sys.argv (passed to the function as sysargv) according to the order given by the 'order' attribute
#Arguments:
#          sysargv: the command line, represented as a list of strings
##############################################################################################################################################################################       
    def sortCMD(self, sysargv):
        userOrder = sysargv.copy()
        order = self.order
        j = 1
        print("'-n', '-D', '-c','-C', '-d', '-v', '-l', '-q', '-f', '-b', '-a', '-m', '-z'")
        for i in order: #put the options and their arguments in the order that is desired. if the option is invalid, treat it as an argument and let the other option parser handle the error
            if i in userOrder:
                placing = sysargv.index(i)
                n=1                        # index for changing the list item referred to when there are multiple list items to move to the end of the command line
                m=1                        # index for changing the list item referred to when there are multiple list items to be moved ahead in the command line
                if placing != j:
                    if j+n < len(userOrder) and sysargv[j+n] not in order:
                        while j+n < len(userOrder) and sysargv[j+n] not in order:
                            n+=1
                        backOtheLine=sysargv[(j):(j+n)]                         #move an option and its arguments to the end of the line
                        del sysargv[(j+1):(j+n)]
                        sysargv[j] = i
                        sysargv+=backOtheLine
                        placing -= (n-1)
                    else:
                        backOtheLine=sysargv[j] #temporarily store the option that is about to be replaced 
                        sysargv[j] = i         
                        sysargv.append(backOtheLine)                            #move the option with no arguments to the end of the line               
                while placing+m < len(sysargv) and sysargv[placing+m] not in order: # treat anything directly after the option as an argument if it is not in the list "order"
                    sysargv.insert((j+m), sysargv[placing+m])    # insert the arguments directly following the new position of the option
                    argIndex=placing+m+1                          
                    sysargv.pop(argIndex)                        # pop the argument in the old postion off the list
                    m+=1
                self.deleteDuplicates(sysargv, j, i)   #get the index of where the next option belongs and store it in j
                j+=m  
                print(sysargv)
        
        self.checkCommandLine(sysargv) 
        
##############################################################################################################################################################################
#deleteDuplicates function:
#   function used by sortCMD to get rid of the duplicates in the command line.
#Arguments:
#    [j] is the current position within the command line [list representation] that is being "looked at" and thus is not yet sorted
#    [i] is an option from the 'order' attribute
#    [sysargv] is a list of strings, representing the command line    
##############################################################################################################################################################################  
    def deleteDuplicates(self, sysargv, j, i): #get rid of duplicates of the command (i) that are not located at the index that j has stored
        for k in range(len(sysargv)):
            if k != j and sysargv[k] == i: #this works on the assumption that no options should be entered twice as the current choices of options stand
                sysargv.pop(k)              
                sysargv.insert(0, None)
        while None in sysargv and len(sysargv)!=None:
            sysargv.remove(None)
            
##############################################################################################################################################################################
#destroyCommandLine function:
#    if there is a "stand_alone" option in the command line, throw out everything else in the command line so that the functions called later have less work to do, 
#    they can just assume that if the stand_alone option is present, it is the only option present.
#arguments:
#          sysargv: a list of strings. The list contains one string for each option and argument entered to the command line by the user
###############################################################################################################################################################################    
    def checkCommandLine(self, sysargv):
        the_lone_option = None
        helpers = []
        for opt in sysargv:
            if opt in self.order:
                the_lone_option = opt #the_lone_option is the option that is being analyzed currently
                if the_lone_option not in helpers: #if the_lone_option is in helpers already, all of its needed_opts will be, too
                    if self.needed_opts[the_lone_option][0] != None:
                        for needed_opt in self.needed_opts[the_lone_option]:
                            if needed_opt not in sysargv:
                                sys.exit("option not entered:{no} (needed in order to use {o})".format(no=needed_opt, o=opt))
                            if needed_opt not in helpers:
                                helpers.append(needed_opt)       
                    # find the children: if the stand alone option needs another option to work properly, go and get that. If this new "child" option needs an otion, go and get that. And so on  
                    helpers_update=helpers.copy()
                    while len(helpers_update) != 0:
                        for i in helpers:
                            if self.needed_opts[i][0] == None:
                                helpers_update.remove(i)       #get rid of "parents" of the "older generation" that have no children. Kill the spinster aunts!
                        for i in helpers_update:
                            for needed_opt in self.needed_opts[i]: 
                                if needed_opt not in sysargv:
                                    sys.exit("option not entered:{no} (needed in order to use {o})".format(no=needed_opt, o=opt))    
                                if needed_opt not in helpers:  #check that two options that are co-dependant do not cause infinite looping
                                    helpers_update.append(needed_opt)
                        for i in helpers: #get rid of the 'parents' that are no longer needed to find children
                            if i in helpers_update:
                                helpers_update.remove(i)
                        helpers+=helpers_update
                    if the_lone_option not in helpers:
                        helpers.append(the_lone_option)
        final_options = helpers  
        for opt in final_options:
            for key in final_options:
                if opt not in self.order:
                    for i in range(self.needed_args[key]): #find out if the needed options and arguments are present in the command line
                        if sysargv[sysargv.index(arg)-(i+1)] != key: #determine if arg can be treated as a valid positional argument to a needed option  
                            if key in self.unallowed_opts[opt]:
                                sys.exit("option {a} cannot be used with {b} ".format(a=opt, b=key))
                elif key in self.unallowed_opts[opt]:
                    sys.exit("option {a} cannot be used with {b} ".format(a=opt, b=key))
        
##############################################################################################################################################################################
#Zpool_options class:
#                     contains attributes for options used as flags in the program or options that can be added to the zfs command that will be executed without 
#    attributes:
#               build: a flag used to determine if the pool will built or not
#               quiet: a flag used to determine where the stdout and stderr will be sent, and whether or not to print the command that will build the zpool
#               options: the list of options that will be put directly into the "zpool create" command to build the pool
#               subprocess_keywords: keyword arguments for the subprocess method which is called to run the "zpool create" command
##############################################################################################################################################################################
class Zpool_options():
    def __init__(self):
        self.subprocess_keywords = {"universal_newlines": True}
        self.build = False
        self.quiet = False
        self.options = []    
    def set_ashift(self, option, opt_str, value, parser):
        self.options.extend(["-o", "ashift="+value])        
    def force(self, option, opt_str, value, parser, *args, **kwargs):
        self.options.append("-f")       
    def set_mount_point(self, option, opt_str, value, parser, *args, **kwargs):
        if os.path.exists(value):
            if os.path.isdir(value):
                if len(os.listdir(value)) == 0: 
                    self.options.extend(["-m", value])
                else:
                    sys.exit("the specified mount point exists as a non-empty directory")
            else:
                sys.exit("the specified mount point exists already and is not a directory")
        else:
            subprocess.run(["mkdir", value], stdout=subprocess.PIPE, universal_newlines=True).stdout
            self.options.extend(["-m", value])
    def silencer(self, option, opt_str, value, parser, *args, **kwargs):    
        self.quiet = True
        self.subprocess_keywords["stdout"]=subprocess.PIPE 
    def set_build(self, options, opt_str, value, parser, *args, **kwargs):
        self.build = True
        
##############################################################################################################################################################################
#Device class:
#    m_type: the media type a given storage device
#    s_device: the name of the storage device as named by the OS (sda, sdbm sd[a-z], etc)
#    alias: the alias for a storage device as given by the dmap or hmap script.       
##############################################################################################################################################################################   
class Device:
    def __init__(self, mediaType, storageDevice, aliasName):
        self.m_type = mediaType
        self.s_device = storageDevice
        self.alias = aliasName
        
##############################################################################################################################################################################
#Zpool_devices class:
#                    This class's attributes are characteristics of the zpool to be built, or destroyed
#   
#    devices: a list of device objects (of the Device class) that are in use by the server
#    drives_count: the number of drives that are in use by the server and are available to the pool that is being built. The user can make less pools available to the pool by
#                  entering a list of device names that is equal to or less than the amount of drives not in use by any other pool.                        
##############################################################################################################################################################################

class Zpool_devices:
    def __init__(self, dev): 
        self.devices = dev
        devs = subprocess.Popen(["zpool", "status"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        for line in devs:
            regex = re.search("^\s+([a-zA-Z]+).+$", line)
            for device in self.devices:
                if regex != None and regex.group(1) != None and regex.group(1) == device.s_device:
                    self.devices.remove(device)
        self.drives_count = len(self.devices)     
    def set_drives_count(self, options, opt_str, value, parser):
        if self.drives_count >= value:
            self.drives_count = value
        else:
            sys.exit("number of available drives is less than desired number of drives")   
    def elim(self, options, opt_str, value, parser): 
        print("-C has been passed the value: {v}".format(v=value))
        if value.lower() == "ssd":
            for device in self.devices:
                if device.m_type == "HDD":
                    self.devices.insert(0, None) 
                    self.devices.remove(device)
            if len(self.devices) != 0:
                while self.devices[self.devices.count(None)-1] == None:
                    self.devices.pop(self.devices.count(None)-1)
                    if len(self.devices) == 0:
                        break    
        elif value.lower() == "hdd":
            for device in self.devices:
                if device.m_type == "SSD":
                    self.devices.insert(0, None)
                    self.devices.remove(device)
            if len(self.devices) != 0:
                while self.devices[self.devices.count(None)-1] == None:
                    self.devices.pop(self.devices.count(None)-1)
                    if len(self.devices) == 0:
                        break
        else:
            sys.exit("the argument for this option must be either ssd or hdd (non-case sensitive)")
        self.drives_count = len(self.devices)
                   
##############################################################################################################################################################################
#Zpool_settings class:
#    vdev_quantity: the number of vdevs that the user wants to have in the pool that is being built
#    name: the name that the user wants for the pool that is being built or destroyed
#    raid_level: the RAID level that the user wants for every vdev in the zpool that is being built        
##############################################################################################################################################################################          
class Zpool_settings:
    def __init__(self):
        self.vdev_quantity=1
        self.name="zpool"
        self.raid_level="raidz2"
    def set_vdev_quantity(self, opt_str, value, parser):
        self.vdev_quantity = value
    def set_zpool_name(self, options, opt_str, value, parser):
        self.name = value
    def set_raid_level(self, options, opt_str, value, parser):
        self.raid_level = value
    def destroy(self, options, opt_str, value, parser):
        if subprocess.run(["zpool", "status"], universal_newlines=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE).returncode == 0:
            devs = subprocess.Popen(["zpool", "status"], universal_newlines=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout
            test_name = None
            for line in devs:
                regex = re.search("^\s+({n}+).+$".format(n = self.name), line)
                if regex != None:
                    test_name=regex.group(1)
                    break
            if test_name != None:
                choosing = True
                while choosing == True:
                    choice = input("Destroying {z}, You sure? ALL data will be lost. Continue?(y/N)".format(z=self.name))
                    if choice == "y":
                        subprocess.run(["zpool", "destroy", self.name], universal_newlines=True).stdout 
                        choosing = False
                    elif choice == "N":
                        choosing = False
                    else:
                        print("invalid option: \"{c}\"".format(c=choice))
            else:
                print("cannot open '{n}': no such pool".format(n=self.name))
##############################################################################################################################################################################
# setVdevCount function:
#                       determine the default number of vdevs for a zpool based on the number of drive bays, and return that number
# Arguments:
#           Zpool_dev: the class containing the number of drives that are available
##############################################################################################################################################################################                    
def setVdevCount(Zpool_dev): # Starting at default vdev_count for chassis size, if DRIVE_COUNT is indivisible by vdev_count, increment vdev_count by one and keep checking until it is.
    bays_count = 0
    allDRIVES=subprocess.Popen(["cat", "/etc/zfs/vdev_id.conf"], stdout = subprocess.PIPE, universal_newlines = True).stdout
    for line in allDRIVES:
        regex = re.search("^alias\s(\S+)\s", line)
        if regex != None:
            bays_count += 1 
        vdev_count=1 
        if bays_count==30:
            vdev_count=3
            
        if bays_count==45:
            vdev_count=5
        
        if bays_count==60:
            vdev_count=5
        
        while Zpool_dev.drives_count%vdev_count != 0:
            if Zpool_dev.drives_count%vdev_count == 0:
                break
                vdev_count=vdev_count+1
        return vdev_count            
##############################################################################################################################################################################
#customsort function:
#           sort available drives into new vdevs based on input prompted from the user, then create a pool from those vdevs
#Arguments:
#           options: an object containing the arguments entered for all options. attributes containing these values are named after the options themselves.
#           opt_str: the string that resulted in this function being called. This option is hard-coded as a valid option in the option parser class.
#           value: the value that was entered as an argument for the option, None in this case
#           parser: the entire OptionParser object that has been used to create this option
##############################################################################################################################################################################                
def customsort(options, opt_str, value, parser):
    subprocess.run(["lsdev"], universal_newlines=True)
    vdevs_count = int(input("number of vdevs: "))
    raid_level = [input("RAID level: ")] 
    zpool_name = input("Pool name: ")
    zpool_name = zpool_name.strip()
    raid_level[0]=raid_level[0].strip()
    if raid_level[0] == "stripe":
       raid_level = [None]
    i=0
    VDEVS = ["create", zpool_name]
    while i < vdevs_count:  
        devices = input("VDEV_{index}: ".format(index = i))
        devices = devices.split()
        VDEVS+=raid_level+devices
        i+=1
    makeCommandLine(VDEVS)

##############################################################################################################################################################################
#init_zpool_devices function:
#           get the device name, alias, and media type from lsdev for all the devices that are in use and then instantiate a device class for each of these drives
#Arguments:
#           No arguments
##############################################################################################################################################################################
def init_zpool_devices():
    devices = []
    lsdev = subprocess.Popen(["lsdev", "-tdn"], stdout=subprocess.PIPE, universal_newlines=True).stdout
    for line in lsdev:
        regex = re.findall("(\d+-\d+)\s+\(/dev/([a-z]+),([a-zA-Z]+)\)", line)
        if len(regex) >= 1:
            i = 0
            while i <= len(regex)-1:
                devices.append(Device(regex[i][2], regex[i][1], regex[i][0]))
                i+=1
    return devices   
 
##############################################################################################################################################################################
# autosort function:
#           use all the available drives to automatically create a pool 
#Arguments:
#           Zpool_opts: a Zpool_options class, 
#           Zpool_dev: a Zpool_devices class. The list of available devices is split up into vdevs, with RAID level and number of devices determined by the attributes of the 
#                      Zpool_settings class
#           Zpool_sett: a Zpool_settings class with attributes for the RAID level and the number of vdevs
############################################################################################################################################################################## 
def autosort(Zpool_opts, Zpool_dev, Zpool_sett):
    if Zpool_sett.raid_level == "stripe":
        Zpool_sett.raid_level=None
    VDEVS = [Zpool_sett.name]
    if Zpool_sett.vdev_quantity == 0:
        print("0 vdevs specified. There must be at least 1 vdev to create a pool")
    else:
        drivespVDEV = int(Zpool_dev.drives_count/Zpool_sett.vdev_quantity)   
        index = 0
        for j in range(Zpool_sett.vdev_quantity):
            temp_list = [Zpool_sett.raid_level]
            for i in range(drivespVDEV):
                temp_list.append(Zpool_dev.devices[index].s_device) 
                index += 1
            VDEVS+=temp_list 
        g_commandLine.append("create")
        makeCommandLine(VDEVS)

##############################################################################################################################################################################
#makeCommandLine function:
#                           remove any Nonetype objects from the VDEVS list, then append the VDEV list items to the global command line
#Argument:
#           VDEVS: a list of drives sorted into vdevs. For example, ['raidz2', 'sda', 'sdb', 'sdc', 'sdd', 'raidz2', 'sde', 'sdf', 'sdg', 'sdh']
##############################################################################################################################################################################
def makeCommandLine(VDEVS):
    for i in VDEVS:
            if i == None:
                VDEVS.remove(None)
    for i in VDEVS:
            g_commandLine.append(i)
            
##############################################################################################################################################################################
# main:
#      Instantiate classes to contain the information about the available drives needed to create or destroy a zpool.
#      Parse the command line and call class methods to set attributes of the zpool that is to be created or destroyed.
#      Create or destroy a zpool.
##############################################################################################################################################################################           
def main():
    Fsettings = Functionality_settings()
    Zpool_opts = Zpool_options()
    devices = init_zpool_devices()
    Zpool_dev = Zpool_devices(devices)
    Zpool_sett = Zpool_settings()
    Zpool_sett.vdev_quantity=setVdevCount(Zpool_dev)
    parser = OptionParser()
    parser.add_option("-a", "--set-ashift-value", action="callback", type=str, callback=Zpool_opts.set_ashift, help="[-a] Set ashift value")
    parser.add_option("-b", "--build", action="callback", callback=Zpool_opts.set_build, help="-b: Build Flag. Include to build the array")
    parser.add_option("-C", "--create-using-drive-type", action="callback", type=str, callback=Zpool_dev.elim, help="[-C] Device class. Only use this type of device. \
            '\n' Default: Use all drive '\n' Options: hdd, ssd")
    parser.add_option("-c", "--custom", action="callback", callback=customsort, help="[-c] Custom Flag. Include for manual pool configuration")
    parser.add_option("-D", "--destroy", action="callback", callback=Zpool_sett.destroy, help="destroy zpool")
    parser.add_option("-d", "--set-drives_count", action="callback", type=int, callback=Zpool_dev.set_drives_count, help="set quantity of drives to use")
    parser.add_option("-f", "--force", action="callback", callback=Zpool_opts.force, help="force action")
    parser.add_option("-l", "--RAID level", action="callback", type=str, callback=Zpool_sett.set_raid_level, help="[-l] Specify RAID level '\n'     Default is raidz2 '\n'      Options: raidz[123], mirror, stripe")
    parser.add_option("-m", "--set-mount-point", action="callback", type=str, callback=Zpool_opts.set_mount_point, help="set mount point")
    parser.add_option("-n", "--name-pool", action="callback", type=str, callback=Zpool_sett.set_zpool_name, help="[-n] Specify zpool name. Defaults to zpool")
    parser.add_option("-q", "--quiet", action="callback", callback=Zpool_opts.silencer, help="don't show stdout stream. Don't print details")
    parser.add_option("-v", "--set-vdev-quantity", action="callback", type=int, callback=Zpool_sett.set_vdev_quantity, help="set quantity of the vdevs")
    parser.add_option("-z", "--debug", action="store_true", default=False, dest="debug", help="[-z] Debug flag. Prints all varibles&temp files to terminal")
    sysargv = sys.argv
    Fsettings.sortCMD(sysargv)
    
    try:
        (options, args) = parser.parse_args()
        
        if options.debug == True:
            print("    drive count: {dc} \n    raid level: {rl} \n    zpool name: {zpn} \n    vdev count: {vdc} \n    drives/vdev: {dpd}".format(dc=Zpool_dev.drives_count,\
            rl=Zpool_sett.raid_level, zpn=Zpool_sett.name, vdc=Zpool_sett.vdev_quantity, dpd=int(Zpool_dev.drives_count/Zpool_sett.vdev_quantity)))
            print("the list of available drives:")
            for i in Zpool_dev.devices:
                print("    {t} {sd} {al}".format(t=i.m_type, sd=i.s_device, al=i.alias))      
            
        for key in Zpool_opts.subprocess_keywords:
            g_keywords[key] = Zpool_opts.subprocess_keywords[key]   
        if not '-D' in sys.argv and not '-c' in sys.argv:
            autosort(Zpool_opts, Zpool_dev, Zpool_sett)
        for i in Zpool_opts.options:
            g_commandLine.append(i)
                
        if Zpool_opts.quiet == False and '-D' not in sys.argv:
            for command in g_commandLine:
                print(command, end = ' ')
            print(' ')
        if Zpool_opts.build == True or '-c' in sys.argv:
            subprocess.run(g_commandLine, **g_keywords).stdout    
        if Zpool_opts.build != True and '-D' not in sys.argv and '-c' not in sys.argv:
            print("Use -b flag to build the above pool\nUse -h flag for more options")
    except KeyboardInterrupt:
        sys.exit('\n')
       
if __name__ == "__main__":
    main()