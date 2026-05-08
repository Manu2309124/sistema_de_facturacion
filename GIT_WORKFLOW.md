# Estructura de Ramas Git - Sistema de Facturación

## 📋 Descripción

Este proyecto usa **Git Flow** como estrategia de branching. Las ramas principales son:

### Ramas Permanentes

#### `main` (Producción)

- **Propósito**: Código estable listo para producción
- **Protección**: Cambios solo mediante Pull Requests desde `develop`
- **Versiones**: Etiquetadas con tags (v1.0.0, v1.1.0, etc.)
- **Acceso**: Solo cambios desde `develop` después de testing

#### `develop` (Desarrollo)

- **Propósito**: Integración continua de features
- **Estado**: Código funcional pero en desarrollo
- **Uso**: Rama base para features y bugfixes
- **Deploy**: A staging/pre-producción
- **Flujo**: `develop` ← `feature/*`, `bugfix/*`, `hotfix/*`

### Ramas Temporales

#### `feature/*` (Nuevas Funcionalidades)

```bash
# Crear feature desde develop
git checkout develop
git pull origin develop
git checkout -b feature/nombre-feature

# Trabajar, hacer commits
git add .
git commit -m "feat: descripción"

# Subir feature
git push -u origin feature/nombre-feature

# Hacer Pull Request a develop (en GitHub)
```

Ejemplos:

- `feature/sistema-pagos`
- `feature/reportes-pdf`
- `feature/autenticacion`

#### `bugfix/*` (Correcciones)

```bash
# Crear bugfix desde develop
git checkout develop
git pull origin develop
git checkout -b bugfix/nombre-bugfix

# Corregir, hacer commits
git add .
git commit -m "fix: descripción"

# Subir bugfix
git push -u origin bugfix/nombre-bugfix

# Hacer Pull Request a develop
```

Ejemplos:

- `bugfix/error-calculos`
- `bugfix/conexion-bd`

#### `hotfix/*` (Correcciones Críticas en Producción)

```bash
# Crear hotfix desde main (¡IMPORTANTE!)
git checkout main
git pull origin main
git checkout -b hotfix/nombre-hotfix

# Corregir, hacer commits
git add .
git commit -m "hotfix: descripción crítica"

# Subir hotfix
git push -u origin hotfix/nombre-hotfix

# Hacer Pull Request a main
# Y luego TAMBIÉN a develop
```

Ejemplos:

- `hotfix/seguridad-critica`
- `hotfix/error-facturacion`

---

## 🚀 Flujo de Trabajo (Git Flow)

```
main (producción)
  ↑
  ├─ v1.0.0 (tag)
  │
develop (integración continua)
  ↑
  ├─ feature/nueva-funcionalidad
  ├─ feature/otro-feature
  ├─ bugfix/error-importante
  └─ hotfix/* (desde main)
```

---

## 📝 Comandos Principales

### Configuración Inicial

```bash
# Clonar repositorio
git clone https://github.com/Manu2309124/sistema_de_facturacion.git

# Cambiar a rama develop
git checkout develop

# Descargar cambios de develop
git pull origin develop
```

### Crear y Trabajar en Feature

```bash
# 1. Crear feature basada en develop
git checkout develop
git pull origin develop
git checkout -b feature/mi-feature

# 2. Hacer cambios y commits
git add .
git commit -m "feat: descripción de cambios"
git commit -m "feat: más cambios"

# 3. Subir feature al remoto
git push -u origin feature/mi-feature

# 4. Crear Pull Request en GitHub
# (Cambiar base a 'develop', no a 'main')

# 5. Después de merge, eliminar rama local
git checkout develop
git pull origin develop
git branch -d feature/mi-feature
git push origin --delete feature/mi-feature
```

### Actualizar Feature con Cambios de Develop

```bash
# En tu rama feature
git fetch origin
git rebase origin/develop

# O si prefieres merge
git merge origin/develop

# Resolver conflictos si los hay
# Hacer commit y push
git push origin feature/mi-feature
```

### Sincronizar Local con Remoto

```bash
# Descargar todos los cambios
git fetch --all

# Ver estado de branches
git branch -vv

# Actualizar develop local
git checkout develop
git pull origin develop
```

---

## ✅ Checklist de Workflow

### Antes de Crear Feature

- [ ] Estoy en rama `develop`
- [ ] `develop` está actualizado: `git pull origin develop`
- [ ] No hay cambios sin commit: `git status`
- [ ] Creo rama con nombre descriptivo

### Mientras Desarrollo

- [ ] Commits frecuentes con mensajes claros
- [ ] Mensajes en formato: `feat:`, `fix:`, `docs:`, etc.
- [ ] Pruebas locales funcionando
- [ ] Código formateado

### Antes de Push

- [ ] Todos los cambios están staged: `git add .`
- [ ] Commits tienen mensajes descriptivos
- [ ] Actualizaciones de develop sincronizadas: `git fetch origin`
- [ ] No hay conflictos: `git status`

### Pull Request

- [ ] Base: `develop` (NO `main`)
- [ ] Descripción clara de cambios
- [ ] Reference a issues si aplica (#123)
- [ ] Code review realizado
- [ ] Tests pasando
- [ ] Merge a develop
- [ ] Eliminar rama remota después de merge

---

## 🔄 Convención de Commits

Usar formato Conventional Commits:

```bash
# Nuevas funcionalidades
git commit -m "feat: agregar sistema de pagos"

# Correcciones de bugs
git commit -m "fix: corregir cálculo de impuestos"

# Documentación
git commit -m "docs: actualizar README"

# Mejoras de código
git commit -m "refactor: optimizar queries de BD"

# Tests
git commit -m "test: agregar tests para pagos"

# Cambios de configuración
git commit -m "chore: actualizar dependencias"
```

---

## 🎯 Ramas Actuales

```
Locales:
  * develop  (RAMA DE TRABAJO ACTUAL)
    main

Remotas:
  origin/develop
  origin/main
```

---

## 📌 Notas Importantes

1. **NUNCA hacer commit directo a `main` o `develop`**
   - Siempre usar ramas `feature/*` o `bugfix/*`
   - Cambios a través de Pull Requests

2. **Pull Requests deben apuntar a `develop`**
   - Solo si son hotfixes críticos, apuntar a `main`
   - Y luego crear PR desde `main` a `develop`

3. **Mantener `develop` siempre funcional**
   - Tests deben pasar
   - Código debe ser compilable
   - Sin errores críticos

4. **Tags en `main` para versiones**

   ```bash
   git tag -a v1.0.0 -m "Versión 1.0.0 - Inicial"
   git push origin v1.0.0
   ```

5. **Sincronizar frecuentemente**
   ```bash
   git fetch --all
   git pull origin develop
   ```

---

## 🆘 Problemas Comunes

### "Your branch is behind"

```bash
# Actualizar rama local
git pull origin develop
```

### "Conflictos al hacer merge"

```bash
# Ver conflictos
git status

# Resolver en editor, luego
git add .
git commit -m "fix: resolver conflictos de merge"
git push origin feature/mi-feature
```

### "Quiero eliminar cambios locales"

```bash
# Descartar cambios en archivo
git checkout -- app/models.py

# Descartar todos los cambios
git reset --hard origin/develop
```

### "Necesito cambiar de rama sin hacer commit"

```bash
# Guardar cambios temporalmente
git stash

# Cambiar de rama
git checkout develop

# Recuperar cambios
git stash pop
```

---

## 📚 Recursos

- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

---

**¡Rama develop configurada y lista para usar!** 🚀
