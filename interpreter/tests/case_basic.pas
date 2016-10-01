PROGRAM Part10;
VAR
   number     : INTEGER;
   a, b, c    : INTEGER;
   y          : REAL;
   str        : STRING;
   on_fire    : BOOLEAN;
   i          : INTEGER;
BEGIN
   BEGIN
      number := 2;
      a := number;
      b := 10 * a + 10 * number DIV 4;
      c := a - (-b);
      y := 5 / 2
   END;

   for i := 1 to 10 do
   BEGIN
      writeln(i);
   END;

   on_fire := True;  { Comment }
   
   if on_fire then
      writeln('Mark is on Fire!')
   else
      writeln('Mark isnt on Fire');

   writeln(' ');
END.