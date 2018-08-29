
type rel_op_t =
    | Eq
    | Ne
    | Lt
    | Lte
    | Gt
    | Gte

type expr =
    | Int of int
    | Float of float
    | Bool of bool
    | Var of string
    | Neg of expr
    | Add of expr * expr
    | Sub of expr * expr
    | Mult of expr * expr
    | Div of expr * expr
    | Let of string * expr * expr
    | If of expr * expr * expr
    | RelOp of rel_op_t * expr * expr
    | Lambda of string * expr
    | App of string * expr

type func_t =
    | FuncRecord of (expr -> expr)

type itype =
    | TInt of int
    | TFloat of float
    | TBool of bool


let string_of_expr = function
    | Int n -> string_of_int n
    | Float n -> string_of_float n
    | Bool b -> string_of_bool b
    | Var x -> x
    | _ -> "could not cast expression to string"

