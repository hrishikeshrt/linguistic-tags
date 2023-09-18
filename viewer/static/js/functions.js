// Constants
const GITHUB_USERNAME = 'hrishikeshrt';
const GITHUB_REPOSITORY_NAME = 'linguistic-tags';
const GITHUB_REPOSITORY = 'hrishikeshrt/linguistic-tags';
const GITHUB_BRANCH = 'master';
const GITHUB_DATA_DIRECTORY_URL = `https://raw.githubusercontent.com/${GITHUB_REPOSITORY}/${GITHUB_BRANCH}/data/`;

/* ------------------------------------------------------------------------- */
// Parsers

// Parse CSV data from local files
function parseCSVFile(filePath, complete_callback, step_callback) {
    Papa.parse(filePath, {
        header: true,
        skipEmptyLines: true,
        worker: false, // worker: true to stream a big file in worker thread
        complete: function (results) {
            complete_callback(results.data);
        },
        // step: function (results) {
        //     step_callback("Row:", results.data);
        // },
    });
}

// Parse CSV data from remote files
function parse_remote_csv_file(fileUrl, complete_callback, step_callback) {
    Papa.parse(fileUrl, {
        download: true,
        header: true,
        skipEmptyLines: true,
        worker: false, // worker: true to stream a big file in worker thread
        complete: function (results) {
            complete_callback(results.data);
        },
        // step: function (results) {
        //     step_callback("Row:", results.data);
        // },
    });
}

/* ------------------------------------------------------------------------- */

/* ------------------------------------------------------------------------- */
// Formatters

// Function to generate and populate the table
function populate_tag_dropdown() {
    const tagSelector = document.getElementById('tag-selector');
    const tagIds = ['001', '002', '003', '004']; // Update with actual tag filenames

    // Add options to the dropdown for each tag file
    for (const tagFile of tagIds) {
        const option = document.createElement('option');
        option.value = tagFile;
        option.textContent = tagFile;
        tagSelector.appendChild(option);
    }

    // Event listener to load selected tag's data when dropdown value changes
    tagSelector.addEventListener('change', function () {
        const selectedTag = tagSelector.value;
        load_tag_data(selectedTag);
    });
}

function populate_table(data) {
    const tableHeaders = Object.keys(data[0]);
    let tableHTML = '<thead><tr>';

    // Create table headers
    for (const header of tableHeaders) {
        tableHTML += `<th data-field="${header}">${header}</th>`;
    }
    tableHTML += '</tr></thead><tbody>';

    // Create table rows
    for (const row of data) {
        tableHTML += '<tr>';
        for (const header of tableHeaders) {
            tableHTML += `<td>${row[header]}</td>`;
        }
        tableHTML += '</tr>';
    }

    tableHTML += '</tbody>';
    document.getElementById('linguistic-tag-table').innerHTML = tableHTML;
}

function populate_meta(data) {
    var metaHTML = '';
    for (const row of data) {
        var first = true;
        for (const entry of Object.values(row)) {
            if (first) {
                metaHTML += '<b>' + entry + '</b>';
                first = false;
            } else {
                metaHTML += entry;
            }
        }
        metaHTML += '<br>';
    }
    document.getElementById('linguistic-tag-meta').innerHTML = metaHTML;
}

/* ------------------------------------------------------------------------- */
// View Functions

function load_tag_data(tag_id) {
    const meta_csv_url = `${GITHUB_DATA_DIRECTORY_URL}/meta_${tag_id}.csv`;
    const table_csv_url = `${GITHUB_DATA_DIRECTORY_URL}/table_${tag_id}.csv`;

    parse_remote_csv_file(table_csv_url, function (data) {
        populate_table(data);
    });
    parse_remote_csv_file(meta_csv_url, function (data) {
        populate_meta(data);
    });
}

function load_tag_list() {
    const metaUrl = `${GITHUB_DATA_DIRECTORY_URL}/meta.csv`
    parse_remote_csv_file(metaUrl, function(data) {
        populate_table(data);
    })
}

function compare_tag_data(tag_id_1, tag_id_2) {
    const table_csv_url_1 = `${GITHUB_DATA_DIRECTORY_URL}/table_${tag_id_1}.csv`;
    const table_csv_url_2 = `${GITHUB_DATA_DIRECTORY_URL}/table_${tag_id_2}.csv`;
}