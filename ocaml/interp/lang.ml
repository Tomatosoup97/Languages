
module Lang = Zoo.Main(struct
    let name = "interp"

    type command = Syntax.expr

    type environment = Interpreter.environment

    let options = []

    let initial_environment = []

    let read_more _ = false

    let file_parser = None

    let toplevel_parser = Some (Parser.toplevel Lexer.lex)

    let exec env e =
        let res = Interpreter.eval env e in
        Zoo.print_info "%s@." (Interpreter.string_of_result res);
        env

end) ;;

Lang.main ()

