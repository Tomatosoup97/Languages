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
    | '='         { ASSIGN }
    | '+'         { PLUS }
    | '-'         { MINUS }
    | '*'         { MULT }
    | '/'         { DIV }
    | '('         { LPAREN }
    | ')'         { RPAREN }
    | "=="         { EQUAL }
    | "!="        { NEQUAL }
    | '<'         { LT }
    | "<="        { LTE }
    | '>'         { GT }
    | ">="        { GTE }
    | eof         { EOF }
    | "not"       { NOT }
    | "true"      { BOOL (true) }
    | "false"     { BOOL (false) }
    | "let"       { LET }
    | "in"        { IN }
    | "if"        { IF }
    | "then"      { THEN }
    | "else"      { ELSE }
    | is_char+ (is_char|digit)* { VAR (Lexing.lexeme lexbuf) }

