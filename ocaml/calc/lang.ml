
module Lang = Zoo.Main(struct
    let name = "calc"

    type command = Syntax.t

    type environment = (string * int) list

    let options = []

    let initial_environment = []

    let read_more _ = false

    let file_parser = None

    let toplevel_parser = Some (Parser.toplevel Lexer.lex)

    let exec env e =
        let n = Interpreter.eval env e in
        Zoo.print_info "%d@." n;
        env

end) ;;

Lang.main ()

