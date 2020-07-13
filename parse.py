import ast
import json

class Analyzer(ast.NodeVisitor):

    def __init__(self):
        self.inputs = []
        self.statements = []

    ######################### Import Modules Block Here #########################
    def visit_Import(self, node):
        
        for name in node.names:

            module = {}
            module["type"] = "import"
            module["line"] = node.lineno
            module["og"] = name.name
            module["alias"] = name.asname if name.asname else None

            self.statements.append(module)
        self.generic_visit(node)


    def visit_ImportFrom(self, node):
        
        for name in node.names:

            member = {}
            member["type"] = "import"
            member["line"] = node.lineno
            member["og"] = node.module +'.'+ name.name if name.name !="*" else node.module
            member["alias"] = node.module +'.'+ name.asname if name.asname else None

            self.statements.append(member)
        self.generic_visit(node)


    ######################### Function Definitions Here #########################
    def visit_FunctionDef(self, node):
        
        func_def = {}

        func_def["type"] = "function_def"
        func_def["line"] = node.lineno
        func_def["name"] = node.name
        func_def["args"] = []
        func_def["defaults"] = []

        for arg in node.args.args:
            if isinstance(arg, ast.arg): func_def["args"].append(arg.arg)
        
        for default in node.args.defaults:
            if isinstance(default, ast.Constant): func_def["defaults"].append(default.value) 
            elif isinstance(default,ast.Call): func_def["defaults"].append(default.func.id)
            elif isinstance(default, ast.BinOp):
                usedVars = self.getUsedVariablesInVariableDeclaration(default)
                func_def["defaults"].append(self.buildNewVariableValueFromUsedOnes(usedVars))

        for item in node.body:
            if isinstance(item,ast.Return):
                if isinstance(item.value,ast.Constant):
                    func_def["return"] = item.value.value
                
                elif isinstance(item.value, ast.BinOp):
                    usedVars = self.getUsedVariablesInVariableDeclaration(item.value)
                    func_def["return"] = self.buildNewVariableValueFromUsedOnes(usedVars)

                elif isinstance(item.value,ast.Call): func_def["return"] = item.value.func.id

        self.statements.append(func_def)
        self.generic_visit(node)


    ######################### Variable And List Assign Block Here #########################

    def visit_Assign(self, node):
        
        for target in node.targets:
            
            variable = {}
            variable["type"] = "variable"
            variable["line"] = node.lineno
        
            if isinstance(target,ast.Name):
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
                variable["args"] = []

                if(funcName == "input"):
                    variable["isInput"] = True
                    self.inputs.append(variable["name"])
                
                else: variable["isInput"] = False

                for arg in node.value.args:
                    if isinstance(arg,ast.Constant): variable["args"].append(arg.value)
                    elif isinstance(arg,ast.Name): variable["args"].append(self.getValueFromVariableName(arg.id))
                    elif isinstance(arg, ast.Attribute): 
                        
                        variable["args"].append(self.functionAttr(arg)+'.'+arg.attr)

                        funcObj = {}
                        funcObj["type"] = "function_obj"
                        funcObj["line"] = node.lineno
                        funcObj["objName"] = variable["name"]
                        funcObj["funcName"] = variable["valueSrc"]
                        funcObj["args"] = variable["args"]

                        if(funcObj not in self.statements):self.statements.append(funcObj)

            elif isinstance(node.value, ast.List):
                variable["type"] = "list"
                variable["values"] = []
                
                for value in node.value.elts:
                    if isinstance(value,ast.Constant):
                        variable["values"].append(value.value)

            self.statements.append(variable)
        self.generic_visit(node)



    ######################### If Comparasion Block Here #########################
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


    ######################### Try Block Here #########################

    def visit_Try(self, node):
        
        statement = {}
        statement["type"] = "except_statement"
        print(ast.dump(node))

        if isinstance(node, ast.Try):
            
            if isinstance(node.handlers[0].body[0],ast.Continue):
                statement["line"] = node.handlers[0].body[0].lineno
                statement["firstBlock"] = "continue"

            elif isinstance(node.handlers[0].body[0],ast.Pass): 
                statement["line"] = node.handlers[0].body[0].lineno
                statement["firstBlock"] = "pass"

            elif isinstance(node.handlers[0].body[0], ast.Expr):
                statement["line"] = node.handlers[0].body[0].lineno
                statement["firstBlock"] = "expression"

        self.statements.append(statement)
        self.generic_visit(node)


    ######################### Expressions Block Here #########################

    def visit_Expr(self, node):
        
        funcCall = {}
        funcCall["type"] = "function_call"
        funcCall["line"] = node.lineno
        
        # print(node.lineno)
        # print(ast.dump(node))

        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name): funcCall["name"] = node.value.func.id
            elif isinstance(node.value.func,ast.Call): funcCall["name"] = self.getFunctionName(node)
            elif isinstance(node.value.func,ast.Attribute): funcCall["name"] = self.getFunctionNameFromObject(self.getFunctionName(node))


            funcCall["args"] = []
            
            for arg in node.value.args:
                
                if isinstance(arg,ast.Name):
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
    


    ######################### Utility Function Here #########################

    def getValueFromVariableName(self,name):
        for statement in self.statements:
            if statement["type"] == "variable" and statement["name"] == name : return statement["value"]
        return name



    def valueOfFuncArguments(self,arg):
        for statement in self.statements:
            if statement["type"] == "variable" and statement["name"] == arg:
                return statement["value"]
        return None


    def getFunctionNameFromObject(self,name):
        
        fName = name.split('.')[0]
        lName = name.split('.')[1]

        for statement in self.statements:
            if statement["type"] == "function_obj" and fName == statement["objName"]: return statement["funcName"]+'.'+lName
        return name


    def getFunctionReturnValueFromName(self,funcName):

        for statement in self.statements:
            if statement["type"] == "function_def":
                if statement["name"] == funcName:
                    if statement.__contains__("return"): return statement["return"]
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
                # print(statement)        
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
                    if value.attr and funcName: funcName = funcName +'.'+ value.attr
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


    def printStatements(self):
        for statement in self.statements:
            print(statement)
        
        self.writeToFile()


    def printUserInputs(self):
        for user_input in self.inputs:
            print("user input: "+user_input)


    def writeToFile(self):
        f = open("tokens.txt", "w")
        
        for statement in self.statements:
            json.dump(statement, f)
            f.write("\n")
        
        f.close()

    