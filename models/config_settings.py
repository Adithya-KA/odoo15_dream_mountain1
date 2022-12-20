from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mv_ip_address = fields.Char(string='Mv Ip Address')
    mv_port = fields.Char(string='Mv Port')
    mv_user = fields.Char(string='Mv User')
    mv_password = fields.Char(string='Mv Password')
    mv_enabled = fields.Boolean("DB Authentication")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('dream_mountain.mv_ip_address', self.mv_ip_address)
        self.env['ir.config_parameter'].set_param('dream_mountain.mv_port', self.mv_port)
        self.env['ir.config_parameter'].set_param('dream_mountain.mv_user', self.mv_user)
        self.env['ir.config_parameter'].set_param('dream_mountain.mv_password', self.mv_password)
        self.env['ir.config_parameter'].set_param('dream_mountain.mv_enabled', self.mv_enabled)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            mv_ip_address=params.get_param('dream_mountain.mv_ip_address'),
            mv_port=params.get_param('dream_mountain.mv_port'),
            mv_user=params.get_param('dream_mountain.mv_user'),
            mv_password=params.get_param('dream_mountain.mv_password'),
            mv_enabled=params.get_param('dream_mountain.mv_enabled'),
        )
        return res
