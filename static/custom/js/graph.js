function parse_dot(graph_input) {
    return graph_input;
}

function parse_dependency_relations(graph_input) {
    const relations = graph_input.trim().split(/[\t ]*\n+[\t ]*/);
    const dot_text = [
        "digraph G {"
    ];
    for (const relation of relations) {
        const relation_words = relation.split(/\s+/);
        const src_id = relation_words[0];
        const src_text = relation_words[1];
        dot_text.push(`n${src_id} [label="${src_text}"];`);
    }
    for (const relation of relations) {
        const relation_words = relation.split(/\s+/);
        const src_id = relation_words[0];

        if (relation_words.length < 3) {
            continue;
        }
        const relation_label = relation_words[2];
        const trg_id = relation_words[3];
        dot_text.push(`n${trg_id} -> n${src_id} [label="${relation_label}", dir="back"];`);
    }
    dot_text.push("}");
    return dot_text.join("\n");
}

function render_graph_in_container(graph_input, $graph_container) {
    $graph_container.empty();
    Viz.instance().then(function(viz) {
        const svg = viz.renderSVGElement(graph_input);
        $graph_container[0].appendChild(svg);
    });
}
