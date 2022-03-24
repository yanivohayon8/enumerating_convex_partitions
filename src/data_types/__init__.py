import lxml.etree as etree

class XmlWrapper():
    
    def __init__(self,prefix="_"):
        self.element = etree.Element(f"{prefix}")
    
    def set_att(self,att,val):
        self.element.set(att,val)

    def add_child(self,child):
        self.element.append(child.element)

    def indent(self):
        etree.indent(self.element,space="\t")
    
    def toString(self):
        # return etree.tostring(self.element).decode("UTF-8")
        return etree.tostring(self.element,pretty_print=True).decode("UTF-8")

    def print(self):
        self.indent()
        print(self.toString())