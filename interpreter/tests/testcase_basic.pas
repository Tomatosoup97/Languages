PROGRAM Part10;
VAR
   number     : INTEGER;
   a, b, c, x : INTEGER;
   y          : REAL;
   str        : STRING;
   bool       : BOOLEAN;
BEGIN
   BEGIN
      number := 2;
      a := number;
      b := 10 * a + 10 * number DIV 4;
      c := a - - b
   END;
   { Comment }
   x := 11;
   y := 5 / 2;
   bool := True;
   str := 'abc';
END.