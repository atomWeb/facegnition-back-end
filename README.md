# facegnition - back-end

## **Sistema _Cloud_ de Identificación Automática de Personas Mediante Comparación Facial.**

<br/>

Este proyecto fue desarrollado como TFM del máster [Ciencia de Datos e Ingeniería de Datos en la Nube 2020-2021](http://www.cidaen.es/) de la Universidad de Castilla-La Mancha.

Se emplea el servicio de análisis de imágenes Rekognition, que permite realizar comparación facial contra rostros previamente registrados en el sistema.  Esta solución se podría aplicar en diversos escenarios, tales como: Registro de usuarios de un hotel, registro a un evento tipo conferencia, control de acceso a áreas restringidas, detección de intrusos, control horario en una empresa, etc.

Además, se ha utilizado [serverless](https://serverless.com/) framework para definir y desplegar en la nube de AWS toda la infraestructura necesaria por el sistema. 

Debe generar un fichero `.env` con las siguientes variables: <br/>
NOTIFY_EMAIL=email para notificación de validaciones. <br/>

Release entregada a la Universidad: v1.01

## Front-end.

La aplicación web `demo` esta alojada en [http://facegnition.ddns.net](http://facegnition.ddns.net).

Se puede ver el código front-end del sistema en el repositorio de gitHub [facegnition](https://github.com/atomWeb/facegnition).
