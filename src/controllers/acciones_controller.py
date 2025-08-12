from flask import Blueprint, jsonify
from src.models import session as db_session
from src.models.detalle_factura import DetalleFactura
from src.models.factura import Factura
from src.models.usuarios import usuario
from src.models.productos import Producto
from datetime import datetime, timezone

acciones_bp = Blueprint('acciones', __name__)


@acciones_bp.route('/eliminar_detalle/<int:id_detalle>', methods=['POST'])
def eliminar_detalle(id_detalle):
    detalle = db_session.get(DetalleFactura, id_detalle)
    if not detalle:
        return jsonify(success=False, error="detalle no encontrado"), 404

    try:
        db_session.delete(detalle)
        db_session.commit()
        return jsonify(success=True)
    except Exception as e:
        db_session.rollback()
        return jsonify(success=False, error=str(e)), 500


@acciones_bp.route('/eliminar_factura/<int:id_factura>', methods=['POST'])
def eliminar_factura(id_factura):
    factura = db_session.get(Factura, id_factura)
    if not factura:
        return jsonify(success=False, error="factura no encontrada"), 404

    try:
        db_session.delete(factura)
        db_session.commit()
        return jsonify(success=True)
    except Exception as e:
        db_session.rollback()
        return jsonify(success=False, error=str(e)), 500


@acciones_bp.route('/usuario/soft_delete/<int:id_usuario>', methods=['POST'])
def usuario_soft_delete(id_usuario):
    usuario_obj = db_session.get(usuario, id_usuario)
    if not usuario_obj:
        return jsonify(success=False, error="usuario no encontrado"), 404

    # <-- OPCIÓN: permitir marcar como inactivo aunque tenga facturas.
    # Si deseas impedirlo, descomenta la comprobación y devuelve error.
    # emitidas = db_session.query(Factura).filter_by(id_empleado=id_usuario).count()
    # recibidas = db_session.query(Factura).filter_by(id_cliente=id_usuario).count()
    # if emitidas or recibidas:
    #     return jsonify(success=False, error="El usuario tiene facturas relacionadas"), 400

    try:
        usuario_obj.activo = False
        usuario_obj.deleted_at = datetime.now(timezone.utc)   # CORRECCIÓN: deleted_at (no deletead_at)
        db_session.commit()
        return jsonify(success=True)
    except Exception as e:
        db_session.rollback()
        return jsonify(success=False, error=str(e)), 500


@acciones_bp.route('/usuario/restore/<int:id_usuario>', methods=['POST'])
def usuario_restore(id_usuario):
    usuario_obj = db_session.get(usuario, id_usuario)
    if not usuario_obj:
        return jsonify(success=False, error="Usuario no encontrado"), 404
    try:
        usuario_obj.activo = True
        usuario_obj.deleted_at = None
        db_session.commit()
        return jsonify(success=True)
    except Exception as e:
        db_session.rollback()
        return jsonify(success=False, error=str(e)), 500


@acciones_bp.route('/usuario/hard_delete/<int:id_usuario>', methods=['POST'])
def usuario_hard_delete(id_usuario):
    usuario_obj = db_session.get(usuario, id_usuario)
    if not usuario_obj:
        return jsonify(success=False, error="Usuario no encontrado"), 404

    # Comprobación para prevenir borrado si hay facturas
    emitidas = db_session.query(Factura).filter_by(id_empleado=id_usuario).count()
    recibidas = db_session.query(Factura).filter_by(id_cliente=id_usuario).count()
    if emitidas or recibidas:
        return jsonify(
            success=False,
            error="No se puede eliminar permanentemente: usuario tiene facturas relacionadas",
            detalles={"facturas_emitidas": emitidas, "facturas_recibidas": recibidas}
        ), 400

    try:
        db_session.delete(usuario_obj)
        db_session.commit()
        return jsonify(success=True)
    except Exception as e:
        db_session.rollback()
        return jsonify(success=False, error=str(e)), 500


@acciones_bp.route('/producto/soft_delete/<int:id_producto>', methods=['POST'])
def producto_soft_delete(id_producto):
    producto_obj = db_session.get(Producto, id_producto)
    if not producto_obj:
        return jsonify(success=False, error="producto no encontrado"), 404

    detalles_count = db_session.query(DetalleFactura).filter_by(id_producto=id_producto).count()
    if detalles_count:
        return jsonify(
            success=False,
            error="no se puede inactivar: producto está en detalles de facturas",
            detalles={"detalles": detalles_count}
        ), 400

    try:
        producto_obj.activo = False
        producto_obj.deleted_at = datetime.now(timezone.utc)   # CORRECCIÓN: deleted_at
        db_session.commit()
        return jsonify(success=True)
    except Exception as e:
        db_session.rollback()
        return jsonify(success=False, error=str(e)), 500


@acciones_bp.route('/producto/restore/<int:id_producto>', methods=['POST'])
def producto_restore(id_producto):
    producto_obj = db_session.get(Producto, id_producto)
    if not producto_obj:
        return jsonify(success=False, error="Producto no encontrado"), 404
    try:
        producto_obj.activo = True
        producto_obj.deleted_at = None
        db_session.commit()
        return jsonify(success=True)
    except Exception as e:
        db_session.rollback()
        return jsonify(success=False, error=str(e)), 500
