
let rec eval = function
    | Syntax.Int n -> n
(*    | Syntax.Float n -> n *)
    | Syntax.Add (e1, e2) -> eval e1 + eval e2
    | Syntax.Sub (e1, e2) -> eval e1 - eval e2
    | Syntax.Mult (e1, e2) -> eval e1 * eval e2
    | Syntax.Div (e1, e2) -> eval e1 / eval e2
    | Syntax.Neg e -> - (eval e)

