
module Lang = Zoo.Main(struct
    let name = "calc"

    type command = Syntax.t

    type environment = unit

    let options = []

    let initial_environment = ()

    let read_more _ = false

    let file_parser = None

    let toplevel_parser = Some (Parser.toplevel Lexer.lex)

    let exec () e =
        let n = Interpreter.eval e in
        Zoo.print_info "%d@." n

end) ;;

Lang.main ()

