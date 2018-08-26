
type t =
    | Int of int
    | Float of float
    | Neg of t
    | Add of t * t
    | Sub of t * t
    | Mult of t * t
    | Div of t * t

