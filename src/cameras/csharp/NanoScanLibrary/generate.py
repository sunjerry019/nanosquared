import types


with open("Dllimports.cs", 'r') as f:
    for line in f:
        line = line.strip()
        if (line != "") and ("static extern" in line):
            splitted    = line.split()

            type_index  = splitted.index("extern")

            return_type = splitted[type_index + 1]
            func_name   = splitted[type_index + 2].split("(")[0]
            temp        = func_name.split("NsInterop")
            my_func     = temp[1] if temp[1] != "" else temp[0]

            params      = line.split("(")[1].split(")")[0]
            params_2    = ", ".join([x.split(" ")[-1] for x in params.split(",")])

            ret         = "return " if return_type != 'void' else ""
            print(f"public {return_type} {my_func} ({params}) {{ {ret}{func_name}({params_2}); }}")
