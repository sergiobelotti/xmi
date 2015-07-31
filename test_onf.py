import xml.dom.minidom as minidom
import logging
import sys
import os


logging.basicConfig(level=logging.DEBUG)

class yang_class():
    def __init__(self) :
        self.name = ""
        self.inherits = [] # class id it inherits
        self.comment = ""
        self.class_id = ""
        self.attr = []
        
    def __str__(self):
        string = "Class name: " + self.name + " id: " + self.class_id 
        if self.inherits :
            string += " inherits: " + str(self.inherits) 
        if self.attr :
            string += " attributes: " + str(self.attr)
        return string

class yang_attribute():
    def __init__ (self):
        self.name = ""
        self.aggregation = ""
        self.agg_type = ""
        self.agg_association = ""
        self.type = ""
        self.lower_value = ""
        self.upper_value = ""
        self.default_value = ""
        
    def __str__ (self):
        string = "Attribute name: " + self.name
        
def get_packages(dom):
    pkgs = dom.getElementsByTagName('uml:Package')
    #print pkgs[0]
    i = 0
    for child in pkgs[0].childNodes :
            if child.nodeType == child.ELEMENT_NODE and child.nodeName == "packagedElement" :
                print "Child index: " + str(i) + " " + child.attributes["xmi:type"].value + " " + child.attributes["name"].value        
                parse_package(child, i)
    
def parse_package(pkg, i = 1):
    i+=1
    print pkg.nodeName + " Type: " + pkg.getAttribute("xmi:type")
    if pkg.getAttribute("xmi:type") == "uml:Enumeration" :
        get_enumeration( pkg)
    elif pkg.getAttribute("xmi:type") == "uml:DataType" :
        get_data_type( pkg)
    elif pkg.getAttribute("xmi:type") == "uml:Class" :
        get_class(pkg)
    elif pkg.getAttribute("xmi:type") == "uml:Association":
        get_association(pkg)
    elif pkg.getAttribute("xmi:type") == "uml:Dependency":
        get_dependency(pkg)    
    elif pkg.getAttribute("xmi:type") == "uml:Constraint":
        get_constraint(pkg)
    elif pkg.getAttribute("xmi:type") == "uml:PrimitiveType":
        print "PrimitiveType"  
    elif pkg.getAttribute("xmi:type") == "uml:AssociationClass":
        print "AssociationClass" 
    elif pkg.getAttribute("xmi:type") == "uml:Activity":
        print "Activity"     
    elif pkg.getAttribute("xmi:type") == "uml:Component":
        print "Component"     
    elif pkg.getAttribute("xmi:type") == "uml:Realization":
        print "Realization"  
    elif pkg.getAttribute("xmi:type") == "uml:Usage":
        print "Usage"  
    elif pkg.getAttribute("xmi:type") == "uml:InformationFlow":
        print "InformationFlow" 
    elif pkg.getAttribute("xmi:type") == "uml:Abstraction":
        print "Abstraction"     
    elif pkg.getAttribute("xmi:type") == "uml:InformationItem":
        print "InformationItem"               
    elif pkg.getAttribute("xmi:type") == "uml:Interface":
        print "Interface" 
    elif pkg.getAttribute("xmi:type") == "uml:InterfaceRealization":
        print "InterfaceRealization"                                                    
    elif pkg.getAttribute("xmi:type") == "uml:Package" :
        for child in pkg.childNodes :
            if child.nodeType == child.ELEMENT_NODE and child.nodeName == "packagedElement" :
                print "Child index: " + str(i) + " " + child.attributes["xmi:type"].value + " " + child.attributes["name"].value        
                parse_package(child, i)
            if child.nodeType == child.ELEMENT_NODE and child.nodeName == "ownedComment" :
                print "Comment: " + get_comment ( child )            
    else:
        sys.exit("Not interpreted node: " + pkg.getAttribute("xmi:type") )
        
def get_comment(child):
    
    body = child.getElementsByTagName("body")
    if body.length > 0:
        return body[0].firstChild.nodeValue.encode("utf-8")
    else:
        return ""

def get_enumeration(child):
    print "Enumeration name: " + child.attributes["name"].value 
    print "Comment: " + get_comment ( child )
    enums = child.getElementsByTagName('ownedLiteral')
    for enum in enums:
        print "Value: " + enum.attributes["name"].value

def get_data_type (child):
    print "DataType name: " + child.attributes["name"].value
    print "Comment: " + get_comment ( child )
    attribs= child.getElementsByTagName('ownedAttribute')
    for attrib in attribs:
        get_attribute(attrib)
    

def get_attribute (child):
    #print "Attribute name: " + child.attributes["name"].value
    att = yang_attribute()
    att.name = child.attributes["name"].value
    
    att.aggregation = child.getAttribute("aggregation")
    att.agg_type = child.getAttribute("type")
    att.agg_association = child.getAttribute("association")
    
    att.type = get_attribute_type( child )
    att.lower_value = get_attribute_lower_value( child )
    att.upper_value = get_attribute_upper_value( child )
    att.default_value = get_attribute_default_value( child )
    
    return att

def get_attribute_type (child):
    attr_type = child.getElementsByTagName("type")
    if attr_type.length > 0:
        href = attr_type[0].getAttribute("href")
        if href == "pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String" :
            return "string"
        elif href == "pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#Integer" :
            return "integer"
        else:
            sys.exit("Not considered type: " + str(attr_type[0].toxml()) )
    return ""


def get_attribute_lower_value( child ):
    lowerValue = child.getElementsByTagName("lowerValue")
    if lowerValue.length > 0:
        value = lowerValue[0].getAttribute("value")
        print "lowerValue: " + value
        return value
    return ""

def get_attribute_upper_value( child ):
    upperValue = child.getElementsByTagName("upperValue")
    if upperValue.length > 0:
        value = upperValue[0].getAttribute("value")
        print "upperValue: " + value
        return value
    return ""

def get_attribute_default_value( child ):
    defaultValue = child.getElementsByTagName("defaultValue")
    if defaultValue.length > 0:
        value = defaultValue[0].getAttribute("name")
        print "defaultValue: " + value
        return value
    return ""

def get_class ( child):
    print "Class name: " + child.attributes["name"].value
    a = yang_class()
    a.name = child.attributes["name"].value
    a.class_id = child.attributes["xmi:id"].value 
    a.comment = get_comment(child)
    #inheritance
    inhs = child.getElementsByTagName("generalization")
    for inh in inhs :
        inh_id = inh.getAttribute("general")
        a.inherits.append(inh_id)

    #get owned attributes
    attrs = child.getElementsByTagName("ownedAttribute")
    for attr in attrs :
        attrib = get_attribute(attr)
        a.attr.append(attrib)
    #save class
    class_dict[a.name] = a
    
def get_association (child):   
    print "Association"
    
def get_dependency(child):
    print "Dependency"

def get_constraint(child):
    print "Constraint"





if __name__ == "__main__":


    class_dict = {}
       
    try:
        dom = minidom.parse("CoreModel.uml")
    except IOError:
        raise PyXMIFileNotFound(file_name)
    except:
        raise PyXMIBadXML(file_name)
        

    get_packages(dom)
    
    for cl in class_dict :
        print class_dict[cl]
        
    print "Length: " + str (len(class_dict))

