# Copyright Nova Code (http://www.novacode.nl)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models

from ..models.celery_task import STATES_TO_JAMMED


class CeleryHandleJammedJask(models.TransientModel):
    _name = 'celery.handle.jammed.task'
    _description = 'Handle Jammed Task'

    @api.model
    def _default_task_ids(self):
        res = False
        context = self.env.context
        if (context.get('active_model') == 'celery.jammed.task.report' and
                context.get('active_ids')):
            task_ids = context['active_ids']
            res = self.env['celery.task'].search([
                ('id', 'in', context['active_ids']),
                ('state', 'in', STATES_TO_JAMMED)]).ids
        return res

    task_ids = fields.Many2many(
        'celery.task', string='Tasks', default=_default_task_ids,
        domain=[('state', 'in', STATES_TO_JAMMED)])

    @api.multi
    def action_handle_jammed_tasks(self):
        self.task_ids.action_jammed()
        return {'type': 'ir.actions.act_window_close'}
