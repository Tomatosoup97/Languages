
let extend_env env var value = (var, value) :: env

type value =
    | VInt of int
    | VFloat of float
    | VBool of bool

let rec eval env = function
    | Syntax.Int n -> VInt n
    | Syntax.Bool b -> VBool b
    | Syntax.Float x -> VFloat x
    | Syntax.Add (e1, e2) ->
        let (VInt x1) = eval env e1 in
        let (VInt x2) = eval env e2 in
        VInt (x1 + x2)
    | Syntax.Sub (e1, e2) ->
        let (VInt x1) = eval env e1 in
        let (VInt x2) = eval env e2 in
        VInt (x1 - x2)
    | Syntax.Mult (e1, e2) ->
        let (VInt x1) = eval env e1 in
        let (VInt x2) = eval env e2 in
        VInt (x1 * x2)
    | Syntax.Div (e1, e2) ->
        let (VInt x1) = eval env e1 in
        let (VInt x2) = eval env e2 in
        VInt (x1 / x2)
    | Syntax.Neg e ->
        let (VInt x) = eval env e in VInt (-x)
    | Syntax.Let (x, var_expr, e) ->
        let var_value = eval env var_expr in
        let env = extend_env env x var_value in
        eval env e
    | Syntax.Var x ->
        (try
             List.assoc x env
         with
             | Not_found -> Zoo.error "unknown variable %s" x)
    | Syntax.If (cond, t_e, f_e) ->
        let (VBool cond_val) = eval env cond in
        let to_eval = if cond_val then t_e else f_e in
        eval env to_eval

    | Syntax.RelOp (op, e1, e2) ->
        let (VInt x1) = eval env e1 in
        let (VInt x2) = eval env e2 in
        match op with
            | Eq -> VBool (x1 == x2)
            | Ne -> VBool (x1 != x2)
            | Lt -> VBool (x1 < x2)
            | Lte -> VBool (x1 <= x2)
            | Gt -> VBool (x1 > x2)
            | Gte -> VBool (x1 >= x2)

let string_of_result = function
    | VInt n -> string_of_int n
    | VFloat n -> string_of_float n
    | VBool b -> string_of_bool b
    | _ -> "could not cast result to string"

