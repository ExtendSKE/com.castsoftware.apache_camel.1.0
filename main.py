import cast.analysers.ua
import cast.analysers.log as X
import xml.etree.ElementTree as ET
from cast.analysers import CustomObject,Bookmark,create_link
import re

fromRef = {}
toRef = {}

def get_namespace(element):
    """
    Determine the namespace of a element.
    """
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

class MyExtension(cast.analysers.ua.Extension):
    
    def __init__ (self):
        pass
    def start_analysis(self):
        cast.analysers.log.debug('Processing..!!')
        
    def start_file(self,file):
        filename = file.get_path()
        #X.debug(filename)
        
        if filename.endswith('.xml'):
            tree = ET.parse(filename)
            root = tree.getroot()
            count = 0
            for k in list(root.iter()) :
                data1 =re.sub('{.*?}', '',str(k.tag)) 
                if data1 == "from" :
                    try:
                        X.debug(k.attrib['uri'])
                        fromObj = CustomObject()
                        self.saveObject(fromObj, data1+"."+k.attrib['uri'], filename+'.'+data1, "Sender", file, filename+"."+data1+'.'+str(count) )
                        count = count+1
                        fromObj.save_position(Bookmark(file,1,1,-1,-1))
                        fromRef[fromObj]= [fromObj, k.attrib['uri']]
                    except (RuntimeError, TypeError, NameError):
                        pass
                elif data1 == "to" :
                    try:   
                        X.debug(k.attrib['uri'])
                        toObj = CustomObject()
                        self.saveObject(toObj, data1+"."+k.attrib['uri'], filename+'.'+data1, "Receiver", file, filename+"."+data1+'.'+str(count) )
                        count = count+1
                        toObj.save_position(Bookmark(file,1,1,-1,-1))
                        toRef[toObj]= [toObj, k.attrib['uri']]
                    except (RuntimeError, TypeError, NameError):
                        pass 
        elif filename.endswith('.java') :
            X.debug("")

        
    def end_file(self,file):
        pass
    def end_analysis(self):
        X.debug("****************")
        for fromObjs, fromURIs in fromRef.items():
            for toObjs, toURIs in toRef.items():
                if(toURIs[1] == fromURIs[1]):
                    X.debug("&&&&&&&&&")
                    create_link('callLink',fromObjs, toObjs, Bookmark(toObjs.parent,1,1,-1,-1))
                    X.debug("__________")
                    
            #X.debug(str(keys))
            #X.debug(str(values[1]))
        
        pass
    def saveObject(self, obj, name, fullname, obj_type, parent, guid): 
        obj.set_name(name)
        obj.set_fullname(fullname)
        obj.set_type(obj_type)
        obj.set_parent(parent)
        obj.set_guid(guid) 
        obj.save()
        pass
if __name__ == '__main__':
    pass
