#!/bin/bash

################################################################################
# 🔧 CONSOLIDADOR DE RAMAS - NEURAFORGE AI
################################################################################
# Limpia, sincroniza y consolida todas las ramas
# Soluciona: commits duplicados, ramas obsoletas, conflictos
# Uso: ./consolidate_branches.sh
################################################################################

set -e

# ============================================================================
# COLORES
# ============================================================================
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

print_header() {
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC} $1"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════╝${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_section() {
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# ============================================================================
# PASO 1: VALIDAR REPOSITORIO
# ============================================================================

validate_repo() {
    print_section "PASO 1: Validando repositorio"
    
    if [ ! -d ".git" ]; then
        print_error "No es un repositorio Git"
        exit 1
    fi
    
    print_success "Es un repositorio Git válido"
    
    # Obtener nombre del repo
    REPO_NAME=$(git rev-parse --show-toplevel | xargs basename)
    print_info "Repositorio: $REPO_NAME"
}

# ============================================================================
# PASO 2: OBTENER ESTADO ACTUAL
# ============================================================================

get_status() {
    print_section "PASO 2: Estado Actual"
    
    print_info "Rama actual:"
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo -e "  ${CYAN}→ $CURRENT_BRANCH${NC}"
    
    print_info "Ramas locales:"
    git branch -v | sed 's/^/  /'
    
    print_info "Ramas remotas:"
    git branch -r -v | sed 's/^/  /'
    
    print_info "Estado de archivos:"
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "  ${YELLOW}Cambios sin stagear${NC}"
        git status --short | sed 's/^/    /'
    else
        echo -e "  ${GREEN}Sin cambios${NC}"
    fi
}

# ============================================================================
# PASO 3: LIMPIAR CAMBIOS LOCALES
# ============================================================================

cleanup_local_changes() {
    print_section "PASO 3: Limpieza Local"
    
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "Hay cambios sin guardar"
        
        read -p "¿Descartar cambios locales? (s/n): " confirm
        if [ "$confirm" = "s" ]; then
            git checkout -- .
            git clean -fd
            print_success "Cambios descartados"
        else
            print_warning "Abortado por el usuario"
            return 1
        fi
    else
        print_success "No hay cambios locales"
    fi
}

# ============================================================================
# PASO 4: SINCRONIZAR REMOTO
# ============================================================================

sync_remote() {
    print_section "PASO 4: Sincronizando con Remoto"
    
    print_info "Actualizando referencias remotas..."
    git fetch --all --prune
    print_success "Referencias actualizadas"
    
    print_info "Ramas en remoto origin:"
    git branch -r | grep "origin/" | sed 's/^/  /'
}

# ============================================================================
# PASO 5: DETECTAR RAMAS IMPORTANTES
# ============================================================================

detect_main_branch() {
    print_section "PASO 5: Detectando Rama Principal"
    
    # Buscar rama principal
    if git rev-parse --verify origin/main >/dev/null 2>&1; then
        MAIN_BRANCH="main"
    elif git rev-parse --verify origin/master >/dev/null 2>&1; then
        MAIN_BRANCH="master"
    elif git rev-parse --verify origin/masterAI >/dev/null 2>&1; then
        MAIN_BRANCH="masterAI"
    else
        MAIN_BRANCH=$(git rev-parse --abbrev-ref origin/HEAD | sed 's|origin/||')
    fi
    
    print_success "Rama principal: $MAIN_BRANCH"
}

# ============================================================================
# PASO 6: ANALIZAR RAMAS
# ============================================================================

analyze_branches() {
    print_section "PASO 6: Analizando Ramas"
    
    print_info "Commits adelantados por rama:"
    
    for branch in $(git branch | sed 's/^ *//'); do
        if [ "$branch" != "$MAIN_BRANCH" ]; then
            AHEAD=$(git rev-list --count origin/$MAIN_BRANCH..$branch 2>/dev/null || echo "0")
            BEHIND=$(git rev-list --count $branch..origin/$MAIN_BRANCH 2>/dev/null || echo "0")
            
            if [ "$AHEAD" -gt 0 ] || [ "$BEHIND" -gt 0 ]; then
                echo -e "  ${CYAN}$branch${NC}: ${GREEN}↑$AHEAD${NC} ${RED}↓$BEHIND${NC}"
            fi
        fi
    done
}

# ============================================================================
# PASO 7: CONSOLIDAR RAMAS
# ============================================================================

consolidate_branches() {
    print_section "PASO 7: Consolidando Ramas"
    
    print_info "Cambiando a rama principal: $MAIN_BRANCH"
    git checkout $MAIN_BRANCH
    
    print_info "Descargando últimos cambios..."
    git pull origin $MAIN_BRANCH --ff-only 2>/dev/null || git pull origin $MAIN_BRANCH
    
    print_success "Rama principal actualizada"
    
    # Consolidar ramas de feature
    print_info "Procesando ramas de feature..."
    
    for branch in $(git branch | sed 's/^ *//'); do
        if [ "$branch" = "$MAIN_BRANCH" ] || [ "$branch" = "HEAD" ]; then
            continue
        fi
        
        COMMITS_AHEAD=$(git rev-list --count origin/$MAIN_BRANCH..$branch 2>/dev/null || echo "0")
        
        if [ "$COMMITS_AHEAD" -gt 0 ]; then
            echo -e "  ${YELLOW}→ Mergeando $branch${NC}"
            
            git merge --no-edit $branch || {
                print_warning "Conflicto en $branch. Resolviendo..."
                git merge --abort
                continue
            }
        else
            echo -e "  ${GRAY}→ $branch sin cambios${NC}"
        fi
    done
    
    print_success "Consolidación completada"
}

# ============================================================================
# PASO 8: LIMPIAR RAMAS OBSOLETAS
# ============================================================================

cleanup_branches() {
    print_section "PASO 8: Limpieza de Ramas"
    
    print_info "Eliminando ramas merged:"
    
    DELETED_COUNT=0
    
    for branch in $(git branch | sed 's/^ *//'); do
        if [ "$branch" = "$MAIN_BRANCH" ] || [ "$branch" = "HEAD" ]; then
            continue
        fi
        
        # Verificar si está merged en main
        if git merge-base --is-ancestor $branch $MAIN_BRANCH 2>/dev/null; then
            read -p "¿Eliminar rama $branch? (s/n): " confirm
            if [ "$confirm" = "s" ]; then
                git branch -d $branch
                echo -e "  ${GREEN}✓ $branch eliminada${NC}"
                ((DELETED_COUNT++))
            fi
        fi
    done
    
    if [ $DELETED_COUNT -gt 0 ]; then
        print_success "$DELETED_COUNT ramas eliminadas"
    else
        print_info "No hay ramas para eliminar"
    fi
}

# ============================================================================
# PASO 9: ELIMINAR DUPLICADOS
# ============================================================================

remove_duplicates() {
    print_section "PASO 9: Eliminando Commits Duplicados"
    
    print_info "Buscando commits duplicados..."
    
    # Obtener hash de commits en main
    MAIN_COMMITS=$(git rev-list $MAIN_BRANCH)
    
    # Buscar en otras ramas
    DUPLICATES=0
    for commit in $MAIN_COMMITS; do
        if git log --oneline | grep -q "^${commit:0:7}"; then
            ((DUPLICATES++))
        fi
    done
    
    if [ $DUPLICATES -gt 0 ]; then
        print_warning "Se encontraron $DUPLICATES commits posiblemente duplicados"
        print_info "Ejecutar: git log --oneline $MAIN_BRANCH | sort | uniq -d"
    else
        print_success "No hay duplicados detectados"
    fi
}

# ============================================================================
# PASO 10: SINCRONIZAR CON REMOTO
# ============================================================================

final_sync() {
    print_section "PASO 10: Sincronización Final"
    
    print_info "Subiendo cambios a origin/$MAIN_BRANCH..."
    
    if git push origin $MAIN_BRANCH; then
        print_success "Push completado exitosamente"
    else
        print_warning "No se pudo hacer push (posible divergencia)"
        print_info "Intenta: git push origin $MAIN_BRANCH --force-with-lease"
    fi
    
    print_info "Sincronizando tags..."
    git fetch --tags
    git push origin --tags || print_warning "Algunos tags no se pudieron subir"
    
    print_success "Sincronización completada"
}

# ============================================================================
# RESUMEN FINAL
# ============================================================================

final_report() {
    print_section "RESUMEN FINAL"
    
    echo ""
    print_info "Estado del repositorio:"
    echo -e "  ${CYAN}Rama actual:${NC} $(git rev-parse --abbrev-ref HEAD)"
    echo -e "  ${CYAN}Commits locales:${NC} $(git rev-list --count origin/$MAIN_BRANCH..HEAD)"
    echo -e "  ${CYAN}Commits remotos:${NC} $(git rev-list --count HEAD..origin/$MAIN_BRANCH)"
    
    echo ""
    print_info "Ramas locales:"
    git branch -v | sed 's/^/  /'
    
    echo ""
    print_success "¡Consolidación completada!"
    echo ""
    print_info "Próximos pasos:"
    echo "  1. Verifica los cambios: git log --oneline -10"
    echo "  2. Prueba la aplicación"
    echo "  3. Haz pull en otros repositorios clonados"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    clear
    print_header "🔧 CONSOLIDADOR DE RAMAS - NEURAFORGE AI"
    echo ""
    print_info "Este script sincronizará y consolidará todas tus ramas"
    echo ""
    
    # Validar
    validate_repo
    echo ""
    
    # Obtener estado
    get_status
    echo ""
    
    # Confirmar inicio
    read -p "¿Deseas continuar? (s/n): " start_confirm
    if [ "$start_confirm" != "s" ]; then
        print_warning "Abortado por el usuario"
        exit 0
    fi
    echo ""
    
    # Ejecutar pasos
    cleanup_local_changes || exit 1
    echo ""
    
    sync_remote
    echo ""
    
    detect_main_branch
    echo ""
    
    analyze_branches
    echo ""
    
    consolidate_branches
    echo ""
    
    cleanup_branches
    echo ""
    
    remove_duplicates
    echo ""
    
    final_sync
    echo ""
    
    final_report
}

# Ejecutar
main "$@"
