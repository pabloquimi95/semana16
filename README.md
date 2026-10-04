# Restaurante App — Semana 16 (Manejo de eventos aplicado a gestión de usuarios)

## Propósito de la Semana 16

Evolución de `restaurante_app` de la Semana 15 incorporando **manejo de eventos** en Tkinter aplicado a una situación real: la **gestión de usuarios**. Se conserva la arquitectura modular, la persistencia JSON, el inicio de sesión, navegación, gestión de productos y ventas, y se amplía únicamente la sección **Usuarios** para demostrar cómo una selección, una tecla o un cambio de opción pueden activar callbacks sin concentrar la lógica en la interfaz.

La interfaz mantiene separación de responsabilidades: la UI coordina la interacción, y las validaciones, reglas y persistencia se delegan a `RestauranteServicio`.

## Novedades S16 respecto a S15

- **Modelo `Usuario` con `rol`:** `Administrador / Empleado / Cliente` (`ROLES_PERMITIDOS`), validado y persistido en `usuarios.json`.
- **Gestión completa de usuarios:** Registrar, consultar, actualizar y eliminar desde formulario + `Treeview` (columnas: identificador, nombre, usuario, rol — sin mostrar contraseña).
- **Control de acceso:** solo `Administrador` accede a "Usuarios"; gestiona `Empleado` y `Cliente`; no se pueden crear nuevos `Administrador` desde la UI; no se puede auto-eliminar ni cambiar el rol del admin actual.

## Manejo de eventos aplicado (S16)

Flujo esperado S16:

```
Usuario → Evento → bind() → callback(event) → RestauranteServicio → usuarios.json → Treeview
```

| Interacción | Evento | `bind()` | Callback | Reutilización |
|---|---|---|---|---|
| Seleccionar fila en tabla | `<<TreeviewSelect>>` | `tabla.bind` | `al_seleccionar_usuario(event)` → obtiene `identificador` → `buscar_usuario_por_identificador` → `cargar_usuario_en_formulario` | No lee JSON directo |
| Presionar Enter en formulario | `<Return>` | `entry/combo.bind` | `al_presionar_enter(event)` → `registrar_usuario()` | Reutiliza método existente |
| Presionar Escape | `<Escape>` | `widget.bind` (a cada campo + tabla) | `al_presionar_escape(event)` → `limpiar_formulario_usuario()` + `selection_remove` | Limpia y devuelve foco |
| Cambiar opción Rol | `<<ComboboxSelected>>` | `combo.bind` | `al_seleccionar_rol(event)` → `actualizar_texto_rol` | Respuesta visual |
| Botones Registrar/Actualizar/Eliminar/Limpiar | `command=` | `ttk.Button(..., command=...)` | `registrar_usuario` / `actualizar_usuario` / `eliminar_usuario` / `limpiar_formulario_usuario` | Diferencia `command=` vs `bind()` |

**No se duplica lógica:** `al_presionar_enter` reutiliza `registrar_usuario()`. **No se manipula JSON desde la UI:** toda lectura/escritura pasa por `RestauranteServicio`.

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json      # ahora con campo "rol"
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py         # con ROLES_PERMITIDOS y propiedad rol
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py  # pathlib para rutas dinámicas
│   └── restaurante_servicio.py # CRUD usuarios + ventas + productos
├── ui/
│   ├── login_view.py
│   └── main_view.py       # S16: gestión usuarios con bind() + Treeview
├── assets/
│   ├── icons/             # obligatorio
│   └── logo/
├── main.py                # pathlib, única instancia Tk()
└── README.md
```

## Persistencia

- `usuarios.json`, `productos.json`, `ventas.json` vía `ArchivoServicio` con `pathlib` (`Path(__file__).resolve().parent / "datos"` — rutas dinámicas, no quemadas).
- `Treeview` solo muestra representación; la fuente real es `RestauranteServicio`.

## Cómo ejecutar

1. Clonar el repositorio.
2. Tener **Python 3.14** + Tkinter (estándar) y `assets/` intacto.
3. Desde `restaurante_app/`:

```bash
python main.py
```

4. Iniciar sesión:
   - `admin / admin123` (Administrador)
   - `cajero / cajero123` (Empleado)
5. Como Administrador → Usuarios → probar: registrar Cliente/Empleado → seleccionar fila (carga) → Enter registra → Escape limpia → cambiar rol en Combobox → Actualizar / Eliminar con confirmación → cerrar y reabrir para verificar persistencia.

## Acceso de prueba

```
Administrador: admin / admin123
Empleado: cajero / cajero123
```

> Las claves no deben de ir al negocio tuyo — solo en sección "Acceso de prueba" del README.

## Principios mantenidos

Reutilización, abstracción, responsabilidad única y separación de responsabilidades. `definir_estilos()` + `construir_interfaz()`, `ttk.Style().theme_use("clam")`, un solo `tk.Tk()`, `command=` sin paréntesis, JSON solo vía servicios, `assets/` obligatorio.

## Autor

Pablo Sergio Quimi Pin — UEA — Programación Orientada a Objetos — Paralelo A — Semana 16
