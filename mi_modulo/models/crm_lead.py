from odoo import api, fields, models


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

    # --- Identificación / responsables ---
    x_folio_operacion = fields.Char(string="Folio interno")
    x_referencia_cliente = fields.Char(string="Referencia del cliente")

    x_ejecutivo_id = fields.Many2one(
        comodel_name="res.users",
        string="Ejecutivo / Atención",
    )

    x_prioridad_operativa = fields.Selection(
        selection=[
            ("normal", "Normal"),
            ("urgente", "Urgente"),
        ],
        string="Prioridad",
        default="normal",
    )

    # --- Clasificación / aduana (complemento) ---
    x_patente_agente = fields.Char(string="Patente / Agente")

    x_tipo_despacho = fields.Selection(
        selection=[
            ("definitivo", "Definitivo"),
            ("temporal", "Temporal"),
            ("retorno", "Retorno"),
            ("deposito_fiscal", "Depósito fiscal"),
            ("transito", "Tránsito"),
        ],
        string="Tipo de despacho",
    )

    x_clave_pedimento = fields.Char(string="Clave de pedimento")

    x_fraccion_arancelaria_principal = fields.Char(string="Fracción arancelaria principal")
    x_descripcion_mercancia = fields.Text(string="Descripción de mercancía")

    # --- Logística / embarque ---
    x_modo_transporte = fields.Selection(
        selection=[
            ("terrestre", "Terrestre"),
            ("aereo", "Aéreo"),
            ("maritimo", "Marítimo"),
            ("ferro", "Ferroviario"),
        ],
        string="Modo de transporte",
    )

    x_pais_origen_id = fields.Many2one(
        comodel_name="res.country",
        string="País de origen",
    )

    x_pais_destino_id = fields.Many2one(
        comodel_name="res.country",
        string="País de destino",
    )

    x_lugar_carga = fields.Char(string="Lugar de carga")
    x_lugar_descarga = fields.Char(string="Lugar de descarga")

    x_fecha_estimada_arribo = fields.Date(string="Fecha estimada de arribo")
    x_fecha_estimada_salida = fields.Date(string="Fecha estimada de salida")

    x_fecha_recoleccion = fields.Date(string="Fecha de recolección")
    x_fecha_entrega = fields.Date(string="Fecha de entrega")

    # --- Partes involucradas ---
    x_exportador_id = fields.Many2one("res.partner", string="Exportador")
    x_exportador_name = fields.Char(string="Exportador (texto)")

    x_importador_id = fields.Many2one("res.partner", string="Importador")
    x_importador_name = fields.Char(string="Importador (texto)")

    x_proveedor_id = fields.Many2one("res.partner", string="Proveedor")
    x_proveedor_name = fields.Char(string="Proveedor (texto)")

    x_consignatario_name = fields.Char(string="Consignatario")
    x_destinatario_final_name = fields.Char(string="Destinatario final")

    # --- Documentos / control documental ---
    x_docs_requeridos_ids = fields.Many2many(
        comodel_name="crm.tag",
        relation="crm_lead_docs_requeridos_tag_rel",
        column1="lead_id",
        column2="tag_id",
        string="Documentos requeridos",
    )

    x_docs_faltantes_text = fields.Text(string="Documentos faltantes")

    x_docs_completos = fields.Boolean(
        string="Documentación completa",
        compute="_compute_x_docs_completos",
        store=True,
    )

    x_visible_portal = fields.Boolean(string="Visible en portal", default=True)

    @api.depends("x_docs_faltantes_text")
    def _compute_x_docs_completos(self):
        for rec in self:
            rec.x_docs_completos = not bool((rec.x_docs_faltantes_text or "").strip())

    # --- Valores y cantidades ---
    x_valor_factura = fields.Monetary(
        string="Valor factura (total)",
        currency_field="x_currency_id",
    )

    x_valor_aduana_estimado = fields.Monetary(
        string="Valor aduana (estimado)",
        currency_field="x_currency_id",
    )

    x_bultos = fields.Integer(string="Bultos")
    x_peso_bruto = fields.Float(string="Peso bruto")
    x_peso_neto = fields.Float(string="Peso neto")
    x_volumen_cbm = fields.Float(string="Volumen (CBM)")

    x_tipo_empaque = fields.Selection(
        selection=[
            ("cajas", "Cajas"),
            ("tarimas", "Tarimas"),
            ("granel", "Granel"),
            ("otro", "Otro"),
        ],
        string="Tipo de empaque",
    )

    x_numero_paquetes = fields.Integer(string="Número de paquetes")

    # --- Transporte / guías ---
    x_bl_awb = fields.Char(string="BL / AWB (Master)")
    x_house_bl_awb = fields.Char(string="House BL / AWB")
    x_booking = fields.Char(string="Booking")
    x_num_contenedor = fields.Char(string="Número de contenedor")
    x_num_sello = fields.Char(string="Número de sello")

    # --- Pedimento / resultado ---
    x_num_pedimento = fields.Char(string="Número de pedimento")
    x_fecha_pago_pedimento = fields.Date(string="Fecha de pago pedimento")
    x_fecha_liberacion = fields.Date(string="Fecha de liberación")

    x_semaforo = fields.Selection(
        selection=[
            ("verde", "Verde"),
            ("rojo", "Rojo"),
        ],
        string="Semáforo",
    )

    x_incidente_text = fields.Text(string="Incidencias")

    # --- Costos / facturación agencia ---
    x_cotizacion_total = fields.Monetary(
        string="Cotización total",
        currency_field="x_currency_id",
    )

    x_costo_estimado = fields.Monetary(
        string="Costo estimado",
        currency_field="x_currency_id",
    )

    x_factura_emitida = fields.Boolean(string="Factura emitida")
    x_factura_ref = fields.Char(string="Folio de factura")

    x_metodo_cobro = fields.Selection(
        selection=[
            ("transferencia", "Transferencia"),
            ("efectivo", "Efectivo"),
            ("credito", "Crédito"),
            ("otro", "Otro"),
        ],
        string="Método de cobro",
    )

    x_pago_confirmado = fields.Boolean(string="Pago confirmado")

    # --- Importación (extras) ---
    x_purchase_order = fields.Char(string="PO / Orden de compra")
    x_proveedor_invoice_number = fields.Char(string="Factura proveedor (número)")
    x_condiciones_pago = fields.Text(string="Condiciones de pago")

    x_tipo_compra = fields.Selection(
        selection=[
            ("materia_prima", "Materia prima"),
            ("refaccion", "Refacción"),
            ("maquinaria", "Maquinaria"),
            ("consumo", "Consumo"),
            ("otro", "Otro"),
        ],
        string="Tipo de compra",
    )

    x_permisos_ids = fields.Many2many(
        comodel_name="crm.tag",
        relation="crm_lead_permisos_tag_rel",
        column1="lead_id",
        column2="tag_id",
        string="Permisos / regulaciones (import)",
    )

    x_normas_noms_text = fields.Text(string="NOM / Normas aplicables")
    x_etiquetado = fields.Boolean(string="Requiere etiquetado")

    x_cumplimiento_noms = fields.Selection(
        selection=[
            ("pendiente", "Pendiente"),
            ("cumple", "Cumple"),
            ("no_aplica", "No aplica"),
        ],
        string="Cumplimiento NOM",
    )

    x_certificado_origen = fields.Boolean(string="Certificado de origen")
    x_tratado_aplicable = fields.Char(string="Tratado aplicable")
    x_pedimento_rectificacion = fields.Boolean(string="Pedimento en rectificación")

    x_iva_estimado = fields.Monetary(string="IVA estimado", currency_field="x_currency_id")
    x_igi_estimado = fields.Monetary(string="IGI estimado", currency_field="x_currency_id")
    x_dta_estimado = fields.Monetary(string="DTA estimado", currency_field="x_currency_id")
    x_prv_estimado = fields.Monetary(string="PRV estimado", currency_field="x_currency_id")

    x_total_impuestos_estimado = fields.Monetary(
        string="Total impuestos (estimado)",
        currency_field="x_currency_id",
    )

    x_total_pagado_real = fields.Monetary(
        string="Total pagado (real)",
        currency_field="x_currency_id",
    )

    x_recinto_fiscalizado = fields.Char(string="Recinto fiscalizado")
    x_almacenaje = fields.Boolean(string="Almacenaje")
    x_citas_almacen = fields.Text(string="Citas / almacén")

    x_transportista_entrega = fields.Many2one(
        comodel_name="res.partner",
        string="Transportista (entrega)",
    )

    x_direccion_entrega_final = fields.Text(string="Dirección entrega final")

    # --- Exportación (extras) ---
    x_sales_order = fields.Char(string="SO / Orden de venta")
    x_invoice_export_number = fields.Char(string="Factura exportación (número)")

    x_cliente_extranjero_name = fields.Char(string="Cliente extranjero")
    x_direccion_destino_final = fields.Text(string="Dirección destino final")
    x_condiciones_venta = fields.Text(string="Condiciones de venta")

    x_regulaciones_exportacion_ids = fields.Many2many(
        comodel_name="crm.tag",
        relation="crm_lead_reg_exp_tag_rel",
        column1="lead_id",
        column2="tag_id",
        string="Regulaciones (export)",
    )

    x_certificados_exportacion_ids = fields.Many2many(
        comodel_name="crm.tag",
        relation="crm_lead_cert_exp_tag_rel",
        column1="lead_id",
        column2="tag_id",
        string="Certificados (export)",
    )

    x_licencia_exportacion = fields.Boolean(string="Licencia de exportación")

    x_motivo_exportacion = fields.Selection(
        selection=[
            ("venta", "Venta"),
            ("retorno", "Retorno"),
            ("muestra", "Muestra"),
            ("reparacion", "Reparación"),
            ("otro", "Otro"),
        ],
        string="Motivo de exportación",
    )

    x_punto_salida = fields.Char(string="Punto de salida")

    x_transportista_salida = fields.Many2one(
        comodel_name="res.partner",
        string="Transportista (salida)",
    )

    x_fecha_cruce = fields.Date(string="Fecha de cruce")
    x_fecha_zarpe = fields.Date(string="Fecha de zarpe")
    x_fecha_vuelo = fields.Date(string="Fecha de vuelo")

    x_prueba_entrega = fields.Boolean(string="Prueba de entrega (POD)")
