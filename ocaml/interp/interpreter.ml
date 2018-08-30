
let extend_env env var value = (var, value) :: env

type value =
    | VInt of int
    | VFloat of float
    | VBool of bool
    | VLambda of environment * func_t
    | VPair of value * value

and environment = (string * value) list

and func_t = value -> value

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
    | Syntax.Pair (e1, e2) -> VPair (eval env e1, eval env e2)
    | Syntax.Fst e -> let p = eval env e in (match p with
        | VPair (e, _) -> e)
    | Syntax.Snd e -> let p = eval env e in (match p with
        | VPair (_, e) -> e)
    | Syntax.If (cond, t_e, f_e) ->
        let (VBool cond_val) = eval env cond in
        let to_eval = if cond_val then t_e else f_e in
        eval env to_eval
    | Syntax.RelOp (op, e1, e2) ->
        let (VInt x1) = eval env e1 in
        let (VInt x2) = eval env e2 in
            (match op with
                | Eq -> VBool (x1 == x2)
                | Ne -> VBool (x1 != x2)
                | Lt -> VBool (x1 < x2)
                | Lte -> VBool (x1 <= x2)
                | Gt -> VBool (x1 > x2)
                | Gte -> VBool (x1 >= x2))
    | Syntax.Lambda (var, body) ->
        let func = fun arg -> let env' = extend_env env var arg in eval env' body in
        VLambda (env, func)
    | Syntax.App (var, arg_e) ->
        (try
            let f = List.assoc var env in
                match f with
                    | VLambda (env', f_e) -> let arg_v = eval env arg_e in f_e (arg_v)
                    | _ -> Zoo.error "%s is not a function" var
         with
             | Not_found -> Zoo.error "unknown function %s" var)


let rec string_of_result = function
    | VInt n -> string_of_int n
    | VFloat n -> string_of_float n
    | VBool b -> string_of_bool b
    | VPair (p1, p2) -> "(" ^ (string_of_result p1) ^ "," ^ (string_of_result p2) ^ ")"
    | _ -> "could not cast result to string"

