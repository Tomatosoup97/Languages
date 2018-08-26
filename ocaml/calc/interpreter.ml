
let extend_env env var value = (var, value) :: env

let rec eval env = function
    | Syntax.Int n -> n
(*    | Syntax.Float n -> n *)
    | Syntax.Add (e1, e2) -> eval env e1 + eval env e2
    | Syntax.Sub (e1, e2) -> eval env e1 - eval env e2
    | Syntax.Mult (e1, e2) -> eval env e1 * eval env e2
    | Syntax.Div (e1, e2) -> eval env e1 / eval env e2
    | Syntax.Neg e -> - (eval env e)
    | Syntax.Let (x, var_expr, e) ->
        let var_value = eval env var_expr in
        let env = extend_env env x var_value in
        eval env e
    | Syntax.Var x ->
        (try
             List.assoc x env
         with
             | Not_found -> Zoo.error "unknown variable %s" x)

