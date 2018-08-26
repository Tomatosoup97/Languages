{
    open Parser
}

let space = [' ' '\t' '\n' '\r']
let digit = ['0'-'9']
let lower = ['a'-'z']
let upper = ['A'-'Z']
let is_char = ['a'-'z' 'A'-'Z' '_']

rule lex = parse
    | space+ { lex lexbuf }
    | digit+ { INT (int_of_string (Lexing.lexeme lexbuf)) }
    | digit+ ('.' digit*)? { FLOAT (float_of_string (Lexing.lexeme lexbuf)) }
    | '='         { EQUAL }
    | '+'         { PLUS }
    | '-'         { MINUS }
    | '*'         { MULT }
    | '/'         { DIV }
    | '('         { LPAREN }
    | ')'         { RPAREN }
    | eof         { EOF }
    | "true"      { BOOL (true) }
    | "false"     { BOOL (false) }
    | "let"       { LET }
    | "in"        { IN }
    | is_char+ (is_char|digit)* { VAR (Lexing.lexeme lexbuf) }

