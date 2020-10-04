import ast
import sys   
import json
import time

from operations.save_token_exceptions import save_token_for_bug_fix
from operations.save_token_exceptions import save_token_parsing_exception

class Analyzer(ast.NodeVisitor):

    def __init__(self):
        self.inputs = []
        self.statements = []
        

    ######################### Import Modules Block Here #########################
    def visit_Import(self, node):
        try: 
            for name in node.names:

                module = {}
                module["type"] = "import"
                module["line"] = node.lineno
                module["og"] = name.name
                module["alias"] = name.asname if name.asname else None
                self.statements.append(module)
        
        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node)


    def visit_ImportFrom(self, node):
        try:
            for name in node.names:

                member = {}
                member["type"] = "import"
                member["line"] = node.lineno

                if node.module is not None: member["og"] = node.module +'.'+ name.name if name.name !="*" else node.module
                else: member["og"] = name.name
                
                if node.module is not None: member["alias"] = node.module +'.'+ name.asname if name.asname else None
                else: member["alias"] = name.asname
                
                self.statements.append(member)
        
        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node)


    ######################### Function Definitions Here #########################
    def visit_FunctionDef(self, node):
        try:
            # print(ast.dump(node))

            func_def = {}
            func_def["type"] = "function_def"
            func_def["line"] = node.lineno
            func_def["name"] = node.name
            func_def["args"] = []
            func_def["defaults"] = []
            func_def["return"] = None

            for arg in node.args.args: 
                if isinstance(arg, ast.arg): func_def["args"].append(arg.arg)
            
            if isinstance(node.args.vararg, ast.arg): 
                func_def["args"].append(node.args.vararg.arg)
            
            elif isinstance(node.args.kwarg, ast.arg): 
                func_def["args"].append(node.args.kwarg.arg)
            
            for default in node.args.defaults:
                self.separate_variables(default,func_def["defaults"])

            for item in node.body:
                
                if isinstance(item,ast.Return):
                    func_def["return"] = self.separate_variables(item.value,[])
                    func_def["return"] = func_def["return"][0] if len(func_def["return"]) > 0 else None

                    if isinstance(item.value,ast.Call):
                        func_def["returnArgs"] = []
                        for arg in item.value.args:
                            func_def["returnArgs"] = self.separate_variables(arg, func_def["returnArgs"])
                            
                            for i in range(len(func_def["returnArgs"])):
                                if self.value_from_variable_name(func_def["returnArgs"][i])[0]: 
                                    func_def["returnArgs"][i] = self.value_from_variable_name(func_def["returnArgs"][i])[1]

                        for keyword in item.value.keywords:
                            func_def['returnKeywords'] = []
                            karg = keyword.arg
                            kvalue = None

                            if isinstance(keyword.value, ast.Constant): kvalue = keyword.value.value
                            if karg: func_def['returnKeywords'].append([karg,kvalue])

            self.statements.append(func_def)
     
        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node)


    ######################### Variable And List Assign Block Here #########################

    def visit_Assign(self, node):
        
        try:
            for target in node.targets:
                
                variable = {}
                variable["type"] = "variable"
                variable["line"] = node.lineno
                variable['name'] = None
                variable['value'] = None
                variable['valueSrc'] = 'initialization'
                variable['isInput'] = False
            
                if isinstance(target, ast.Name):
                    variable["name"] = target.id

                elif isinstance(target, ast.Subscript):
                    var = self.separate_variables(target.value, [])
                    variable["name"] = var[0] if len(var) > 0 else None
                    
                    varSlice = None
                    if isinstance(target.slice, ast.Index): 
                        varSlice = self.separate_variables(target.slice.value, [])
                        varSlice = varSlice[0] if len(varSlice) > 0 else None

                    elif isinstance(target.slice, ast.ExtSlice):
                        varSlice = self.separate_variables(target.slice.dims, [])
                        varSlice = varSlice[0] if len(varSlice) > 0 else None

                    elif isinstance(target.slice, ast.Slice):
                        lowerSlice = self.separate_variables(target.slice.lower, []) if target.slice.lower!= None else 'min'
                        upperSlice = self.separate_variables(target.slice.upper, []) if target.slice.upper!= None else 'max'
                        
                        if lowerSlice != 'min' and len(lowerSlice)>0: lowerSlice = lowerSlice[0]
                        if upperSlice != 'max' and len(upperSlice)>0: upperSlice = upperSlice[0]

                        varSlice = str(lowerSlice)+':'+str(upperSlice)
                        
                    if varSlice is not None and variable["name"] is not None:
                        variable["name"] = variable["name"]+'['+str(varSlice)+']'
                    
                    elif varSlice is None and variable["name"] is not None:
                        pass 
                    
                    elif varSlice is not None and variable["name"] is None: 
                        variable["name"] = '['+str(varSlice)+']'
                
                elif isinstance(target, ast.Tuple):
                    variable["type"] = "tuple"
                    variable["names"] = []

                    for element in target.elts:
                        names = self.separate_variables(element, [])
                        if len(names) > 0: variable["names"].append(names[0])
                
                elif isinstance(target, ast.Attribute):
    
                    name = self.get_function_attribute(target)
                    returns = self.get_value_src_from_variable_name(name)
                    if returns[0] is True: name = returns[1]

                    if name is not None and target.attr is not None: name = name +'.'+ target.attr
                    elif target.attr is None: variable["name"] = name
                    
                    # print('name: {name}'.format(name = name))
                    

                if isinstance(node.value, ast.Constant):
                    variable["value"] = node.value.value
                    variable["valueSrc"] = "initialization"
                    variable["isInput"] = False

                if isinstance(node.value, ast.Name):
                    value_from_variable_name = self.value_from_variable_name(node.value.id)
                    
                    if value_from_variable_name[0] is False:
                        variable['remove'] = True

                    else:
                        if type(value_from_variable_name[1]) == list: 
                            variable["type"] = "list"

                        elif type(value_from_variable_name[1]) == dict: 
                            variable["type"] = "dict"

                        elif type(value_from_variable_name[1]) == set: 
                            variable["type"] = "set"
                            
                        elif type(value_from_variable_name[1]) == tuple: 
                            variable["type"] = "tuple"
                        
                        variable["value"] = value_from_variable_name[1]
                        variable["valueSrc"] = "initialization"
                        variable["isInput"] = False

                
                elif isinstance(node.value, ast.BinOp):
                    usedVars = self.get_variables_used_in_declaration(node.value)
                    # print(usedVars)
                    hasInputs = self.search_input_in_declaration(usedVars)
                    # print(hasInputs)

                    if hasInputs is True:
                        self.inputs.append(variable["name"])
                        variable["value"] = None
                        variable["valueSrc"] = "input"
                        variable["isInput"] = True
                    
                    else:
                        variable["value"] = self.build_value_from_used_variables(usedVars)
                        variable["valueSrc"] = "initialization"
                        variable["isInput"] = False

                elif isinstance(node.value, ast.Call):
                    
                    funcName = self.get_function_name(node)
                    variable["value"] =  self.get_function_return_value(funcName) 
                    variable["valueSrc"] = funcName
                    variable["args"] = []
                    variable["isInput"] = False

                    input_functions = [ 'input', 'request.POST.get', 'request.GET.get', 'request.GET.getlist', 'request.POST.getlist',
                                        'self.request.POST.get', 'self.request.GET.get', 'self.request.GET.getlist', 'self.request.POST.getlist'
                                    ]

                    if funcName in input_functions:
                        variable["value"] = None
                        variable["isInput"] = True
                        self.inputs.append(variable["name"])
                    
                    for arg in node.value.args:
                        if isinstance(arg, ast.Attribute): 
                            
                            variable["args"].append(self.get_function_attribute(arg)+'.'+arg.attr)

                            funcObj = {}
                            funcObj["type"] = "function_obj"
                            funcObj["line"] = node.lineno
                            funcObj["objName"] = variable["name"]
                            funcObj["funcName"] = variable["valueSrc"]
                            funcObj["args"] = variable["args"]

                            if(funcObj not in self.statements):self.statements.append(funcObj)
                        
                        elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                            funcName = arg.func.id
                            variable['args'].append(funcName)
                            if funcName in input_functions:

                                variable['value'] = None
                                variable["valueSrc"] = funcName
                                variable['isInput'] = True
                        
                        elif isinstance(arg, ast.Call):

                            funcName = self.get_function_name(arg)
                            variable["isInput"] = False

                            input_functions = [ 'input', 'request.POST.get', 'request.GET.get', 'request.GET.getlist', 'request.POST.getlist',
                                                'self.request.POST.get', 'self.request.GET.get', 'self.request.GET.getlist', 'self.request.POST.getlist'
                                            ]

                            if funcName in input_functions:
                                variable["value"] = None
                                variable["valueSrc"] = funcName
                                variable["isInput"] = True
                                self.inputs.append(variable["name"])
                            


                        elif isinstance(arg, ast.Name):
                            name = arg.id
                            value = None
                            returns = self.value_from_variable_name(name) 
                            if returns[0] is True: value = returns[1]

                            isInput = self.search_input_in_declaration([name])
                            if isInput is True:
                                variable['value'] = None
                                variable['valueSrc'] = 'input'
                                variable['isInput'] = True

                            else:
                                if value is not None: variable["args"].append(value)
                                else:  variable["args"].append(name)

                        else: variable["args"] = (self.separate_variables(arg,variable["args"]))

                    for keyword in node.value.keywords:
                        variable['funcKeywords'] = []
                        karg = keyword.arg
                        kvalue = None

                        if isinstance(keyword.value, ast.Constant): kvalue = keyword.value.value
                        elif isinstance(keyword.value, ast.Name): 
                            kvalue = keyword.value.id
                            returns = self.value_from_variable_name(kvalue) 
                            if returns[0] is True: kvalue = returns[1]

                            isInput = self.search_input_in_declaration([keyword.value.id])
                            if isInput is True:
                                variable['value'] = None
                                variable['valueSrc'] = 'input'
                                variable['isInput'] = True
                        
                        if karg is not None: 
                            variable['funcKeywords'].append([karg,kvalue])



                elif isinstance(node.value, ast.List):
                    variable["type"] = "list"
                    variable["values"] = []
                    
                    variable["valueSrc"] = 'initialization'
                    variable["isInput"] = False
                    
                    for value in node.value.elts:
                        variable["values"] = self.separate_variables(value,variable["values"])

                elif isinstance(node.value, ast.Dict):
                    variable["type"] = "dict"
                    variable["keys"] = []
                    variable["values"] = []

                    for key in node.value.keys:
                        keyList = self.separate_variables(key,[])
                        if len(keyList) > 0: variable["keys"].append(keyList[0]) 
                    
                    for value in node.value.values:
                        valueList = self.separate_variables(value, [])
                        if len(valueList) > 0: variable["values"].append(valueList[0])
                
                elif isinstance(node.value,ast.Tuple):
                    variable["type"] = "tuple"
                    variable["values"] = []

                    for element in node.value.elts:
                        values = self.separate_variables(element, [])
                        if len(values)>0: variable["values"].append(values[0])
                    

                elif isinstance(node.value,ast.Set):
                    variable["type"] = "set"
                    variable["values"] = []
                    
                    for element in node.value.elts:    
                        values = self.separate_variables(element, [])
                        if len(values)>0: variable["values"].append(values[0])
                    
                elif isinstance(node.value, ast.IfExp):
                    # variable["type"] = "variable" overriding previous type (var , tuple , set etc)
                    variable["values"] = []

                    bodyList = self.separate_variables(node.value.body,[])
                    if len(bodyList) > 0: variable["values"].append(bodyList[0])

                    comparatorList = self.separate_variables(node.value.orelse, [])
                    if len(comparatorList) > 0: variable["values"].append(comparatorList[0])

                elif isinstance(node.value, ast.BoolOp):
                    variable["values"] = []
                    for value in node.value.values:
                        valueList = self.separate_variables(value,[])
                        if len(valueList) > 0: variable["values"].append(valueList[0])
                
                elif isinstance(node.value, ast.Subscript):
                    value = self.separate_variables(node.value.value, [])
                    variable["value"] = value[0] if len(value) > 0 else None
                    variable["value"] = self.value_from_variable_name(variable['value'])[1]

                    if isinstance(node.value.slice, ast.Slice):
                        lowerSlice = self.separate_variables(node.value.slice.lower, []) if node.value.slice.lower!= None else 'min'
                        upperSlice = self.separate_variables(node.value.slice.upper, []) if node.value.slice.upper!= None else 'max'
                        
                        if lowerSlice != 'min' and len(lowerSlice) > 0: lowerSlice = lowerSlice[0]
                        if upperSlice != 'max' and len(upperSlice) > 0: upperSlice = upperSlice[0]

                        varSlice = str(lowerSlice)+':'+str(upperSlice)
                        
                        if type(value) == list and type(lowerSlice) == int and type(upperSlice) == int:
                            variable["value"] = variable["value"][lowerSlice:upperSlice]
                        
                        elif type(value) == list and type(lowerSlice) == int and type(upperSlice) == str:
                            variable["value"] = variable["value"][lowerSlice:]
                        elif variable['value'] != None and type(value) == list and type(lowerSlice) == str and type(upperSlice) == int:
                            variable["value"] = variable["value"][:upperSlice]
                        elif type(value) == list and type(lowerSlice) == str and type(upperSlice) == str:
                            variable["value"] = variable["value"]
                        elif varSlice != None and variable["value"]!= None:
                            variable["value"] = variable["value"]+'['+str(varSlice)+']'
                        else: variable["value"] = '['+str(varSlice)+']'

                elif isinstance(node.value, ast.Attribute):
                    attr = self.get_function_attribute(node.value)+'.'+node.value.attr if node.value.attr else self.get_function_attribute(node.value) 
                    returns = self.value_from_variable_name(attr)
                    variable["value"] = returns[1] if returns[0] is True else attr
                    if returns[0] is False:
                        variable['remove'] = True


                if variable.__contains__('remove') is False:
                    self.statements.append(variable)
 
        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node)


    ######################### If Comparasion Block Here #########################
    def visit_If(self,node):
        try:
            
            statement = {}
            statement["type"] = "comparison"
            statement["line"] = node.lineno
            statement["pairs"] = []
            
            if isinstance(node.test, ast.BoolOp):
                for value in node.test.values:
                    
                    if isinstance(value, ast.Compare):
                        
                        if isinstance(value.left, ast.Name) and isinstance(value.comparators[0], ast.Constant):
                            statement["pairs"].append([value.left.id, value.comparators[0].value])
                        
                        elif isinstance(value.left, ast.Constant) and isinstance(value.comparators[0], ast.Name):
                            statement["pairs"].append([value.comparators[0].id, value.left.value])
                        
                        elif isinstance(value.left, ast.Name) and isinstance(value.comparators[0], ast.Name):
                            left_var = value.left
                            right_var = value.comparators[0]

                            value_of_right_var = self.value_from_variable_name(right_var)
                    
                            if value_of_right_var[0] is True:
                                if isinstance(value_of_right_var[1], list):
                                    for value in value_of_right_var[1]:
                                        statement['pairs'].append([left_var, value])
                                
                                else: statement['pairs'].append([left_var, value_of_right_var[1]])
                            
                            else:
                                value_of_left_var = self.value_from_variable_name(left_var)
                                if value_of_left_var[0] is True: 
                                    statement['pairs'].append([right_var, value_of_left_var[1]])

        
            elif isinstance(node.test, ast.Compare):
                
                if isinstance(node.test.left, ast.Name) and isinstance(node.test.comparators[0], ast.Name):
                    
                    left_var = node.test.left.id
                    right_var = node.test.comparators[0].id
                    value_of_right_var = self.value_from_variable_name(right_var)
                    
                    if value_of_right_var[0] is True:
                        if isinstance(value_of_right_var[1], list):
                            for value in value_of_right_var[1]:
                                statement['pairs'].append([left_var, value])
                        
                        else: statement['pairs'].append([left_var, value_of_right_var[1]])
                    
                    else:
                        value_of_left_var = self.value_from_variable_name(left_var)
                        if value_of_left_var[0] is True: 
                            statement['pairs'].append([right_var, value_of_left_var[1]])


                elif isinstance(node.test.left, ast.Name) and isinstance(node.test.comparators[0], ast.Constant):
                    statement["pairs"].append([node.test.left.id, node.test.comparators[0].value])

                elif isinstance(node.test.left, ast.Constant) and isinstance(node.test.comparators[0], ast.Name):
                    statement["pairs"].append([node.test.comparators[0].id, node.test.left.value])

            if len(statement['pairs']) > 0:
                self.statements.append(statement)
        
        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node)


    ######################### Try Block Here #########################

    def visit_Try(self, node):
        try:
            statement = {}
            statement["type"] = "exception_handle"
            # print(ast.dump(node))
            should_include_in_statements = False

            if isinstance(node, ast.Try):
                # print(ast.dump(node.handlers[0].body[0]))
                # print(type(node.handlers[0].body[0]))
                
                if len(node.handlers) > 0:    
                    if isinstance(node.handlers[0].body[0],ast.Continue):
                        statement["line"] = node.handlers[0].body[0].lineno
                        statement["exceptionHandler"] = "continue"
                        should_include_in_statements = True

                    elif isinstance(node.handlers[0].body[0],ast.Pass): 
                        statement["line"] = node.handlers[0].body[0].lineno
                        statement["exceptionHandler"] = "pass"
                        should_include_in_statements = True

                    else:
                        statement["line"] = node.handlers[0].body[0].lineno
                        statement["exceptionHandler"] = "expression"
                        should_include_in_statements = True

                elif len(node.finalbody) > 0:
                    if isinstance(node.finalbody[0],ast.Continue):
                        statement["line"] = nodenode.finalbody[0].lineno
                        statement["exceptionHandler"] = "continue"
                        should_include_in_statements = True
                    

                    elif isinstance(node.finalbody[0],ast.Pass): 
                        statement["line"] = node.finalbody[0].lineno
                        statement["exceptionHandler"] = "pass"
                        should_include_in_statements = True

                    else:
                        statement["line"] = node.finalbody[0].lineno
                        statement["exceptionHandler"] = "expression"
                        should_include_in_statements = True

            if should_include_in_statements is True:
                self.statements.append(statement)

        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node)


    ######################### Expressions Block Here #########################

    def visit_Expr(self, node):
        try:
            expression = {}
            expression["type"] = "function_call"
            expression["line"] = node.lineno
            expression["name"] = None
            expression["args"] = []
            expression["keywords"] = []
            expression["hasInputs"] = False
                
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name): expression["name"] = node.value.func.id
                elif isinstance(node.value.func,ast.Call): expression["name"] = self.get_function_name(node)
                elif isinstance(node.value.func,ast.Attribute): expression["name"] = self.get_function_name_from_object(self.get_function_name(node))
    
                # separating args in function call
                for arg in node.value.args:
                    expression["args"] = self.separate_variables(arg,expression["args"])
                    
                # print(expression['args'])
                hasInputs = self.search_input_in_declaration(expression['args'])
                if hasInputs is True: expression["hasInputs"] = True

                # getting args value from name in function call
                for i in range(len(expression['args'])): 
                    returns = self.value_from_variable_name(expression['args'][i])
                    expression['args'][i] = returns[1] 
                
                for keyword in node.value.keywords:
                    karg = keyword.arg
                    kvalue = None

                    if isinstance(keyword.value, ast.Constant): kvalue = keyword.value.value
                    if karg: expression["keywords"].append([karg,kvalue])

                self.statements.append(expression)

        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node)
    

    ######################### Assert Here #########################

    def visit_Assert(self, node):
        try:
            # print(ast.dump(node))
            
            assertStatement = {}
            assertStatement["type"] = "assert"
            assertStatement["line"] = node.lineno
                
            if isinstance(node.test, ast.Compare):
                left = self.separate_variables(node.test.left, [])
                left = left[0] if len(left) > 0 else None

                comparators = []
                for comparator in node.test.comparators:
                    name = self.separate_variables(comparator, [])
                    name = name[0] if len(name)>0 else None
                    
                    if name is not None: comparators.append(name)
                
                assertStatement["left"] = left
                assertStatement["comparators"] = comparators

            elif isinstance(node.test, ast.Call):
                funcName = self.separate_variables(node.test, [])
                funcName = funcName[0] if len(funcName) > 0 else None
                funcArgs = []
                
                for arg in node.test.args:
                    funcArgs = self.separate_variables(arg, funcArgs)

                assertStatement['func'] = funcName
                assertStatement['args'] = funcArgs

            self.statements.append(assertStatement)

        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

        self.generic_visit(node) 

            
    ######################### Utility Function Here #########################
    def separate_variables(self,node,itemList):
        try:
            if isinstance(node,ast.Name): itemList.append(node.id) 
            elif isinstance(node,ast.Constant): itemList.append(node.value)
            elif isinstance(node,ast.Attribute): itemList.append(self.get_function_attribute(node)+'.'+node.attr)
            elif isinstance(node,ast.FormattedValue): itemList = self.separate_variables(node.value, itemList)
            
            elif isinstance(node,ast.BinOp):    
                usedArgs = self.get_variables_used_in_declaration(node)
                for arg in usedArgs:
                    itemList.append(arg)
                # actualValue = self.build_value_from_used_variables(usedArgs)
            
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name): itemList.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    func = self.get_function_attribute(node.func)
                    if node.func.attr and func: func = func +'.'+ node.func.attr
                    itemList.append(func)

                    for arg in node.args:
                        itemList = self.separate_variables(arg, itemList)
            
            elif isinstance(node, ast.List):
                if len(node.elts) == 0: itemList.append(None)
                for element in node.elts:
                    itemList = self.separate_variables(element,itemList)

            
            elif isinstance(node, ast.JoinedStr):
                for value in node.values:
                    itemList = self.separate_variables(value, itemList)

            elif isinstance(node, ast.Lambda): itemList = self.separate_variables(node.body, itemList)
            
            elif isinstance(node, ast.Subscript):

                varSlice = None
                itemList = self.separate_variables(node.value, itemList)
                # print(ast.dump(node))

                if isinstance(node.slice, ast.Index): 
                    varSlice = self.separate_variables(node.slice.value, [])
                    varSlice = varSlice[0] if len(varSlice) > 0 else None

                elif isinstance(node.slice, ast.ExtSlice):
                    varSlice = self.separate_variables(node.slice.dims, [])
                    varSlice = varSlice[0] if len(varSlice) > 0 else None

                if itemList == None: pass
                elif varSlice == None and len(itemList) > 0: pass 
                elif varSlice != None and len(itemList) > 0: itemList[0] = str(itemList[-1])+'['+str(varSlice)+']'

            elif isinstance(node, ast.Tuple):
                for elt in node.elts:
                    itemList = self.separate_variables(elt, itemList)

            return itemList

        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)

    def refine_tokens(self):
        for statement in self.statements:
            try:
                if statement["type"] == "variable" and statement.__contains__("names") and statement.__contains__("values"):
                    for name in statement["names"]:

                        variable = {}
                        variable["type"] = "variable"
                        variable["line"] = statement["line"]
                        variable["name"] = name
                        
                        index = statement["names"].index(name)

                        if len(statement['values']) != 0 and index < len(statement["values"]): variable["value"] = statement["values"][index] 
                        elif statement.__contains__("value") is True: variable["value"] = statement["value"]
                        else: variable["value"] = None

                        variable["valueSrc"] = statement["valueSrc"] if statement.__contains__("valueSrc") else "initialization"
                        variable["args"] = statement["args"] if statement.__contains__('args') else []
                        variable["isInput"] = statement["isInput"] if statement.__contains__("isInput") else False
                        
                        self.statements.append(variable)

                    self.statements.remove(statement)
                    print('statement not deleted yet!') if statement in self.statements else print('statement is deleted!')
                    # time.sleep(2)

                elif statement["type"] == "variable" and statement.__contains__("names") and statement.__contains__("valueSrc") and statement.__contains__('args'):
                    for name in statement["names"]:

                        variable = {}
                        variable["type"] = "variable"
                        variable["line"] = statement["line"]
                        variable["name"] = name
                        variable["value"] = None
                        variable["valueSrc"] = statement["valueSrc"] if statement.__contains__("valueSrc") else "initialization"
                        variable["args"] = statement["args"]
                        variable["isInput"] = statement["isInput"] if statement.__contains__("isInput") else False
                        
                        self.statements.append(variable)

                    self.statements.remove(statement)
                    print('statement not deleted yet!') if statement in self.statements else print('statement is deleted!')
                    # time.sleep(2)

                elif statement['type'] == 'tuple' and statement.__contains__("names") and statement.__contains__("values"):
                    for i in  range(0, len(statement['names'])):
                        variable = {}
                        variable["type"] = "variable"
                        variable["line"] = statement["line"]
                        variable["name"] = statement['names'][i]
                        variable["value"] = statement['values'][i] if i < len(statement['values']) else statement['values'][0]
                        variable["valueSrc"] = statement["valueSrc"] if statement.__contains__("valueSrc") else "initialization"
                        if statement.__contains__("args"): variable["args"] = statement["args"] 
                        variable["isInput"] = statement["isInput"] if statement.__contains__("isInput") else False
                        
                        self.statements.append(variable)
                    self.statements.remove(statement)

                elif statement["type"] == "function_def" and statement.__contains__("return") is False: 
                    self.statements.remove(statement)
                    print('statement not deleted yet!') if statement in self.statements else print('statement is deleted!')
                    # time.sleep(2)
                    
            except Exception as error:
                line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
                save_token_parsing_exception(str(error), line_number)


    def make_tokens_byte_free(self):
        for statement in self.statements:
            for item in statement:
                if isinstance(item, bytes): 
                    try: statement[item] = statement[item].decode('utf-8')
                    except: pass

    def value_from_variable_name(self,name):
        for statement in reversed(self.statements):
            if statement["type"] == "variable" and statement["name"] == name:
                return [True, statement["value"]] if statement.__contains__("value") and statement['value'] is not None else [False, name]
            
            elif statement["type"] == "list" and statement["name"] == name: 
                return [True, statement["values"]] if statement.__contains__("values") else [False, name]
            
        return [False, name]


    def get_function_name_from_object(self,name):
        fName = None
        for part in name.split('.')[0:-1]:
            fName = fName +'.'+ part if fName is not None else part
            
        lName = name.split('.')[-1]

        for statement in self.statements:
            if statement["type"] == "function_obj" and fName == statement["objName"]: return statement["funcName"]+'.'+lName
        return name


    def get_function_return_value(self,funcName):

        for statement in self.statements:
            if statement["type"] == "function_def" and statement["name"] == funcName:
                return statement["return"] if statement.__contains__("return") and statement["return"] is not None else None 
                
        return None


    def get_operands_from_bin_operation(self,node,usedVars):
        if isinstance(node, ast.Name) and node.id: usedVars.append(node.id)
        elif isinstance(node, ast.Constant) and node.value: usedVars.append(node.value)
        elif isinstance(node, ast.Call): 
            if isinstance(node.func, ast.Name): usedVars.append(node.func.id)
            elif isinstance(node.func, ast.Attribute): usedVars.append(self.get_function_name(node.func))
        
        elif isinstance(node,ast.BinOp): 
            usedVars = self.get_operands_from_bin_operation(node.left,usedVars)  
            usedVars = self.get_operands_from_bin_operation(node.right,usedVars)

        elif isinstance(node, ast.Tuple):
            for item in node.elts:
                self.get_operands_from_bin_operation(item, usedVars)
        return usedVars     
        

    def get_variables_used_in_declaration(self,node):
        usedVariables = []
        for field, value in ast.iter_fields(node):
            self.get_operands_from_bin_operation(value,usedVariables)
                
        return usedVariables


    def build_value_from_used_variables(self,usedVariables):
        try:
            value = None
            for variable in usedVariables:    
                
                matched = False
                for statement in self.statements:
                    
                    if statement["type"] == "variable" and statement["name"] == variable and statement.__contains__("isInput"):
                        
                        if statement["isInput"] == False and value != None:
                            if value == None: value = statement['value']
                            elif statement['value'] == None: pass

                            elif type(value) == str or type(statement["value"]) == str: value = str(value) + str(statement["value"])
                            else: value = value + statement["value"]

                        elif statement["isInput"] != True: value = statement["value"]
                        elif statement["isInput"] == True: value = str(value) + "input"

                        matched = True
                        break
                    
                    elif statement["type"] == "function_def" and statement["name"] == variable:
                        if statement.__contains__("return"): 
                            
                            if type(value) == str or type(statement["return"]) == str: value = str(value) + str(statement["return"])
                            elif value == None: value = statement["return"]
                            else : 
                                if type(value) == str or type(statement['return']) == str: value = str(value) + str(statement["return"])
                                elif type(value) == type(statement['return']): value = value + statement['return']

                            matched = True
                            break

                if isinstance(value, bytes): 
                    value = value.decode('utf-8')

                elif isinstance(variable, bytes):
                    variable = variable.decode('utf-8')
                
                if matched == False and value and variable and (type(value) != str and type(variable) != str): value = value + variable
                elif matched == False and value and variable and (type(value) == str or type(variable) == str): value = str(value) + str(variable)
                elif matched == False and variable: value = variable

            return value

        except Exception as error:
            line_number = "Error on line {}".format(sys.exc_info()[-1].tb_lineno)
            save_token_parsing_exception(str(error), line_number)



    def get_function_name(self, node):
        for fieldname, value in ast.iter_fields(node.value):
            
            if(fieldname == "func" and isinstance(value, ast.Name)): return value.id
            
            elif(fieldname == "func" and isinstance(value, ast.Attribute)):    
                functionName = self.get_function_attribute(value)

                if functionName != None and value.attr != None : return str(functionName) +'.'+ str(value.attr) 
                elif functionName != None and value.attr == None : return str(functionName)
                elif functionName == None and value.attr == None : return None

        return None
        

    def get_function_attribute(self, node):
        name = None
        attr = None
        
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.Attribute):
                attr = value.attr
                name = self.get_function_attribute(value)

            elif isinstance(value, ast.Constant): name = value.value
            elif isinstance(value,ast.Name): name = value.id
            elif isinstance(value, ast.Subscript): name = self.get_function_attribute(value)
            elif isinstance(value,ast.Call): name = self.get_function_attribute(value)

        return str(name)+'.'+str(attr) if attr else str(name)


    def search_input_in_function_call_and_returned_function_args(self):
        for statement in self.statements:
            if statement['type'] == 'variable':
                if statement.__contains__('valueSrc') and statement.__contains__('args'):
                    for arg in statement['args']:
                        if arg in reversed(self.inputs):
                            statement['isInput'] = True
                            break
                
            elif statement['type'] == 'function_call':
                if statement.__contains__('args'):
                    for arg in statement['args']:
                        if arg in reversed(self.inputs):
                            statement['hasInputs'] = True
                            break
                
            elif statement['type'] == 'function_def':
                if statement.__contains__('returnArgs'):
                    for arg in statement['returnArgs']:
                        if arg in reversed(self.inputs):
                            statement['returnHasInputs'] = True
                            break
                              


    def search_input_in_declaration(self,usedVariables):
        for variable in usedVariables:
            for statement in reversed(self.statements):
                if statement["type"] == "variable" and variable == statement["name"]:
                    if statement["isInput"] is True: return True
                     
                    
        return False

    def get_value_src_from_variable_name(self, name):
        for statement in reversed(self.statements):
            if statement['type'] == 'variable' and statement['name'] == name:
                return [True, statement['valueSrc']]
                
        return [False, name]


    def print_statements(self, *types):
        for statement in self.statements:
            if len(types) == 0: print(statement)
            elif statement["type"] in types: print(statement)


    def write_user_inputs(self):
        fp_input = open("logs/inputs.txt", "a+")

        for statement in self.statements:
            if statement['type'] == 'variable':
                try:
                    json.dump(statement, fp_input)
                    fp_input.write("\n")
        
                except Exception as error:
                    line_number = "Error on line {} ".format(sys.exc_info()[-1].tb_lineno)
                    save_token_parsing_exception(line_number, str(error))
            
        fp_input.close()


    def write_tokens_to_file(self):
        
        fp = open("logs/tokens.txt", "w+")
        
        for statement in self.statements:
            try:
                json.dump(statement, fp)
                fp.write("\n")
        
            except Exception as error:
                line_number = "Error on line {} ".format(sys.exc_info()[-1].tb_lineno)
                save_token_parsing_exception(line_number, str(error))
            
        fp.close()
