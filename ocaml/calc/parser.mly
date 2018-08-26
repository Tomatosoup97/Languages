%{
%}

%token <int> INT
%token <float> FLOAT
%token <string> VAR
%token <bool> BOOL
%token EQUAL
%token PLUS
%token MINUS
%token MULT
%token DIV
%token LPAREN
%token RPAREN
%token LET
%token IN
%token EOF

%start toplevel
%type <Syntax.t> toplevel

%%

toplevel: e = statement EOF
    { e }
;

statement:
    | e = assignment  { e }
    | e = expr { e }
;

assignment:
    | LET x = VAR EQUAL var_expr = expr IN e = statement
    { Syntax.Let (x, var_expr, e) }
;

expr:
    | e1 = term PLUS e2 = expr  { Syntax.Add (e1, e2) }
    | e1 = term MINUS e2 = expr { Syntax.Sub (e1, e2) }
    | e = term                         { e }
;

term:
    | e1 = factor MULT e2 = term    { Syntax.Mult (e1, e2) }
    | e1 = factor DIV e2 = term     { Syntax.Div (e1, e2) }
    | e = factor                    { e }
;

factor:
    | n = INT                     { Syntax.Int n }
    | n = FLOAT                   { Syntax.Float n }
    | x = VAR                     { Syntax.Var x }
    | MINUS f = factor            { Syntax.Neg f }
    | LPAREN e = expr RPAREN      { e }
;

