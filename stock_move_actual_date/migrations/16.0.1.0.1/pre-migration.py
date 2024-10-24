# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Check if the old column 'accounting_date' exists before attempting to transfer data
    if openupgrade.column_exists(env.cr, "stock_picking", "accounting_date"):
        env.cr.execute(
            """
            UPDATE stock_picking
            SET actual_date = accounting_date
            WHERE accounting_date IS NOT NULL;
            """
        )
        env.cr.execute(
            """
            UPDATE stock_move
            SET actual_date = accounting_date
            """
        )
        env.cr.execute(
            """
            UPDATE stock_move_line sml
            SET actual_date = sm.actual_date
            FROM stock_move sm
            WHERE sml.move_id = sm.id
            """
        )
