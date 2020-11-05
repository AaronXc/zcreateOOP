 sortCMD(self, sysargv):
        userOrder = sysargv.copy()
        order = self.order
        j = 1
        print("'-n', '-D', '-c','-C', '-d', '-v', '-l', '-q', '-f', '-b', '-a', '-m', '-z'")
        for i in order: #put the options and their arguments in the order that is desired. if the option is invalid, treat it as an argument and let the other option parser handle the error
            if i in userOrder:
				for k in range(self.needed_args[key]): #find out if the needed options and arguments are present in the command line
                        if sysargv[sysargv.index(arg)-(k+1)] != key: #determine if arg can be treated as a valid positional argument to a needed option  
                            if key in self.unallowed_opts[opt]:
                                sys.exit("option {a} cannot be used with {b} ".format(a=opt, b=key))
                elif key in self.unallowed_opts[opt]:
                    sys.exit("option {a} cannot be used with {b} ".format(a=opt, b=key))
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