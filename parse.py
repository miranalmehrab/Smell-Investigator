import ast

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports = {"import": [], "from": []}
        self.functions = {"name":[],"args":[]}
        self.variables = {"name":[],"valueSrc":[],"value":[],"isInput":[],"funcArgs":[]}


    def visit_Import(self, node):
        for alias in node.names:
            self.imports["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports["from"].append(alias.name)
        self.generic_visit(node)

    def visit_FunctionDef(self,node):
        self.functions["name"].append(node.name)
        for arg in node.args.args:
            self.functions["args"].append(arg.arg)
        self.generic_visit(node) 

    def visit_Assign(self,node):
        # print(type(node))
        
        for target in node.targets:
            self.variables["name"].append(target.id)

        if isinstance(node.value, ast.Constant):
            print('inner value: ',node.value.value)    
            
            self.variables["value"].append(node.value.value)
            self.variables["valueSrc"].append("initialized")
            self.variables["isInput"].append(False)

        if isinstance(node.value, ast.Call):
            self.variables["value"].append(None)
            funcName = node.value.func.id
            
            if(node.value.func.id == "input"):
                self.variables["isInput"].append(True)
            else:
                self.variables["isInput"].append(False)

            self.variables["valueSrc"].append(node.value.func.id)
            
            for arg in node.value.args:
                print('inner func args: ',arg.value)
                self.variables["funcArgs"].append(arg.value)
                
        self.generic_visit(node)


    def report(self):
        x = 2
        # print(self.imports)
        # print(self.functions)
        print(self.variables)


def main():
    srcFile = open('src.py','r')
    srcCode = srcFile.read()
    tree = ast.parse(srcCode,type_comments=True)

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()

    # print(ast.dump(tree,include_attributes=False))

if __name__ == "__main__":
    main()