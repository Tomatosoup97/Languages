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
    | digit+ { Int (int_of_string (Lexing.lexeme lexbuf)) }
    | digit+ ('.' digit*)? { Float (float_of_string (Lexing.lexeme lexbuf)) }
    (*| (is_char) (is_char|digit)* { Var (Lexing.lexme lexbuf) }*)
    | "true"      { Bool (true) }
    | "false"     { Bool (false) }
    (*| '='         { EQUAL }*)
    | '+'         { PLUS }
    | '-'         { MINUS }
    | '*'         { MULT }
    | '/'         { DIV }
    | '('         { LPAREN }
    | ')'         { RPAREN }
    | eof         { EOF }

