within ;
model test_dpi_1
  Real y;
  Real t;

equation
  t = time;
  y = 2*t;

  when time > 5 then
    terminate("finish");
  end when;

  annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
        coordinateSystem(preserveAspectRatio=false)));
end test_dpi_1;
