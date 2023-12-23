/* --------------------------------------------------------------------- */
// Elements

const $add_comment_modal = $("#add-comment-modal");
const $add_comment_form = $("#add-comment-form");
const $add_comment_submit_button = $("#add-comment-submit");

const $add_comment_tablename = $("#add-comment-tablename");
const $add_comment_action = $("#add-comment-action");
const $add_comment_detail = $("#add-comment-detail");
const $add_comment_comment_text = $("#add-comment-comment-text");

/* --------------------------------------------------------------------- */
// Menu Items (as compatible with Context-js)

const cell_actions_header_menu_item = {
    header: "Cell Actions",
}

const add_comment_menu_item = {
    text: "<i class='fa fa-comment mr-1'></i> Add Comment",
    action: function (e, context) {
        e.preventDefault();
        const $element = $(context);
        // const tablename = $element.data("tablename");
        // const detail = $element.data("detail");

        const $table = $element.closest("table");
        const data = $table.bootstrapTable("getData");
        const options = $table.bootstrapTable("getOptions");
        const visible_columns = $table.bootstrapTable("getVisibleColumns");
        const row_index = $element.parent().data("index");
        const cell_index = $element[0].cellIndex;
        const detail_view_index_offset = (
            options.detailView &&
            options.detailViewIcon &&
            !options.cardView
            && options.detailViewAlign !== "right"
        ) ? 1 : 0;
        const row = data[row_index];
        const field = visible_columns[cell_index - detail_view_index_offset].field;
        const tablename = $table.data("tablename");
        const extra = $table.data("extra");

        const detail = {
            tablename: tablename,
            row_index: row_index,
            cell_index: cell_index,
            field: field,
            value: row[field],
            extra: extra,
        };
        console.log(detail);

        $add_comment_modal.modal('show');
        $add_comment_tablename.val(tablename);
        $add_comment_detail.val(JSON.stringify(detail));

        setTimeout(function () {
            $add_comment_comment_text.focus(); // focus on comment text
        }, 500);
    }
};

/* --------------------------------------------------------------------- */
// Submit Action

$add_comment_submit_button.on('click', function (e) {
    if ($add_comment_form[0].checkValidity()) {
        $add_comment_modal.modal('hide');

        const comment_data = {
            tablename: $add_comment_tablename.val(),
            action: $add_comment_action.val(),
            comment: $add_comment_comment_text.val(),
            detail: $add_comment_detail.val(),
        };
        console.log(comment_data);

        $.post(API_URL_POST_COMMENT,
            comment_data,
            function (response) {
                $.notify({
                    message: response.message
                }, {
                    type: response.style
                });
                if (response.success) {
                    $add_comment_tablename.val("");
                    $add_comment_action.val("");
                    $add_comment_comment_text.val("");
                    $add_comment_detail.val("");
                }
            }, 'json');
    } else {
        $add_comment_form[0].reportValidity();
    }
});

/* --------------------------------------------------------------------- */
