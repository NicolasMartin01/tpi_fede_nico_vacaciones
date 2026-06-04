# Elección del proceso

Justificamos por qué elegimos el proceso. 

## Proceso seleccionado

El grupo eligió resolver el proceso de Gestión de solicitudes de vacaciones.

## Organización de referencia

# (Acá deberíamos darle una identidad a la organización/empresa ficticia a la que le resolvemos el problema)

PYME del sector comercial/servicios. (Cambiar)


## Justificación de la elección

Seleccionamos resolver el proceso de gestión de vacaciones porque creemos que reúne las características ideales para ser modelado, analizado y automatizado mediante un chatbot. A continuación detallamos los criterios que nos sirven para estandarizar este proceso:

#### 1. Reglas de negocio

El proceso opera bajo reglas definidas: el empleado debe contar con días disponibles en su saldo, las fechas solicitadas no deben superponerse con licencias ya aprobadas, y la solicitud debe realizarse con antelación mínima de 1 mes.

#### 2. Alta frecuencia y carga administrativa repetitiva

En una PYME, las solicitudes de vacaciones se gestionan de forma manual: el empleado consulta a RRHH, RRHH verifica el saldo y el calendario, el supervisor aprueba o rechaza, y finalmente se notifica al empleado. Este flujo manual genera demoras, errores y un consumo innecesario de tiempo del área de Recursos Humanos. La automatización aporta valor operativo.

#### 3. Actores y caminos lógicos identificados

Nuestro proceso involucra al menos tres actores (Empleado, Chatbot/Bot/Sistema y Supervisor), lo que permite modelar Lanes diferenciados en el diagrama BPMN. Identificamos los siguientes puntos de decisión:

- ¿el empleado existe en el sistema?
- ¿el empleado tiene saldo suficiente de días?
- ¿la solicitud se hizo con 30 dias de antelación?
- ¿la solicitud se superpone con licencias ya aprobadas?
- ¿la solicitud es aprobada por el supervisor?  

#### 4. Persistencia de datos

El proceso requiere consultar, actualizar y persistir información. El saldo de días disponibles por empleado, historial de solicitudes y estado de cada una.<br>

Identificamos las siguientes entidades para el modelo de datos:

-   Empleado
    -   legajo
    -   nombre
    -   apellido
    -   saldoVacaciones
-   Solicitud
    -   id
    -   fechaInicio
    -   fechaFin
    -   estado
-   Supervisor
    -   legajo
    -   nombre
    -   apellido
    -   telefono

#### 5. Automatización mediante chatbot

El proceso se automatizará mediante un chatbot qué interactuará con el empleado y validará su legajo, su saldo y las fechas de la solicitud de vacaciones que quiera crear. La solicitud será enviada a su supervisor y decidirá si la solicitud se crea o no.