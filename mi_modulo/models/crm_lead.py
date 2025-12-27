from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    # --- Agencia aduanal (ejemplo) ---
    x_tipo_operacion = fields.Selection(
        selection=[
            ("importacion", "Importación"),
            ("exportacion", "Exportación"),
        ],
        string="Tipo de operación",
    )

    x_regimen = fields.Selection(
        selection=[
            ("definitivo", "Definitivo"),
            ("temporal", "Temporal"),
            ("deposito_fiscal", "Depósito fiscal"),
            ("transito", "Tránsito"),
        ],
        string="Régimen",
    )

    x_aduana = fields.Char(string="Aduana")

    x_incoterm = fields.Selection(
        selection=[
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

    # --- Operación / mercancía (ejemplo) ---
    x_fraccion_arancelaria = fields.Char(string="Fracción arancelaria")

    x_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id,
    )

    x_valor_mercancia = fields.Monetary(
        string="Valor mercancía",
        currency_field="x_currency_id",
    )

    x_peso_kg = fields.Float(string="Peso (kg)")
