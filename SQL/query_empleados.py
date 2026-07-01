query = """SELECT emp.nit,
       emp.empresa,
          emp.nombre
       || ' '
       || emp.primer_apellido
       || ' '
       || emp.segundo_apellido
          "Nombre",
       car.nombre_cargo "Cargo",
       dep.nombre_dependencia "Dependencia"
  FROM empleado emp, cargo car, dependencia dep
 WHERE emp.cargo = car.cargo AND emp.dependencia = dep.dependencia 
 and emp.estado in ('A','V','M') 
  and emp.estado <> 'R'  
  and emp.nit NOT IN('55555555')  
  and emp.empleado = (Select max(emp2.empleado) from empleado emp2 where emp2.estado <> 'R' and emp2.nit= emp.nit)  order by emp.nit desc"""