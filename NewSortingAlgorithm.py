 sortCMD(self, sysargv):
        userOrder = sysargv.copy()
        good_order = self.order
        after_sorting = []
        print("'-n', '-D', '-c','-C', '-d', '-v', '-l', '-q', '-f', '-b', '-a', '-m', '-z'")
        for option in good_order: #put the options and their arguments in the order that is desired. if the option is invalid, treat it as an argument and let the other option parser handle the error
            after_sorting.append(option)
            if option in userOrder:
                j=0
				for i in range(self.needed_args[option])-1: 
                    if userOrder[userOrder.index(arg)+(i+1)] not in good_order: #determine if arg can be treated as a valid positional argument to a needed option  
                        after_sorting.append(option)
                        j=i
                    else:
                        sys.exit("The {o} option requires {i} arguments, {j} entered".format(o=option, i=len(range(self.needed_args[option]), j=i))
                while userOrder[j+2] not in good_order:
                    j+=1
                if j != i:
                    sys.exit("The {o} option requires {i} arguments, {j} entered".format(o=option, i=(i+1), j=(j+2)))
                    
                print(after_sorting)