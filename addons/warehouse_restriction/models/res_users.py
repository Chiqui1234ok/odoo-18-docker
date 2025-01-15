from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_warehouse_ids = fields.Many2many(
        'stock.warehouse',
        'res_users_stock_warehouse_rel',
        'user_id',
        'warehouse_id',
        string='Almacenes Permitidos',
        help='Define los almacenes a los que el usuario tiene acceso.',
    )

    default_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Almacén Predeterminado',
        help='Almacén que se seleccionará por defecto al crear documentos de inventario.'
    )

    @api.model
    def create(self, vals):
        """ Al crear un usuario, establece el primer almacén permitido como predeterminado si no se especifica. """
        if 'allowed_warehouse_ids' in vals and not vals.get('default_warehouse_id'):
            allowed_warehouses = vals.get('allowed_warehouse_ids')[0][2]  # Lista de IDs
            if allowed_warehouses:
                vals['default_warehouse_id'] = allowed_warehouses[0]
        return super(ResUsers, self).create(vals)

    @api.constrains('allowed_warehouse_ids', 'default_warehouse_id')
    def _check_default_warehouse(self):
        """ Valida que el almacén predeterminado esté dentro de los almacenes permitidos. """
        for user in self:
            if user.default_warehouse_id and user.default_warehouse_id not in user.allowed_warehouse_ids:
                raise ValueError('El almacén predeterminado debe estar dentro de los almacenes permitidos.')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _default_warehouse(self):
        """ Devuelve el almacén predeterminado del usuario actual. """
        return self.env.user.default_warehouse_id

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Almacén',
        default=_default_warehouse,
        required=True
    )
