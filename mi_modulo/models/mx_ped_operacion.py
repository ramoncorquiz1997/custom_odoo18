# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


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

    # ==========================
    # Clasificación
    # ==========================
    tipo_operacion = fields.Selection(
        [("importacion", "Importación"), ("exportacion", "Exportación")],
        string="Tipo",
    )
    regimen = fields.Selection(
        [
            ("definitivo", "Definitivo"),
            ("temporal", "Temporal"),
            ("deposito_fiscal", "Depósito fiscal"),
            ("transito", "Tránsito"),
        ],
        string="Régimen",
    )
    incoterm = fields.Selection(
        [
            ("EXW", "EXW"),
            ("FCA", "FCA"),
            ("FOB", "FOB"),
            ("CFR", "CFR"),
            ("CIF", "CIF"),
            ("DAP", "DAP"),
            ("DDP", "DDP"),
        ],
        string="Incoterm",
    )

    aduana_clave = fields.Char(string="Aduana (clave)")  # ej 070
    patente = fields.Char(string="Patente")
    clave_pedimento = fields.Char(string="Clave pedimento")

    # ==========================
    # Resultado oficial/operativo
    # ==========================
    pedimento_numero = fields.Char(string="Número de pedimento")
    fecha_pago = fields.Date(string="Fecha de pago")
    fecha_liberacion = fields.Date(string="Fecha de liberación")
    semaforo = fields.Selection(
        [("verde", "Verde"), ("rojo", "Rojo")],
        string="Semáforo",
    )

    # Moneda
    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    observaciones = fields.Text(string="Observaciones")

    # ==========================
    # Partidas / Mercancías
    # ==========================
    partida_ids = fields.One2many(
        comodel_name="mx.ped.partida",
        inverse_name="operacion_id",
        string="Partidas / Mercancías",
        copy=True,
    )

    partida_count = fields.Integer(
        string="Partidas",
        compute="_compute_partida_count",
    )

    @api.depends("partida_ids")
    def _compute_partida_count(self):
        for rec in self:
            rec.partida_count = len(rec.partida_ids)

    def action_view_partidas(self):
        """Abre las partidas de esta operación (útil para smart button)."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Partidas"),
            "res_model": "mx.ped.partida",
            "view_mode": "list,form",
            "domain": [("operacion_id", "=", self.id)],
            "context": {"default_operacion_id": self.id},
            "target": "current",
        }