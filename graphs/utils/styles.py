def table_css():
    return [{ # override default css for selected/focused table cells
                'selector': 'td.cell--selected, td.focused',
                'rule': 'background-color: #FF4136;'
            }, {
                'selector': 'td.cell--selected *, td.focused *',
                'rule': 'color: #3C3C3C !important;'
            }]