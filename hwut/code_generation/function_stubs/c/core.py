# SPDX license identifier: LGPL-2.1
#
# Copyright (C) Frank-Rene Schaefer, private.
# Copyright (C) Frank-Rene Schaefer, 
#               Visteon Innovation&Technology GmbH, 
#               Kerpen, Germany.
#
# This file is part of "HWUT -- The hello worldler's unit test".
#
#                  http://hwut.sourceforge.net
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA
#
# For further information see http://www.genivi.org/. 
#------------------------------------------------------------------------------
from collections import namedtuple
from operator    import attrgetter

import hwut.auxiliary.file_system as fs

import os

class ObjectSpec:
    def __init__(self, Type, Name):
        self.type = Type
        self.name = Name
    def __str__(self):
        return "(%s)%s" % (self.type, self.name)

FunctionSpec = namedtuple("FunctionSpec", ("return_type", "return_type_plain", "name", "argument_list", "argument_list_str"))

varg_promotion_db = {
    "byte":       "unsigned",
    "u8":         "unsigned",
    "u16":        "unsigned",
    "uint8_t":    "unsigned",
    "uint16_t":   "unsigned",
    "unsigned8":  "unsigned",
    "unsigned16": "unsigned",
    "word":       "int",
    "i8":         "int",
    "i16":        "int",
    "signed8":    "int",
    "signed16":   "int",
    "int8_t":     "int",
    "int16_t":    "int",
    "bool":       "int",
    "float":      "double",
}

built_in_number_type_set = set([
    "u32", "unsigned32", "u64", "unsigned64",
    "i32", "signed32", "i64", "signed64",
    "char",  "int", "short",  "int", "long", "long long", 
	"double", "long double", 
])

def is_number_like_type(TypeName):
    global built_in_number_type_set
	
    TypeName = TypeName.replace("unsigned ", "").replace("unsigned\t", "").strip().lower()
    if   TypeName[-1] == "*":           return True  # pointer
    elif TypeName in varg_promotion_db: return True  # promoted integer type
    else:                               return TypeName in built_in_number_type_set

def do(StubDescriptionFileName, OutputFileStem):
    header_list, function_list = parse(StubDescriptionFileName)

    write_stubs(header_list, function_list, OutputFileStem)

def skip_whitespace(fh):
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if   tmp.isspace(): 
            continue
        elif len(tmp) == 0: 
            break
        else:
            fh.seek(-1, 1)
            break

def snap_function(fh):
    text = ""
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if len(tmp) == 0: return None
        elif tmp == ";":  break

        text += tmp

    open_idx  = text.find("(")
    close_idx = text.rfind(")", open_idx)
    if open_idx == -1 or close_idx == -1: 
        return None

    function = extract_specification(text[:open_idx])
    if function is None:
        return

    argument_list_str = text[open_idx+1:close_idx]
    argument_list     = extract_argument_list(argument_list_str)

    return FunctionSpec(function.type, plain_type(function.type), function.name, argument_list, argument_list_str)


def extract_argument_list(Text, Delimiter=","):
    argument_text_list = Text.split(Delimiter)

    result = []
    for text in argument_text_list:
        text = text.strip()
        if not text: continue
        spec = extract_specification(text)
        if spec is not None: 
            result.append(spec)
    return result

def extract_specification(Text):
    """RETURNS: [0] Type
                [1] Name
    """
    text = Text.strip()
    i = 0
    for i in xrange(len(text)-1, -1, -1):
        if not text[i].isalnum() and text[i] != "_": 
            return ObjectSpec(Type=text[:i].strip(), Name=text[i+1:])
    return ObjectSpec(Type="", Name=text)

def parse(StubDbFileName):
    fh = fs.open_or_die(StubDbFileName, "rb")
    
    preprocessor_list = []
    while 1 + 1 == 2:
        skip_whitespace(fh)

        line = fh.readline()
        if len(line) == 0:                     return preprocessor_list, []
        elif line.find("<<functions>>") != -1: break
        preprocessor_list.append(line)

    function_list     = []
    while 1 + 1 == 2:
        skip_whitespace(fh)

        function = snap_function(fh)
        if function is None: 
            break
        function_list.append(function)

    return preprocessor_list, function_list

def write_stubs(header_list, function_list, OutputFileStem):
    type_def_list           = []
    api_list                = []
    implementation_list     = []
    default_object_type_set = set()
    for function in sorted(function_list, key=attrgetter("name")):
        header, type_def, \
        api, implementation = write_stub_server(function, default_object_type_set)
        header_list.append(header)
        type_def_list.append(type_def)
        api_list.append(api)
        implementation_list.append(implementation)

    fh = open("%s.h" % OutputFileStem, "wb")
    fh.write("#ifndef  INCLUDE_GUARD_HWUT_STUB_H\n")
    fh.write("#define INCLUDE_GUARD_HWUT_STUB_H\n\n")
    fh.write("\n")
    fh.write("".join(header_list))
    fh.write("\n")
    fh.write("#define hwut_stub_RETURN(F, V)       do { F ##_RETURN(V); } while(0)\n")
    fh.write("#define hwut_stub_RETURNS(F, N, ...) do { F ##_RETURNS(N, ## __VA_ARGS__); } while(0)\n")
    fh.write("#define hwut_stub_CALL(F, FP)        do { F ##_CALL(FP); } while(0)\n")
    fh.write("#define hwut_stub_CALLS(F, FP)       do { F ##_CALLS(FP); } while(0)\n")
    fh.write("\n")
    fh.write("#endif  /* INCLUDE_GUARD_HWUT_STUB_H */\n")
    fh.close()

    fh = open("%s.c" % OutputFileStem, "wb")
    fh.write("#include \"%s.h\"\n" % os.path.normpath(OutputFileStem))
    fh.write("#include <stdarg.h>\n")
    fh.write("#include <malloc.h>\n\n")
    fh.write("#include <string.h>\n\n")
    fh.write("".join(type_def_list))
    fh.write("\n")
    if default_object_type_set:
        fh.write("\n/* Default objects for aggregated types.                                     */\n")
        L = max(len(x) for x in default_object_type_set)
        fh.write("".join(
            "%s%s self_default_object_%s;\n" % \
            (object_type, " " * (L-len(object_type)), object_type)
            for object_type in sorted(default_object_type_set))
        )
        fh.write("\n")
    fh.write("".join(api_list))
    fh.write("".join(implementation_list))
    fh.close()

def plain_type(ObjectType):
    def cut(T, Word):
        L = len(Word)
	if T.find(Word) != 0:    return T
        elif len(T) < L+1:       return T
        if not T[L].isspace(): return T
        else:                    return T[L:].strip()
    
    result = ObjectType.strip()
    result = cut(result, "static")
    result = cut(result, "extern")
    result = cut(result, "const")
   
    return result

def get_argument_name_list_str(ArgumentList):
    result = "".join(
        "%s, " % argument.name for argument in ArgumentList
    )
    if len(result) != 0:
        result = result[:-2]
    return result


def write_stub_server(FSpec, default_object_type_set):
    """Generates type definition and functions:

           function_RETURN(ReturnValue)
           function_RETURNS(N, ReturnValues ...)
           function_CALL(Functioni(ArgmentList))
           function_CALLS(Function(N, ArgumentList))
    """
    # Aggregated types require a default object to point to.
    dereference_str = ""
    if not is_number_like_type(FSpec.return_type): dereference_str = "*"

    space_n = max(0, 80 - 14 - len(FSpec.name))
    txt  = "/* FUNCTION: %s %s\n" % (FSpec.name, "_" * space_n)
    txt += " *%s*/\n" % (" " * 76)

    no_arguments_f = False
    if (not FSpec.argument_list_str.strip()) or FSpec.argument_list_str.strip() == "void": 
        no_arguments_f = True

    if no_arguments_f:
        argument_list_str_x = ""
    else:                                 
        argument_list_str_x = ", %s" % FSpec.argument_list_str


    space_n = max(4, len(FSpec.return_type)) - 4
    txt += "typedef %s %s(*%s_FUNC)(%s);\n"                   % (FSpec.return_type, " " * space_n, FSpec.name, FSpec.argument_list_str)
    txt += "typedef %s %s(*%s_FUNCS)(int CallCount%s);\n\n" % (FSpec.return_type, " " * space_n, FSpec.name, argument_list_str_x)
    if FSpec.return_type == "void":
        txt += "/* NOT: '%s_RETURN(...)' because function returns 'void' */\n" % FSpec.name
    else:
        txt += "extern void %s%s_RETURN(%s%s ReturnValue);\n" % (" " * space_n, FSpec.name, FSpec.return_type, dereference_str)
        txt += "extern void %s%s_RETURNS(int N, ...);\n"    % (" " * space_n, FSpec.name)

    txt += "extern void %s%s_CALL(%s_FUNC FuncP);\n"   % (" " * space_n, FSpec.name, FSpec.name)
    txt += "extern void %s%s_CALLS(%s_FUNCS FuncP);\n" % (" " * space_n, FSpec.name, FSpec.name)
    txt += "\n"
    header = txt

    member_list = [
        ("int",                   "call_count"),
        ("%s_FUNC" % FSpec.name,  "call"),
        ("%s_FUNCS" % FSpec.name, "call_with_call_count"),
    ]
    if FSpec.return_type == "void":
        pass
    else:
        member_list.extend([
           ("%s%s"  % (FSpec.return_type, dereference_str), "return_value"),
           ("%s%s*" % (FSpec.return_type, dereference_str), "return_value_list"),
           ("int",                                          "return_value_list_size"),
        ])

    init_array = ("0, " * len(member_list))[:-2]


    self_str = "self_%s" % FSpec.name
    L = max(len(type_name) for type_name, member_name in member_list)
    txt  = "static struct {\n"
    for type_name, member_name in member_list:
        txt += "    %s%s %s;\n" % (type_name, " " * (L - len(type_name)), member_name)
    txt += "} %s = { %s };\n" % (self_str, init_array)
    txt += "\n"
    type_def = txt

    txt  = "static void %s_RESET() {\n" % self_str
    txt += "    %s.call_count             = 0;\n"           % self_str
    txt += "    %s.call_with_call_count   = (void*)0;\n"    % self_str
    txt += "    %s.call                   = (void*)0;\n"    % self_str
    if FSpec.return_type == "void":
        pass
    else:
        txt += "    if( %s.return_value_list != (void*)0 ) {\n" % self_str
        txt += "         free(%s.return_value_list);\n"         % self_str
        txt += "    }\n" 
        txt += "    %s.return_value_list      = (void*)0;\n"    % self_str
        txt += "    %s.return_value_list_size = 0;\n"           % self_str
        if is_number_like_type(FSpec.return_type):
            txt += "    %s.return_value           = 0;\n"       % self_str
        else:
            txt += "    %s.return_value           = &self_default_object_%s;\n" % (self_str, FSpec.return_type_plain)
            txt += "    memset((void*)&self_default_object_%s, 0, sizeof(%s));\n" % (FSpec.return_type_plain, FSpec.return_type_plain)
            # Make sure, that the according default object is generated
            default_object_type_set.add(FSpec.return_type_plain)

    txt += "}\n\n"

    if FSpec.return_type == "void": 
        pass
    elif is_number_like_type(FSpec.return_type):
        promoted_return_type = varg_promotion_db.get(FSpec.return_type.lower())
        if promoted_return_type is None: promoted_return_type = FSpec.return_type

        txt += "void %s_RETURN(%s ReturnValue) {\n"   % (FSpec.name, FSpec.return_type)
        txt += "    %s_RESET();\n"                    % self_str
        txt += "    %s.return_value = ReturnValue;\n" % self_str
        txt += "}\n"
        txt += "\n"
        txt += "void %s_RETURNS(int N, ...) {\n" % (FSpec.name)
        txt += "    va_list  arg_p;\n"
        txt += "    int      i;\n"
        txt += "\n"
        txt += "    %s_RESET();\n"                    % self_str
        txt += "    %s.return_value_list      = (%s*)malloc(sizeof(%s)*N);\n" % (self_str, FSpec.return_type, FSpec.return_type)
        txt += "    %s.return_value_list_size = N;\n" % self_str
        txt += "    va_start(arg_p, N);\n"
        txt += "    for(i=0; i<N; ++i) { %s.return_value_list[i] = (%s)va_arg(arg_p, %s); }\n" % (self_str, FSpec.return_type, promoted_return_type)
        txt += "    va_end(arg_p);\n"
        txt += "}\n"
        txt += "\n"
    else:
        txt += "void %s_RETURN(%s* ReturnValue) {\n"   % (FSpec.name, FSpec.return_type)
        txt += "    %s_RESET();\n"                    % self_str
        txt += "    %s.return_value = ReturnValue;\n" % self_str
        txt += "}\n"
        txt += "\n"
        txt += "void %s_RETURNS(int N, ...) {\n" % (FSpec.name)
        txt += "    va_list  arg_p;\n"
        txt += "    int      i;\n"
        txt += "\n"
        txt += "    %s_RESET();\n"                    % self_str
        txt += "    %s.return_value_list      = (%s**)malloc(sizeof(%s*)*N);\n" % (self_str, FSpec.return_type, FSpec.return_type)
        txt += "    %s.return_value_list_size = N;\n" % self_str
        txt += "    va_start(arg_p, N);\n"
        txt += "    for(i=0; i<N; ++i) { %s.return_value_list[i] = va_arg(arg_p, %s*); }\n" % (self_str, FSpec.return_type)
        txt += "    va_end(arg_p);\n"
        txt += "}\n"
        txt += "\n"
        

    txt += "void %s_CALL(%s_FUNC FuncP) {\n" % (FSpec.name, FSpec.name)
    txt += "    %s_RESET();\n"                    % self_str
    txt += "    %s.call = FuncP;\n" % self_str
    txt += "}\n"
    txt += "\n"
    txt += "void %s_CALLS(%s_FUNCS FuncP) {\n" % (FSpec.name, FSpec.name)
    txt += "    %s_RESET();\n"                    % self_str
    txt += "    self_%s.call_with_call_count = FuncP;\n"    % FSpec.name
    txt += "}\n"
    txt += "\n"

    api = txt

    argument_name_list_str = get_argument_name_list_str(FSpec.argument_list)

    if no_arguments_f:
        argument_list_str_x = ""
        the_comma           = ""
    else:
        argument_list_str_x = argument_name_list_str
        the_comma           = ", "

    if FSpec.return_type == "void": 
        return0_str  = "%s.call_with_call_count(%s.call_count%s%s); " % (self_str, self_str, the_comma, argument_list_str_x)
        return1_str  = "%s.call(%s); " % (self_str, argument_list_str_x)
        return2_str  = ""
        return3_str  = "return;"
    else:
        return0_str = "return %s.call_with_call_count(%s.call_count%s%s);" % (self_str, self_str, the_comma, argument_list_str_x)
        return1_str = "return %s.call(%s);"                                % (self_str, argument_list_str_x)
        return2_str = "return %s%s.return_value_list[%s.call_count];"      % (dereference_str, self_str, self_str)
        return3_str = "return %s%s.return_value;"                          % (dereference_str, self_str)

    txt  = "%s\n" % FSpec.return_type
    txt += "%s(%s) {\n" % (FSpec.name, FSpec.argument_list_str)
    txt += "    %s.call_count += 1;\n"                             % self_str
    txt += "    if( %s.call_with_call_count != (void*)0 ) {\n"     % self_str
    txt += "        %s\n"     % return0_str
    txt += "    } else if( %s.call != (void*)0 ) {\n"              % self_str
    txt += "        %s\n"     % return1_str
    if FSpec.return_type != "void":
        txt += "    } else if( %s.return_value_list != (void*)0 ) {\n" % self_str
        txt += "        if( %s.call_count >= %s.return_value_list_size ) {\n" % (self_str, self_str)
        txt += "            %s.call_count = 0;\n"            % self_str
        txt += "        }\n"                                           
        txt += "        %s\n" % return2_str
    txt += "    } else {\n"
    txt += "        %s\n"     % return3_str
    txt += "    }\n"
    txt += "}\n"
    txt += "\n"

    implementation = txt

    return header, type_def, api, implementation

