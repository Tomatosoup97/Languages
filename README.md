# Pascal Interpreter

Simple pascal interpreter written in python

## BNF Grammar:

```
program : PROGRAM variable SEMI block DOT

block : declarations compound_statement

declarations : VAR (variable_declaration SEMI)+
             | empty

variable_declaration : ID (COMMA ID)* COLON type_spec

type_spec : INTEGER

compound_statement : BEGIN statement_list END

statement_list : statement
               | statement SEMI statement_list

statement : conditional_statement
          | compound_statement
          | forloop_statement
          | assignment_statement
          | writeln_statement
          | empty

writeln_statement : writeln LPAREN expr (COMMA expr)* RPAREN

conditional_statement : IF expr THEN statement
                      | IF expr THEN statement else statement

forloop_statement : FOR assignment_statement TO expr DO statement

assignment_statement : variable ASSIGN expr

expr : simple_expr
     | simple_expr relational_operator simple_expr 
     | boolean_expr
     | string_expr

relational_operator : ( EQ | NE | LT | LTE | GT | GTE )

boolean_expr : (TRUE | FALSE)

string_expr : STRING_CONST

simple_expr : term ((PLUS | MINUS) term)*

term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*

factor : PLUS factor
       | MINUS factor
       | INTEGER_CONST
       | REAL_CONST
       | LPAREN expr RPAREN
       | variable

variable: ID

empty :

```