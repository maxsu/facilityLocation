def foncteur(myFunc):
    """ Functional operators for functions and lists

    Given functions f, g, and a lists h, j, we define:

    | Operator      | Syntax | Description                   |
    |---------------|:------:|:-----------------------------:|
    | Left compose  | f * g  | the function x => f(g(x))     |
    | Right compose | f >= g | the function x => g(f(x))     |
    | Map           | h >= f | the map object map(f, h)      |
    | Tensor        | f @ g  | the function x,y => f(x),f(y) |

    Examples:

    Decorate a function:
        @foncteur
        def myFunc(): ...

    Decorate a list:
        myList = foncteur([...])

    Caveats:
      - @ may be confusing next to matrix multiplication

    """

    myFunc.__mul__ = lambda f, g: lambda x: f(g(x))

    myFunc.__ge__ = lambda f,g: Foncteur(map(g, f)) \
        if isinstance(f, list)  \
        else lambda x: g(f(x))

    myFunc.__matmul__ = lambda f, g:\
        lambda x, y: (f(x), g(y))

    return myFunc
