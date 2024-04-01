class Find_commands:
    def find(screen: str):        
        last_hash_index = screen.rfind('#')        
        if "config" in screen[last_hash_index:]:
            #place = screen.find("\\config")            
            #end = place + 9            
            #while True:
            #    if screen[end].isalpha():                    
            #        end = end + 1
            #        continue
            #    else:                   
            #        break         
            #print(end)              
            #print("\n"+screen[place+8:end])
            #print("\nValue: " + screen[last_hash_index+9:].strip())            
            return (True, "config")
        return (False,"")
            