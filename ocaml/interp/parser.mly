%{
%}

%token <int> INT
%token <float> FLOAT
%token <string> VAR
%token <bool> BOOL
%token PLUS
%token MINUS
%token MULT
%token DIV
%token ASSIGN
%token LPAREN
%token RPAREN
%token LET
%token IN
%token IF
%token THEN
%token ELSE
%token NOT
%token EQUAL
%token NEQUAL
%token LT
%token LTE
%token GT
%token GTE
%token ARROW
%token BSLASH
%token COMMA
%token FST
%token SND
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
    | LET x = VAR ASSIGN var_expr = expr IN e = statement
        { Syntax.Let (x, var_expr, e) }
;

conditional:
    | IF cond = expr THEN t_e = expr ELSE f_e = expr
        { Syntax.If (cond, t_e, f_e) }
;

expr:
    | e1 = simple_expr op = rel_op e2 = simple_expr { Syntax.RelOp (op, e1, e2) }
    | BSLASH x = VAR ARROW body = expr              { Syntax.Lambda (x, body) }
    | FST LPAREN p = expr RPAREN                    { Syntax.Fst (p) }
    | SND LPAREN p = expr RPAREN                    { Syntax.Snd (p) }
    | x = VAR LPAREN arg = expr RPAREN              { Syntax.App (x, arg) }
    | e = simple_expr                               { e }
;

rel_op:
    | EQUAL     { Syntax.Eq }
    | NEQUAL    { Syntax.Ne }
    | LT        { Syntax.Lt }
    | LTE       { Syntax.Lte }
    | GT        { Syntax.Gt }
    | GTE       { Syntax.Gte }
;

simple_expr:
    | e1 = term PLUS e2 = simple_expr       { Syntax.Add (e1, e2) }
    | e1 = term MINUS e2 = simple_expr      { Syntax.Sub (e1, e2) }
    | e = term                              { e }
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
    | p = pair                      { p }
    | MINUS f = factor              { Syntax.Neg f }
    | LPAREN e = expr RPAREN        { e }
;

pair:
    LPAREN e1 = factor COMMA e2 = factor RPAREN   { Syntax.Pair (e1, e2) }
;

