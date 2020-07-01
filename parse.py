import ast
import json


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.inputs = []
        self.statements = []

    def visit_Import(self, node):
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        import_from = {}

        import_from["type"] = "import"
        import_from["line"] = node.lineno
        import_from["from"] = node.module
        import_from["alias"] = []

        for alias in node.names:
            import_from["alias"] = alias.name

        self.statements.append(import_from)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):

        func_def = {}

        func_def["type"] = "function_def"
        func_def["line"] = node.lineno
        func_def["name"] = node.name
        func_def["args"] = []

        for arg in node.args.args:
            func_def["args"].append(arg.arg)

        self.statements.append(func_def)
        self.generic_visit(node)



    def visit_Assign(self, node):

        variable = {}
        variable["type"] = "variable"
        variable["line"] = node.lineno
        # print(ast.dump(node))

        for target in node.targets:
            variable["name"] = target.id

        if isinstance(node.value, ast.Constant):
            variable["value"] = node.value.value
            variable["valueSrc"] = "initialized"
            variable["isInput"] = False

        if isinstance(node.value, ast.Call):
            funcName = self.getFunctionName(node)
            variable["value"] = None
            variable["valueSrc"] = funcName
            variable["funcArgs"] = []

            if(funcName == "input"):
                variable["isInput"] = True
                self.inputs.append(variable["name"])
            else:
                variable["isInput"] = False

            for arg in node.value.args:
                variable["funcArgs"].append(arg.id)

        # self.getFunctionName(node)

        self.statements.append(variable)
        self.generic_visit(node)



    def visit_Expr(self, node):
        funcCall = {}
        funcCall["type"] = "function_call"
        funcCall["line"] = node.lineno

        if isinstance(node.value.func, ast.Name):
            funcCall["name"] = node.value.func.id
        elif isinstance(node.value.func,ast.Attribute):
            funcCall["name"] = node.value.func.value.id+'.'+node.value.func.attr

        funcCall["args"] = []
        for arg in node.value.args:
            funcCall["args"].append(arg.value)
        funcCall["hasInputs"] = False

        self.statements.append(funcCall)
        self.generic_visit(node)



    def getFunctionName(self, node):

        for fieldname, value in ast.iter_fields(node.value):

            if(fieldname == "func"):
                if isinstance(value, ast.Name):
                    return value.id
                elif isinstance(value, ast.Attribute):
                    funcName = self.functionAttr(value)
                    if value.attr:
                        funcName = funcName+'.'+value.attr

                    return funcName


    def functionAttr(self, node):
        name = None
        attr = None

        for field, value in ast.iter_fields(node):
            
            if isinstance(value, ast.Attribute):
                attr = value.attr
                name = self.functionAttr(value)
            
            if isinstance(value, ast.Name):
                name = value.id
        
        if attr:
            name = name+'.'+attr

        return(name)



    def report(self):
        for statement in self.statements:
            print(statement)

        for user_input in self.inputs:
            print("user input: "+user_input)

        f = open("editor.txt", "w")
        for statement in self.statements:
            json.dump(statement, f)
            f.write("\n")
        f.close()


    def findUserInputInFunction(self):
        for statement in self.statements:
            if statement["type"] == "function_call":
                for arg in statement["args"]:
                    if arg in self.inputs:
                        statement["hasInputs"] = True
                        break

                    for user_input in self.inputs:
                        if user_input in str(arg):
                            statement["hasInputs"] = True
                            break


def main():
    srcFile = open('src.py', 'r')
    srcCode = srcFile.read()
    # print(type(srcCode))

    tree = ast.parse(srcCode, type_comments=True)

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.findUserInputInFunction()
    analyzer.report()

    # print(ast.dump(tree,include_attributes=True))


if __name__ == "__main__":
    main()
