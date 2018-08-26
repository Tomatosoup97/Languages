
type t =
    | Int of int
    | Float of float
    | Var of string
    | Neg of t
    | Add of t * t
    | Sub of t * t
    | Mult of t * t
    | Div of t * t
    | Let of string * t * t

