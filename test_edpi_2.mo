within ;
model test_dpi_2
  parameter Real t0=0;
  parameter Boolean decision( start = false);
  Real t;

equation
  t = time;

  when time > t0 +5 then
    terminate("Make a decision");
  end when;

  annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
        coordinateSystem(preserveAspectRatio=false)),
    uses(Modelica(version="3.2.1")));
end test_dpi_2;
