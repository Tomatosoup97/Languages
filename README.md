# Pascal Interpreter

Simple pascal interpreter written in python

## Grammar:

```
program : compound_statement DOT

compound_statement: BEGIN statement_list END

statement_list : statement 
               | statement SEMI statement_list

statement : compound_statement
          | assignment_statement
          | empty

assignment_statement: variable ASSIGN expr

empty : 

expr    : term ((PLUS | MINUS) term)*
term    : factor ((MUL | DIV) factor)*
factor  : PLUS  factor 
        | MINUS factor
        | INTEGER 
        | LPAREN expr RPAREN
        | variable

variable : ID
```