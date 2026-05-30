# Automaz(h)er v1.0

Automatiza la publicación de comentarios en sorteos de redes sociales mediante visión por computadora.

Configura múltiples dominios(sorteos), define comentarios y etiquetados. Deja que el bot trabaje por ti comentando automáticamente.

## ¿Qué hace?
**Versión 1.0**

-**1. Reconocimiento visual** Busca en la pantalla la barra de navegación (URL), barra de comentarios, y botón de enviado.

-**2. Comentarios inteligentes** Comenta de manera dinámica, generando aleatoriamente un rango de comentarios en cada URL para no ser percatado como predecible.

-**3. Persistencia con JSON** Guarda las URL, comentarios, limites de comentarios, y avances para futuras sesiones.

-**4. Reportabilidad de datos** Muestra un avance de los comentarios realizados en cada dominio

-**5. Botón de pánico**: pulsa `q` en cualquier momento para detener el bot.

---

## Requisitos

-**Python 3.8** o superior

-**Conexión a internet**

-**Acceso a un navegador iniciado con tu instagram**

---

## Linux (Instalación y Ejecución)

1. **Abrir terminal** en la carpeta del proyecto.

2. **Crear entorno virtual** (opcional pero recomendado):
   ```bash
   python3 -m venv venv
   ```

3. **Activar entorno**:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar**:
   ```bash
   python main.py
   ```
---
## Windows (Instalación y Ejecución)

**Nota importante**: Aún no se ha probado en windows, proximamente lo arreglaré. Prueba siguiendo estos pasos, Es posible que algunos comandos no funcionen hasta actualizaciones futuras

1. **Abrir CMD o PowerShell** en la carpeta del proyecto.

2. **Crear entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   ```

3. **Activar entorno**:
   ```bash
   venv\Scripts\activate
   ```

4. **Instalar dependencias**:
   ```bash
   pip install opencv-python mediapipe pyautogui sounddevice numpy
   ```

5. **Ejecutar**:
   ```bash
   python main.py
   ```

---
## Método de uso

**Paso 1**: Configurar las imagenes de visión

El bot utiliza reconocimiento visual para encontrar elementos en pantalla. Necesitas capturar imagenes de referencia.
Guarda estas imagenes en las carpetas correspondientes dentro de `assets/...`:

1. Captura de la barra de direcciones de tu navegador (en `assets/barraURL`)

2. Captura el campo de comentario (donde dice "Agrega un comentario...") (en `assets/barraComentado`)

3. Captura el boton de publicar (en `assets/botonPublicar`)

*Ejemplo (debes tomar la captura en el perimetro rojo)*:

<img width="1043" height="86" alt="ejemploCaptura" src="https://github.com/user-attachments/assets/119c1799-faa8-4924-a537-37c9871f1fef" />


**Consideración**: El programa utiliza capturas del navegador Brave a 100% de zoom, es probable que puedas usarlo sin configurar este paso, sin embargo recomiendo encarecidamente establecer tus capturas, ya que el algortimo extrae la posición a partir de ello y cada pantalla/navegador es diferente

**Nota importante**: El programa utiliza una tabla de capturas, intenta poner más de una captura de la misma en una carpeta para así tener menos probabilidades de que el reconocimiento falle. (Osea que si no encuentra en la primera imagen, salta a la siguiente.)

---

**Paso 2**: Configurar los sorteos

Al ejecutar el programa con `main.py` se desplegará un menú.

<img width="344" height="93" alt="menuOpciones" src="https://github.com/user-attachments/assets/e35bc08e-4ba9-4d13-ad98-d0d2fa17a6e2" />

**Selecciona la opcion 2 del menu principal "Configurar Sorteos (URLs)"**

**Dentro de la gestion de URLs podras:**

-Añadir URLs: Selecciona el dominio donde quieres agregar URLs. Cada URL recibira un limite aleatorio de comentarios.

-Añadir comentarios: Desde el submenu "Editar comentarios" puedes agregar multiples textos. El bot eligira uno al azar cada vez que comente.

-Añadir etiquetados: Si el dominio requiere etiquetar, puedes agregar usuarios con el simbolo @. El bot eligira entre 1 y 3 etiquetas al azar por comentario

<img width="343" height="135" alt="submenuGestionUrlpng" src="https://github.com/user-attachments/assets/bd03cd9b-3478-439a-96af-45934954eea4" />

**Nota**: Toda la información que introduzcas se guardará en un JSON en `persistence/`, persistiendo la información de sorteos.

---

**Paso 3**: Preparar el entorno y ejecutar

Una vez configuradas las imagenes, dominios, y navegador. En el menú principal (main.py) selecciona la opción 1 "Iniciar automatización"

Se lanzará una ventana preguntandote si estás listo asegurate de:

1.-Tener el navegador abierto e iniciado en Instagram (con tu sesion activa)

2.- La ventana del navegador visible y en primer plano

3.- Ninguna otra ventana bloqueando la interfaz de Instagram

<img width="400" height="148" alt="controlUsuario" src="https://github.com/user-attachments/assets/bb29d45b-dab6-4aed-8c79-cd0b5665c195" />

Una vez tengas todo listo dale a iniciar. 

Si el bot no inicia, puedes ver los logs de que falló al presionar `q` o apagarlo forzosamente con `ctrl + c` en la terminal.

---

## Consideraciones importantes

-No muevas el mouse ni cambies de ventana mientras el bot esta ejecutandose

-Evita usar el teclado durante la automatizacion para no interferir

-El bot fue disenado para Instagram, pero puede adaptarse a otras redes sociales cambiando las imagenes de referencia

-Usa este programa de manera etica y respeta los terminos de servicio de la plataforma (No genera spam descontrolado, solo emula el comportamiento humano de comentar una publicación.)

---

## Contribuciones
Las contribuciones son bienvenidas. Abre un issue o envia un pull request en GitHub.

---
## Agradecimientos

Agradezco a Annix por su idea inicial y la recomendación de utilizar pyguiauto

---

## Licencia

MIT License

---

**Desarrollado por kbdd23**
