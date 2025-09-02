frappe.ui.form.on('Purchase Invoice', {
    refresh: function(frm) {
        frm.add_custom_button(__('Print Barcode Labels'), function() {
            window.open(
                `/api/method/barcode_custom_app.api.labels.generate_barcode_labels?docname=${frm.doc.name}`,
                '_blank'   // Open in new tab
            );
        }, __('Print'));
    }
});
