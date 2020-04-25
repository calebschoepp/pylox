import sys

def main(args):
    if len(args) != 2:
        print("Usage: python3 tools/generate_ast.py <output_directory>")
        sys.exit(1)
    output_dir = args[1]
    define_ast(output_dir, "Expr", [
        "Binary   : left, operator, right",
        "Grouping : expression",                      
        "Literal  : value",                         
        "Unary    : operator, right"   
    ])

def define_ast(output_dir, base_name, types):
    path = output_dir + "/" + base_name + ".py"
    with open(path, 'w') as out:
        out.write("class {}():\n".format(base_name))
        for tipe in types:
            class_name = tipe.split(":")[0].strip()
            fields = tipe.split(":")[1].strip()
            define_type(out, base_name, class_name, fields)

def define_type(out, base_name, class_name, field_list):
    out.write("    class {}({}):\n".format(class_name, base_name))
    out.write("        def __init__(self, {}):\n".format(field_list))
    fields = field_list.split(", ")
    for field in fields:
        out.write("            self.{} = {}\n".format(field, field))
    out.write("\n")

if __name__ == "__main__":
    main(sys.argv)