# Documentación OPN - Sistema de Build & Package Management

## Descripción

Documentación profesional y moderna del sistema de compilación, empaquetado y gestión de imports de OPN.

## Características

✅ **Diseño Responsivo** - Se adapta a todos los tamaños de pantalla (desktop, tablet, móvil)
✅ **Tema Oscuro/Claro** - Toggle de tema con persistencia en localStorage
✅ **Navegación Intuitiva** - Menú lateral con búsqueda integrada
✅ **Separación por Temas** - 8 secciones principales en una sola página
✅ **Estilos Profesionales** - Gradientes, transiciones suaves y efectos modernos
✅ **Tipografía Premium** - Inter para UI y Fira Code para código
✅ **Accesibilidad** - Contraste adecuado y navegación por teclado

## Estructura de Archivos

```
docs/html/
├── index.html              # Página principal (única página HTML)
├── styles/
│   └── main.css            # Estilos completos y responsivos
├── js/
│   └── script.js           # Lógica de navegación y temas
└── README.md              # Este archivo
```

## Secciones Incluidas

1. **Bienvenida** - Introducción al sistema y características principales
2. **Sistema de Build** - Compilación automática de proyectos OPN
3. **Guía de Compilación** - Referencia detallada de todos los comandos
4. **Referencia Rápida** - Cheat sheet con comandos más usados
5. **Resumen del Sistema** - Arquitectura e implementación
6. **Configuración** - Gestión centralizada de config en ~/.opn/config/
7. **Sistema de Imports** - Cómo importar y usar paquetes OPN
8. **Solución de Problemas** - FAQs y soluciones comunes

## Cómo Usar

### Abrir la Documentación

1. Abre `index.html` en tu navegador:
   - Doble clic en `index.html`
   - O arrastra el archivo a tu navegador
   - O usa un servidor web local: `python -m http.server 8000` y accede a `http://localhost:8000/docs/html/`

2. La página se cargará con:
   - Menú lateral con navegación
   - Búsqueda integrada
   - Toggle de tema oscuro/claro
   - Contenido formateado y profesional

### Navegación

- **Menú Lateral**: Haz clic en cualquier sección para cambiar de tema
- **Búsqueda**: Escribe en la barra de búsqueda para filtrar contenido
- **Tema**: Haz clic en el ícono de luna/sol para cambiar entre modo oscuro y claro
- **Enlaces Internos**: Los enlaces dentro de la documentación navegan entre secciones

## Características de Diseño

### Colores
- **Primario**: #6366f1 (Índigo)
- **Secundario**: #ec4899 (Rosa)
- **Fondo Oscuro**: #0a0e27
- **Fondo Claro**: #f8fafc
- **Éxito**: #10b981 (Verde)
- **Advertencia**: #f59e0b (Naranja)

### Tipografía
- **Títulos**: Inter 700 (Bold)
- **Cuerpo**: Inter 400 (Regular)
- **Código**: Fira Code 400

### Componentes
- **Cards**: Bordes sutiles con hover effect
- **Badges**: Para destacar estados (success, warning, danger)
- **Code Blocks**: Sintaxis resaltada con fondo oscuro
- **Tablas**: Responsivas con hover effects
- **Alertas**: Example boxes y warning boxes

## Personalización

### Cambiar Colores
Edita las variables CSS en `styles/main.css`:

```css
:root {
  --primary-color: #6366f1;
  --secondary-color: #ec4899;
  /* ... más colores */
}
```

### Cambiar Fuentes
Modifica las importaciones de Google Fonts en `index.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Tu+Fuente:wght@400;600;700&display=swap" rel="stylesheet">
```

### Agregar Nuevas Secciones
1. Crea un nuevo `<div id="nueva-seccion" class="content-section">` en `index.html`
2. Agrega un enlace en el menú: `<a href="#nueva-seccion" class="nav-link">Nueva Sección</a>`
3. Agrega el contenido dentro del div
4. El JavaScript se encargará automáticamente de la navegación

## Responsividad

La documentación es completamente responsiva:

- **Desktop** (>1024px): Menú lateral visible, contenido ancho
- **Tablet** (768px - 1024px): Menú lateral reducido, contenido optimizado
- **Móvil** (<768px): Menú lateral oculto (puede abrirse), contenido full-width

## Navegadores Soportados

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

La documentación es muy ligera:
- Una sola página HTML (~45 KB)
- CSS optimizado (~25 KB)
- JavaScript minimal (~3 KB)
- **Total**: ~73 KB (sin contar fuentes externas)

## Mejoras Futuras

- [ ] Sistema de búsqueda más avanzado
- [ ] Tabla de contenidos automática
- [ ] Sintaxis highlighting para código
- [ ] Dark mode automático basado en preferencias del sistema
- [ ] Exportar a PDF
- [ ] Versiones de la documentación

## Notas

- La documentación está completamente contenida en un solo archivo HTML
- No requiere servidor backend
- No requiere build process
- Funciona offline
- Compatible con dispositivos móviles
- Accesible con teclado

---

**Versión**: 1.0.0
**Última actualización**: 2025-11-12
**Estado**: ✅ Completo y Funcional
