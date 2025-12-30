from odoo import fields, models


class MxPedOperacion(models.Model):
    _name = "mx.ped.operacion"
    _description = "Pedimento / Operación Aduanera"
    _order = "create_date desc, id desc"

    lead_id = fields.Many2one(
        comodel_name="crm.lead",
        string="Operación (Lead)",
        required=True,
        ondelete="cascade",
        index=True,
    )

    name = fields.Char(string="Referencia", required=True)

    # Clasificación (lo que te interesa para armar layout)
    tipo_operacion = fields.Selection(
        [("importacion", "Importación"), ("exportacion", "Exportación")],
        string="Tipo",
    )
    regimen = fields.Selection(
        [("definitivo", "Definitivo"), ("temporal", "Temporal"), ("deposito_fiscal", "Depósito fiscal"), ("transito", "Tránsito")],
        string="Régimen",
    )
    incoterm = fields.Selection(
        [("EXW", "EXW"), ("FCA", "FCA"), ("FOB", "FOB"), ("CFR", "CFR"), ("CIF", "CIF"), ("DAP", "DAP"), ("DDP", "DDP")],
        string="Incoterm",
    )

    aduana_clave = fields.Char(string="Aduana (clave)")  # ej 070
    patente = fields.Char(string="Patente")
    clave_pedimento = fields.Char(string="Clave pedimento")

    # Resultado oficial/operativo
    pedimento_numero = fields.Char(string="Número de pedimento")
    fecha_pago = fields.Date(string="Fecha de pago")
    fecha_liberacion = fields.Date(string="Fecha de liberación")
    semaforo = fields.Selection([("verde", "Verde"), ("rojo", "Rojo")], string="Semáforo")

    currency_id = fields.Many2one("res.currency", string="Moneda", required=True)
    observaciones = fields.Text(string="Observaciones")