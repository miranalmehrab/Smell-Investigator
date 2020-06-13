import ast

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.functions = []
        self.variables = []


    def visit_Import(self, node):
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        import_from = {}
        
        import_from["line"] = node.lineno
        import_from["from"] = node.module
        import_from["alias"] = []

        for alias in node.names:
            import_from["alias"] = alias.name
        
        self.imports.append(import_from)
        self.generic_visit(node)

    def visit_FunctionDef(self,node):
        
        func_def = {} 
        
        func_def["line"] = node.lineno
        func_def["name"] = node.name
        func_def["args"] = []

        for arg in node.args.args:
            func_def["args"].append(arg.arg)

        self.functions.append(func_def)
        self.generic_visit(node)

    def visit_Assign(self,node):
        
        variable = {}
        variable["line"] = node.lineno

        for target in node.targets:
            variable["name"] = target.id

        if isinstance(node.value, ast.Constant):
            variable["value"] = node.value.value
            variable["valueSrc"] = "initialized"
            variable["isInput"] = False

        if isinstance(node.value, ast.Call):
            funcName = node.value.func.id
            variable["value"] = None
            variable["valueSrc"] = funcName
            variable["funcArgs"] = []

            if(funcName == "input"):
                variable["isInput"] = True
            else:
                variable["isInput"] = False
            
            for arg in node.value.args:
                variable["funcArgs"].append(arg.value)

        self.variables.append(variable)                
        self.generic_visit(node)


    def report(self):
        print('Imports:')
        print('--------------------------------------------------------')
        for import_statement in  self.imports:
            print(import_statement)

        print('Functions:')
        print('--------------------------------------------------------')
        for func_def_statement in self.functions:
            print(func_def_statement)

        print('Variables:')
        print('--------------------------------------------------------')
        for variable_assignment_statement in self.variables:
            print(variable_assignment_statement)

def main():
    srcFile = open('src.py','r')
    srcCode = srcFile.read()
    tree = ast.parse(srcCode,type_comments=True)
    
    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()
   
    # print(ast.dump(tree,include_attributes=True))

if __name__ == "__main__":
    main()