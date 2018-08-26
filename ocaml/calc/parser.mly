%{
%}

%token <int> Int
%token <float> Float
%token <bool> Bool
%token PLUS
%token MINUS
%token MULT
%token DIV
%token LPAREN
%token RPAREN
%token EOF

%start toplevel
%type <Syntax.t> toplevel

%%

toplevel: e = expr EOF
    { e }
;

expr:
    | e1 = term PLUS e2 = expr  { Syntax.Add (e1, e2) }
    | e1 = term MINUS e2 = expr { Syntax.Sub (e1, e2) }
    | e = term                  { e }
;

term:
    | e1 = factor MULT e2 = term    { Syntax.Mult (e1, e2) }
    | e1 = factor DIV e2 = term     { Syntax.Div (e1, e2) }
    | e = factor                    { e }
;

factor:
    | n = Int                     { Syntax.Int n }
    | n = Float                   { Syntax.Float n }
    | MINUS f = factor            { Syntax.Neg f }
    | LPAREN e = expr RPAREN      { e }
;
