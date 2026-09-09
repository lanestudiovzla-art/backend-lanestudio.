from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Sistema Multi-Empresa LAN ESTUDIO API")

# --- MODELOS DE DATOS ---
class CalculoDiferencial(BaseModel):
    saldo_bs: float
    tasa_registro: float
    tasa_actual: float

class ActualizarEtapaCRM(BaseModel):
    cliente_id: str
    nueva_etapa: str

class FacturaOCRInput(BaseModel):
    imagen_base64: str

# --- ENDPOINTS CORE ---

@app.get("/")
def estado_sistema():
    return {"status": "Sistema Operativo", "plataforma": "PWA Web Multi-tenant"}

@app.post("/api/finanzas/diferencial-cambiario")
def calcular_perdida_cambiaria(data: CalculoDiferencial):
    """
    Calcula el impacto en USD de tener Bolívares en caja ante una variación de la tasa BCV.
    """
    if data.tasa_registro <= 0 or data.tasa_actual <= 0:
        raise HTTPException(status_code=400, detail="Las tasas deben ser mayores a cero.")
    
    # Valor real en USD al momento de entrar el dinero vs Valor real en USD al día de hoy
    usd_inicial = data.saldo_bs / data.tasa_registro
    usd_actual = data.saldo_bs / data.tasa_actual
    
    diferencia_usd = usd_actual - usd_inicial  # Resultado negativo representa pérdida
    
    return {
        "saldo_bolivares": data.saldo_bs,
        "valor_inicial_usd": round(usd_inicial, 2),
        "valor_actual_usd": round(usd_actual, 2),
        "resultado_diferencial_usd": round(diferencia_usd, 2),
        "estado": "Pérdida Cambiaria" if diferencia_usd < 0 else "Ganancia / Estable"
    }

@app.post("/api/crm/mover-etapa")
def mover_etapa_crm(data: ActualizarEtapaCRM):
    """
    Actualiza la posición del cliente en el embudo Kanban de ventas.
    """
    etapas_validas = ["Prospecto", "Cotizado", "Aprobado", "Producción", "Listo para Entrega", "Cobrado"]
    if data.nueva_etapa not in etapas_validas:
        raise HTTPException(status_code=400, detail="Etapa no válida.")
    
    return {
        "mensaje": f"Cliente {data.cliente_id} movido exitosamente a '{data.nueva_etapa}'",
        "etapa_actual": data.nueva_etapa
    }

@app.post("/api/inventario/ocr-factura")
def procesar_factura_ia(data: FacturaOCRInput):
    """
    Simulación de procesamiento OCR vía IA para carga automática de facturas de proveedores.
    """
    # Integración directa con modelo de visión artificial (GPT-4o Vision / Google Vision)
    return {
        "proveedor": "Distribuidora de Acrílicos y Tintas C.A.",
        "productos_detectados": [
            {"nombre": "Lámina Acrílico 3mm Transparente", "tipo": "insumo", "cantidad": 10, "costo_unitario_usd": 35.00},
            {"nombre": "Tinta Eco-Solvente Negra 1L", "tipo": "insumo", "cantidad": 2, "costo_unitario_usd": 45.00}
        ],
        "total_detectado_usd": 440.00,
        "estatus": "Pendiente de aprobación en un clic"
    }
