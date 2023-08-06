# sympy-to-semantic-latex-translator

## Description

This project in its current version is capable of translating different mathematical expressions (including e.g. the trigonometric functions as well as logarithmic functions) to the required latex equivalent.

## Motivation

Latex is often used to publish scientific papers. Latex is a software package based on the Tex typesetting system, which is particularly useful for creating documents containing mathematical expressions. As converting mathematical expressions to latex per hand can be quite difficult, this project is designed to solve this problem and with that save a lot of time and energy for the developer. It has to be said, that extending the variety of translations e.g. adding more latex functions, might assume a bit of programming (especially SymPy) knowledge, because it is still possible that a few functions cannot be translated correctly by the program.

## Manual

When all the files provided have been downloaded, the program can be run from the command line with the command python3 main.py CAS_SymPy.csv (name of the csv file). This is followed by the prompt: "Enter a SymPy expression: ". There the user enters a mathematical expression and then receives an output suitable to generate the equivalent of the expression for LaTeX. As long as the user enters a valid expression, the prompt reappears after each entry. If the user input is incorrect or cannot be correctly interpreted by the program, a corresponding error message is thrown. The program gets closed when the user pressed enter without any input. The logging commands used in the program are displayed on the command line.

## Programming language

This project was complete using python. This was mandatory to complete this project, but also had a variety of advantages:
- Python is one of the most spread programming languages
- all project participants are familiar with python
- Python provides a big range of libraries and functions that helped to complete this project
- The objective was to convert SymPy expression, SymPy is a python library for mathematical expressions

## Project features, with code examples

In comparison to the current latex printer of SymPy, this program solves a variety of errors occurring the mentioned API. Of course this version is still not complete and need to be further extended (see: How to extend the project?).

This description provides an overview about the different parts of the program and how they function. The main part of this program that is needed to run the tool is split up into three files:
- main.py
- printer.py
- csv_loader.py

### Description of code

All code files contain brief descriptions and comments to explain selected code snippets. Below you can find a more detailed description of the main files.

**main.py**

In this file the main loop is executed. Therefore we use the SymPy function .core and multiple self-created functions from printer.py and csv_loader.py.

~~~
import sympy.core
from printer import SemanticLatexPrinter, sympy_to_semantic_latex, SemanticLatexNotAvailableException
from csv_loader import load_csv_file, load_csv_file_for_printer
~~~

Before executing the main part, the function sympy_to_semantic_latex (which is used to convert the expressions) is called by a wrapper function and stored in sympy.core.Basic.semanticLatex. The wrapper function has the purpose to prevent irregularities that occur if the function sympy_to_semantic_latex is directly called. The result is stored sympy.core.Basic.semanticLatex, which is due to its purpose as a base class for all SymPy objects

Subsequently the main part is executed, which starts with a few necessary settings. Therefore a logger is set up to log messages of the level .INFO or higher. Next, readline is imported to interpret commando line input.

The next step is to import the sympy_parser, that provides the functionality to import SymPy expressions entered as strings. Also sys is imported to check the command line input to decide if csv file should be loaded. The csv file contains the possible cases requested for this project that aren't covered in the code itself. This is realized as follows:

~~~
if len(sys.argv) > 1:
    load_csv_file_for_printer(sys.argv[1])
~~~

The program always expects the csv file as input. The first argument of the input is in this case the main.py, the second one is the csv file. If the user doesn’t try to access the csv file, this code ensures that the program doesn't try to load the csv file (unsuccessfully).   

If this requirement is fulfilled, the main loop of the program is executed.

~~~
try:
    while True:
        expression = sympy_parser.parse_expr(input("Enter a SymPy-expression: "),evaluate=False)
                try:
            print(sympy_to_semantic_latex(expression))
        except SemanticLatexNotAvailableException as ex:
            print("Translation failed:",ex)
except (EOFError, IndexError):
  pass
~~~

This parses the input and prints the converted expression using the sympy_to_semantic_latex function from printer.py. An exception to this is expressions without any semantics. Those are executed without the use of the csv file and are processed with the SemanticLatexNotAvailableException function.

The while loop (while True) is set up as a continuous loop. This means after each input and the resulting output another input is requested. The EOFError, IndexError exception occurs if the user provides an empty input. This set up (pass) enables the user to close the function in that way, hence just press enter without any input. 

**printer.py**

The printer file contains the key functionality of the program, it ultimately converts the printout to its latex equivalent.
The file consists of the "get_expression_type()"- method, the SemanticLatexNotAvailableException- class, the FormatTemplate- class, the SemanticLatexPrinter- class and the method "sympy_to_semantic_latex()". 

The SemanticLatexPrinter class first initializes two dictionaries. The "generic_latex_table"-dictionary, which includes the arithmetic operations and basic functions of SymPy (e.g. 

~~~
sympy.core.add.Add
~~~

) and the "semantic_latex_table"-dictionary, which includes the trigonometric functions in SymPy, as well as some logarithmic functions(e.g.

~~~
(sympy.functions.elementary.trigonometric.sin,1): (sympy.sin(Symbol("x0")),FormatTemplate(r"\sin@{$0}"))
~~~

).
Furthermore, the class contains a method tree_match(), which generally checks whether the given expression matches the second parameter of the function, i.e. the template, and the associated number of arguments. If not, None is returned, otherwise the dictionary containing the (recursively created) arguments of the expression with the associated values.

The _print() method in the same class checks at the beginning whether the expression type and the number of arguments are contained in the "semantic_latex_table" dictionary and, if so, saves the entry in the "format_template" variable. Then the dictionary created by the tree_match() method is substituted into the format_template variable and returned (if format_template can be interpreted as a tuple, otherwise each argument is passed individually).

~~~
if (expr_type, arg_count) in semantic_latex_table:
            format_template = semantic_latex_table[(expr_type, arg_count)]
            if isinstance(format_template,tuple):
                logger.debug(f"Matching {expression} against {format_template[0]}...")
                format_arguments = self.tree_match(expression, format_template[0])
                format_template = format_template[1]
            else:
                format_arguments = {str(i): self._print(expression.args[i]) for i in range(arg_count)}
            if format_arguments != None:
                return format_template.substitute(format_arguments)
            logger.warning(f'Unable to translate "{expression}": Translation entry for {expr_type.__module__}.{expr_type.__qualname__} with {arg_count} arguments did not match.')
~~~

The last part of this method now checks whether the individual operations are elements of the generic_latex_table dictionary (logs if not) and finally lets the LatexPrinter class print the expression.

~~~
allowed = False
        for allowed_type in generic_latex_table:
            if isinstance(expression, allowed_type):
                allowed = True
        if not allowed:
            if not expr_type in (key[0] for key in semantic_latex_table.keys()):
                logger.warning(f'Unable to translate "{expression}": No translation entry for {expr_type.__module__}.{expr_type.__qualname__} found.')
            else:
                logger.warning(f'Unable to translate "{expression}": No translation entry for {expr_type.__module__}.{expr_type.__qualname__} with {arg_count} arguments found.')
                allowed_number_args = None
                for k, count in semantic_latex_table:
                    if k == expr_type:
                        logger.info(f'There is a translation entry for "{expr_type.__module__}.{expr_type.__qualname__}" with {count} arguments.')
            if self._settings['strict_mode']:
                raise SemanticLatexNotAvailableException(expression)
        return LatexPrinter._print(self, expression)
 ~~~

The emptyPrinter()- method extends the fallback print method of the LatexPrinter to raise an error in strict_mode.

The "get_expression_type()"- method is self-explanatory.

The sympy_to_semantic_latex method just calls the do print() method of the SemanticLatexPrinter class, inherited from the LatexPrinter class. It returns the converted expression.

**csv_loader.py**

The csv_loader is needed to get necessary information about a variety of SymPy expressions. Therefore a the CAS_SymPy.csv is used to store this information, such as the number of variables and the DLMF equivalent for each expression. In this file also the logger is set up first. Also, there is a replacement dictionary, since some expressions lead to complications in the programs code.

Next, the function load_csv_file(filename) is executed.

~~~
with open(filename) as file:
        reader = csv.reader(file, delimiter=";")
        for line in reader:
            if line == []: continue
            if line[0] != '' and line[2].isdigit():
~~~

Therefore, the csv is read and the values for the rows in the relevant columns are checked. The first column (line[0]) contains the SymPy expression, the third column the number variables, which is why the existence of a number is checked. If this is the case, the DLMF equivalent for the expression gets transformed for the further use in the program. 

Next, the necessary information get extracted to convert the expression to semantic LaTeX. 

~~~
                expr_func = get_expression_type(expr)
                arg_count = len(getattr(expr, "args", ()))
                csv_semantic_latex_table[(expr_func, arg_count)] = (expr, translation_as_FormatTemplate)
~~~

This is realized by splitting the expression into the expression type and the number of arguments and uses these as a key in a dictionary named "csv_semantic_latex_table". 

## Tests

We included a "testcases.txt" file containing several (nested) testcases, with the correct latextranslation separated by a semicolon. For proving the functionality of the program, the "test_sympy_to_latex.py" script iterates over all lines in the testcases file and checks using unittest the results.

## Distribution of tasks / Credits

Matthias: Programming of main program parts of the printer.py and the main.py, improving the csv_loader.py

Wilma: Programming of the csv_loader.py, support to main programming tasks

Dario: Programming support, converting project to module, creation of documentation/read me

Paul: Programming support, creation of test cases, converting project to module, creation of documentation/read me

