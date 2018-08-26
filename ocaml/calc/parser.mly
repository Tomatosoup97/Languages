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
%token IF
%token THEN
%token ELSE
%token EOF

%start toplevel
%type <Syntax.expr> toplevel

%%

toplevel: e = statement EOF
    { e }
;

statement:
    | e = assignment    { e }
    | e = expr          { e }
    | e = conditional   { e }
;

assignment:
    | LET x = VAR EQUAL var_expr = expr IN e = statement
    { Syntax.Let (x, var_expr, e) }
;

conditional:
    | IF cond = expr THEN t_e = expr ELSE f_e = expr
    { Syntax.If (cond, t_e, f_e) }
;

expr:
    | e1 = term PLUS e2 = expr      { Syntax.Add (e1, e2) }
    | e1 = term MINUS e2 = expr     { Syntax.Sub (e1, e2) }
    | e = term                      { e }
;

term:
    | e1 = factor MULT e2 = term    { Syntax.Mult (e1, e2) }
    | e1 = factor DIV e2 = term     { Syntax.Div (e1, e2) }
    | e = factor                    { e }
;

factor:
    | n = INT                       { Syntax.Int n }
    | n = FLOAT                     { Syntax.Float n }
    | b = BOOL                      { Syntax.Bool b }
    | x = VAR                       { Syntax.Var x }
    | MINUS f = factor              { Syntax.Neg f }
    | LPAREN e = expr RPAREN        { e }
;

