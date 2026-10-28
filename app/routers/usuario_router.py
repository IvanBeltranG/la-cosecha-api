from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import SesionDB
from app.schemas.usuario_schema import UsuarioCrear, UsuarioEstado, UsuarioRespuesta
from app.seguridad.dependencias import UsuarioActual, exigir_admin
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(exigir_admin)])


@router.get("/", response_model=list[UsuarioRespuesta])
def listar(db: SesionDB):
    return usuario_service.listar_usuarios(db)


@router.post("/", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def crear(datos: UsuarioCrear, db: SesionDB):
    if usuario_service.buscar_por_correo(db, datos.correo) is not None:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese correo")
    return usuario_service.crear_usuario(db, datos)


@router.patch("/{usuario_id}/estado", response_model=UsuarioRespuesta)
def cambiar_estado(usuario_id: int, datos: UsuarioEstado, db: SesionDB, actual: UsuarioActual):
    usuario = usuario_service.buscar_usuario(db, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.id == actual.id:
        raise HTTPException(status_code=409, detail="No puedes desactivar tu propia cuenta")
    return usuario_service.cambiar_estado(db, usuario, datos.activo)