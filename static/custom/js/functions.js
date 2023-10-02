/* ------------------------------------------------------------------------- */

String.prototype.toTitleCase = function(){
    return this.replace("_", " ").replace(/(?:^|\s)\w/g, function(match) {
        return match.toUpperCase();
    });
};

/* ------------------------------------------------------------------------- */
// Render Table

function render_table($parent, data, options, download_name = 'result') {
    // data.headers contains list of header fields
    // each field being a JSON object
    // {title: "display_name", field: "field_name", switchable: bool, sortable: bool, searchable: bool, visible: bool, ...}
    // https://bootstrap-table.com/docs/api/column-options/

    // data.rows contains list of rows
    // each row being a JSON object {field_name: field_value}

    $parent.empty();
    console.log(data)

    const $table  = $("<table />", {class: "table table-hover"});
    $parent.append($table);

    $table.bootstrapTable({
        columns: data.columns,
        search: false,
        searchHighlight: true,
        showColumns: true,
        stickyHeader: true,
        stickyHeaderOffsetLeft: 0,
        stickyHeaderOffsetRight: 0,
        resizable: true,
        pagination: false,
        showToggle: false,
        detailView: false,
        showExport: true,
        exportTypes: ['csv', 'json', 'txt', 'excel'],
        exportOptions: {
            fileName: function () {
                return download_name
            }
        },
        data: data.rows
    });
    $table.bootstrapTable('refreshOptions', options);
}

/* ------------------------------------------------------------------------- */