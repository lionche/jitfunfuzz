# coding:utf-8
import math
import random
import re

from six import unichr


class CallableProcessor:
    def __init__(self, callables=['1'], function_name='fuzzopt'):
        self.functions = [self.generate_integer, self.generate_float_point, self.generate_string, self.generate_boolean,
                          self.generate_null, self.generate_undefined, self.generate_array_of_different_type,
                          self.generate_array_of_same_type, self.generate_function]
        self.callables = callables
        self.function_name = function_name
        self.type_inferer = TypeInferer()
        self.function_mapping = {
            'array': self.generate_array,
            'boolean': self.generate_boolean,
            'number': self.generate_number,
            'string': self.generate_string,
            'function': self.generate_function,
            'none': self.generate_a_random_typed_param
        }

    def generate_integer(self):
        power = random.randint(0, 10)
        width = -(math.pow(10, power))
        return str(random.randint(width, -width))

    def generate_float_point(self):
        return str(self.generate_integer()) + (str(random.random())[1:])

    def generate_number(self):
        choice = random.randint(0, 1)
        return self.generate_integer() if choice == 0 else self.generate_float_point()

    def generate_string(self):
        length = random.randint(1, 128)
        result = ''
        start, end = (32, 126)
        while length > 0:
            try:
                newChar = unichr(random.randint(start, end))
                if newChar.__eq__('"') or newChar.__eq__('\\'):
                    newChar = '\\' + newChar
                result += newChar
            except UnicodeEncodeError:
                pass
            length -= 1
        result.replace('\"', '')
        result.replace("'", "")
        result.replace('\n', '')
        result.replace('\r', '')
        return '"' + result + '"'

    def generate_boolean(self):
        return str(bool(random.randint(0, 1))).lower()

    def generate_null(self):
        return 'null'

    def generate_undefined(self):
        return 'undefined'

    def generate_array_of_different_type(self):
        length = random.randint(0, 9)
        result = '[' + self.generate_a_random_typed_param()
        while length > 0:
            result += (', ' + self.generate_a_random_typed_param())
            length -= 1
        result += ']'
        return result

    def generate_array_of_same_type(self):
        length = random.randint(0, 15)
        choice = random.randint(0, self.functions.__len__() - 1)
        while self.functions[choice] == self.generate_array_of_same_type or self.functions[
            choice] == self.generate_array_of_different_type:
            choice = random.randint(0, self.functions.__len__() - 1)
        result = '[' + self.functions[choice]()
        while length > 0:
            result += (', ' + self.functions[choice]())
            length -= 1
        result += ']'
        return result

    def generate_array(self):
        choice = random.randint(0, 1)
        return self.generate_array_of_same_type() if choice == 0 else self.generate_array_of_different_type()

    def generate_a_random_typed_param(self):
        choice = random.randint(0, self.functions.__len__() - 1)
        return self.functions[choice]()

    def generate_a_param(self, type):
        return self.function_mapping[type]()

    def generate_function(self):
        index = random.randint(0, self.callables.__len__() - 1)
        # param_function = self.callables[index].__getitem__(0)
        param_function = self.callables[index]
        if param_function.startswith('"use strict";'):
            param_function = re.sub('"use strict";\n\n', '', param_function, 1)
        return re.sub('function[\s\S]*?\(', 'function(', param_function).rstrip(';')

    def extract_function_name(self, function_body: str):
        index_of_function = function_body.find('function', 0)
        index_of_open_parenthesis = function_body.find('(', index_of_function)
        function_name = function_body[index_of_function + 8:index_of_open_parenthesis]
        return function_name.strip()

    def extract_num_of_params(self, function_body: str):
        index_of_open_parenthesis = function_body.find('(', 0)
        index_of_close_parenthesis = function_body.find(')', index_of_open_parenthesis + 1)
        params = function_body[index_of_open_parenthesis + 1:index_of_close_parenthesis]
        params = params.replace(' ', '')
        if params.__eq__(''):
            return 0
        return params.split(',').__len__()

    def generate_self_calling(self, function_body: str):

        if not function_body.endswith(';'):
            function_body += ';'
        function_body = function_body.replace('function(', 'function fuzzopt(',1)
        param_function_name = 'OPTParameter'
        param_function_count = 0
        if self.functions.__contains__(self.generate_function):
            self.functions.remove(self.generate_function)

        function_name = self.extract_function_name(function_body)

        num_of_param = self.extract_num_of_params(function_body)
        param_type = self.type_inferer.execute(function_body)

        self_calling = '('
        if num_of_param > 0:
            param = self.generate_a_param(param_type[0][0])
            function_body += '\nvar ' + param_function_name + str(param_function_count) + ' = ' + param + ';'
            self_calling += param_function_name + str(param_function_count)
            param_function_count += 1
            num_of_param -= 1
        index = 1
        while num_of_param > 0:
            self_calling += ', '
            param = self.generate_a_param(param_type[index][0])
            function_body += '\nvar ' + param_function_name + str(param_function_count) + ' = ' + param + ';'
            self_calling += param_function_name + str(param_function_count)
            param_function_count += 1
            index += 1
            num_of_param -= 1
        self_calling += ')'
        # print(function_body)
        try:
            import execjs
            with open('/root/fuzzopt/workline/node/fixReturn.js', 'r', encoding='utf-8') as f:
                jstext = f.read()
            ctx = execjs.compile(jstext)

            function_body = ctx.call('fixReturn', function_body)
        except:
            pass

        # jit_testcese_dict = self.get_output_statement(function_body_fix_return, function_name, self_calling)
        return function_body

    def get_output_statement(self, function_body_fix_return, function_name, self_calling):
        dic = {}
        Suffix = 'var FuzzoptJITResult = ' + function_name + self_calling + ';\nprint(FuzzoptJITResult);'

        # v8 %OptimizeFunctionOnNextCall(foo);

        v8 = function_body_fix_return + f"%OptimizeFunctionOnNextCall({function_name});\n"
        v8 += Suffix
        dic['v8'] = v8
        # jsc
        jsc = function_body_fix_return + f"for (let i = 0 ; i < 30 ; i++) {{{function_name + self_calling}}}\n"
        jsc += f"for (let i = 0 ; i < 75 ; i++) {{{function_name + self_calling}}}\n"
        jsc += f"for (let i = 0 ; i < 150 ; i++) {{{function_name + self_calling}}}\n"
        jsc += Suffix
        dic['jsc'] = jsc

        # chakra
        chakra = function_body_fix_return + f"for (let i = 0 ; i < 30 ; i++) {{{function_name + self_calling}}}\n"
        chakra += f"for (let i = 0 ; i < 150 ; i++) {{{function_name + self_calling}}}\n"
        chakra += Suffix
        dic['chakra'] = chakra

        # spm
        spm = function_body_fix_return + f"for (let i = 0 ; i < 150 ; i++) {{{function_name + self_calling}}}\n"
        spm += f"for (let i = 0 ; i < 300 ; i++) {{{function_name + self_calling}}}\n"
        spm += Suffix
        dic['spm'] = spm

        return dic

    # def get_random_self_calling(self):
    #     choice = random.randint(0, self.callables.__len__() - 1)
    #     function_body = self.callables[choice].__getitem__(0).decode()
    #     return self.generate_self_calling(function_body)

    # def get_self_calling(self, function_body):
    #     return self.generate_self_calling(function_body)


class TypeInferer:
    def __init__(self):
        self.array_characters = [
            [],
            [".length", ".concat", ".join", ".pop", ".push",
             ".reverse", ".shift", ".slice", ".sort", ".splice", ".toSource",
             ".toLocaleString", ".unshift", "[", " ["],
            []
        ]
        self.boolean_characters = [
            ["!", "! ", "&& ", "|| ", "^", "^ ", "true=", "true= ", "true =", "true = ", "false=", "false= ", "false =",
             "false = "],
            [".toSource", " &&", " ||", "^", " ^", "=true", " =true", "= true", " = true", "=false", " =false",
             "= false", " = false"],
            []
        ]
        self.number_characters = [
            ["-=", "-= ", "*=", "*= ", "/=", "/= ", "++", "++ ", "--", "-- ", "%", "% "],
            [".toLocaleString", ".toFixed", ".toExponential", ".toPrecision", "-=", " -=", "*=", " *=", "/=", " /=",
             "++", " ++", "++ ", "--", " --", "-- ", "%", " %", "% "],
            []
        ]
        self.string_characters = [
            [],
            [".length", ".anchor", ".big", ".blink", ".bold", ".charAt", ".charCodeAt", ".concat", ".fixed",
             ".fontsize", ".indexOf", ".italics", ".lastIndexOf", ".link", ".localeCompare", ".match", ".replace",
             ".search", ".slice", ".small", ".split", ".strike", ".sub", ".substr", ".substring", ".sup",
             ".toLocaleLowerCase", ".toLocaleUpperCase", ".toLowerCase", ".toUpperCase", ".toSource", "[", " [", "=\"",
             " =\"", "= \"", " = \""],
            []
        ]
        self.function_characters = [
            [],
            ["(", " (", "=function", " =function", "= function", " = function"],
            [["function", "("], ["function ", "("], ["function", " ("], ["function ", " ("]]
        ]

    def execute(self, callable):
        params = self.extract_params(callable)
        result = []
        for i in range(0, params.__len__()):
            result.append(self.infer_param_type(callable, params[i]))
        return result

    def infer_param_type(self, callable, param_name):
        characters = [self.array_characters, self.boolean_characters, self.number_characters, self.string_characters,
                      self.function_characters]
        counter = [0, 0, 0, 0, 0]
        types = ["array", "boolean", "number", "string", "function"]
        for i in range(0, characters.__len__()):
            counter[i] += self.infer_left(param_name, callable, characters[i][0])
            counter[i] += self.infer_right(param_name, callable, characters[i][1])
            counter[i] += self.infer_around(param_name, callable, characters[i][2])

        max = 0
        for i in range(0, counter.__len__()):
            if counter[i] > max:
                max = counter[i]

        if max > 0:
            result = []
            for i in range(0, counter.__len__()):
                if counter[i] == max:
                    result.append(types[i])
            return result
        else:
            return ['none']

    def infer_left(self, param_name, callable, left_characters):
        result = 0
        for character in left_characters:
            target = character + param_name
            if callable.__contains__(target):
                result += 1
        return result

    def infer_right(self, param_name, callable, left_characters):
        result = 0
        for character in left_characters:
            target = param_name + character
            if callable.__contains__(target):
                result += 1
        return result

    def infer_around(self, param_name, callable, left_characters):
        result = 0
        for character in left_characters:
            target = character[0] + param_name + character[1]
            if callable.__contains__(target):
                result += 1
        return result

    def extract_params(self, callable):
        left_index = callable.find('(')
        right_index = callable.find(')')
        raw = callable[left_index + 1:right_index]
        if raw.__len__() < 1:
            return []

        params = raw.strip(' ').split(',')
        for i in range(0, params.__len__()):
            params[i] = params[i].strip(' ')
        return params
