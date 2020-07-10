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

        for item in node.body:
            
            if isinstance(item,ast.Return):
                if isinstance(item.value,ast.Constant):
                    func_def["returnValue"] = item.value.value
                
                elif isinstance(item.value, ast.BinOp):
                    usedVars = self.getUsedVariablesInVariableDeclaration(item.value)
                    hasInputs = self.checkUserInputsInVariableDeclaration(usedVars)
                    func_def["returnValue"] = self.buildNewVariableValueFromUsedOnes(usedVars)
            
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

        elif isinstance(node.value, ast.BinOp):
            usedVars = self.getUsedVariablesInVariableDeclaration(node.value)
            hasInputs = self.checkUserInputsInVariableDeclaration(usedVars)

            if hasInputs:
                self.inputs.append(variable["name"])
                variable["value"] = None
                variable["valueSrc"] = "input"
                variable["isInput"] = True
            
            else:
                variable["value"] = self.buildNewVariableValueFromUsedOnes(usedVars)
                variable["valueSrc"] = "initialized"
                variable["isInput"] = False


        elif isinstance(node.value, ast.Call):
            funcName = self.getFunctionName(node)
            variable["value"] = None
            variable["valueSrc"] = funcName
            variable["funcArgs"] = []

            if(funcName == "input"):
                variable["isInput"] = True
                self.inputs.append(variable["name"])
            
            else: variable["isInput"] = False

            for arg in node.value.args:
                variable["funcArgs"].append(arg.id)

        elif isinstance(node.value, ast.List):
            
            variable["type"] = "list"
            variable["values"] = []
            
            for value in node.value.elts:
                if isinstance(value,ast.Constant):
                    variable["values"].append(value.value)

        self.statements.append(variable)
        self.generic_visit(node)


    def visit_If(self,node):
        
        statement = {}
        statement["type"] = "comparison"
        statement["line"] = node.lineno
        statement["pairs"] = []

        if isinstance(node.test,ast.BoolOp):
            for compare in node.test.values:

                if isinstance(compare.left,ast.Name) and isinstance(compare.ops[0],ast.Eq) and isinstance(compare.comparators[0],ast.Constant):
                    pair = []
                    pair.append(compare.left.id)
                    pair.append(compare.comparators[0].value)

                    statement["pairs"].append(pair)
                
                elif isinstance(compare.left,ast.Name) and isinstance(compare.ops[0],ast.Eq) and isinstance(compare.comparators[0],ast.BinOp):
                    pair = []
                    pair.append(compare.left.id)
                    
                    usedVars = self.getUsedVariablesInVariableDeclaration(compare.comparators[0])
                    value = self.buildNewVariableValueFromUsedOnes(usedVars)
                    
                    pair.append(value.lstrip())
                    statement["pairs"].append(pair)
                
        elif isinstance(node.test,ast.Compare):
            
            pair = []

            if isinstance(node.test.left,ast.Constant): pair.append(node.test.left.value)
            elif isinstance(node.test.left,ast.Name): pair.append(node.test.left.id)

            for comparator in node.test.comparators:
                if isinstance(comparator,ast.Constant): pair.append(comparator.value)
                elif isinstance(comparator,ast.Name): pair.append(comparator.id)

            statement["pairs"].append(pair)    
        
        self.statements.append(statement)
        self.generic_visit(node)

    def visit_Try(self, node):
        
        statement = {}
        statement["type"] = "except_statement"

        if isinstance(node, ast.Try):
            
            if isinstance(node.handlers[0].body[0],ast.Continue):
                statement["line"] = node.handlers[0].body[0].lineno
                statement["arg"] = "continue"

            elif isinstance(node.handlers[0].body[0],ast.Pass): 
                statement["line"] = node.handlers[0].body[0].lineno
                statement["arg"] = "pass"

        self.statements.append(statement)
        self.generic_visit(node)




    def valueOfFuncArguments(self,arg):
        for statement in self.statements:
            if statement["type"] == "variable" and statement["name"] == arg:
                return statement["value"]
        return None


    def visit_Expr(self, node):
        # print('expression '+ast.dump(node))
        
        funcCall = {}
        funcCall["type"] = "function_call"
        funcCall["line"] = node.lineno
        
        if isinstance(node.value.func, ast.Name): funcCall["name"] = node.value.func.id
        elif isinstance(node.value.func,ast.Call): funcCall["name"] = self.getFunctionName(node)
        elif isinstance(node.value.func,ast.Attribute): funcCall["name"] = self.getFunctionName(node)

        funcCall["args"] = []
        
        for arg in node.value.args:
            
            if isinstance(arg,ast.Name):

                # print(ast.dump(arg))
                if self.valueOfFuncArguments(arg.id): funcCall["args"].append(self.valueOfFuncArguments(arg.id)) 
                else: funcCall["args"].append(arg.id)

            elif isinstance(arg,ast.Constant): funcCall["args"].append(arg.value)
            elif isinstance(arg,ast.Attribute): funcCall["args"].append(self.functionAttr(arg)+'.'+arg.attr)
            elif isinstance(arg,ast.BinOp):
                
                usedArgs = self.getUsedVariablesInVariableDeclaration(arg)
                actualValue = self.buildNewVariableValueFromUsedOnes(usedArgs)
                funcCall["args"].append(actualValue)

            elif isinstance(arg, ast.Call):
                func = arg.func.id
                funcCall["args"].append(self.getFunctionReturnValueFromName(func))
                
        funcCall["keywords"] = []
        funcCall["hasInputs"] = False
        
        for keyword in node.value.keywords:
            karg = keyword.arg
            kvalue = None

            if isinstance(keyword.value,ast.Constant): kvalue = keyword.value.value
            if karg and kvalue: funcCall["keywords"].append([karg,kvalue])


        self.statements.append(funcCall)
        self.generic_visit(node)
    


    def getFunctionReturnValueFromName(self,funcName):

        for statement in self.statements:
            if statement["type"] == "function_def":
                if statement["name"] == funcName:
                    if statement.__contains__("returnValue"): return statement["returnValue"]
                    else: return None
        return funcName


    def getOperandsFromBinOp(self,node,usedVars):
        if isinstance(node, ast.Name) and node.id: usedVars.append(node.id)
        elif isinstance(node, ast.Constant) and node.value: usedVars.append(node.value)
        
        elif isinstance(node,ast.BinOp):  
            usedVars = self.getOperandsFromBinOp(node.left,usedVars)  
            usedVars = self.getOperandsFromBinOp(node.right,usedVars)

        return usedVars     
        
    def getUsedVariablesInVariableDeclaration(self,node):
        
        usedVariables = []
        for field, value in ast.iter_fields(node):
            self.getOperandsFromBinOp(value,usedVariables)
                
        return usedVariables


    def buildNewVariableValueFromUsedOnes(self,usedVariables):
        
        value = None
        
        for variable in usedVariables:
            
            found = False
            for statement in self.statements:
                
                if statement["type"] == "variable" and statement["name"] == variable:
                    
                    if statement["isInput"] != True and value:
                        if type(value) == str or type(statement["value"]) == str: value = str(value) + str(statement["value"])
                        else: value = value + statement["value"]

                    elif statement["isInput"] != True: value = statement["value"]
                    elif statement["isInput"] == True: value = str(value) + "input"

                    found = True
                    break

            if found == False and value: value = value + variable
            elif found == False: value = variable

        return value



    def getFunctionName(self, node):

        for fieldname, value in ast.iter_fields(node.value):
            # print(fieldname)
            # print(ast.dump(value))

            if(fieldname == "func"):
                if isinstance(value, ast.Name): return value.id
                
                elif isinstance(value, ast.Attribute):    
                    funcName = self.functionAttr(value)
                    if value.attr: funcName = funcName +'.'+ value.attr
                    return funcName


    def functionAttr(self, node):
        name = None
        attr = None

        for field, value in ast.iter_fields(node):
            
            if isinstance(value, ast.Attribute):
                attr = value.attr
                name = self.functionAttr(value)
            
            elif isinstance(value, ast.Name): name = value.id
            elif isinstance(value,ast.Call): name = self.functionAttr(value)
        
        if attr: name = name+'.'+attr
        return(name)


    def checkUserInputsInVariableDeclaration(self, usedVariables):
        for variable in usedVariables:
            if variable in self.inputs:
                return True

        return False


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


    def report(self):
        for statement in self.statements:
            print(statement)

        print('')
        # for user_input in self.inputs:
        #     print("user input: "+user_input)

        f = open("tokens.txt", "w")
        for statement in self.statements:
            json.dump(statement, f)
            f.write("\n")
        f.close()
