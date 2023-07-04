import json
import re


def convert_plotly(html: str, **kwargs) -> str:
    # Remove plotly js (remove this to not pollute the search index and use <script src="https://cdn.plot.ly/plotly-2.14.0.min.js"></script> instead)
    html = re.sub(
        '<div class="jp-RenderedHTMLCommon jp-RenderedHTML jp-OutputArea-output " data-mime-type="text\/html">\s*?<script type="text\/javascript">.*?<\/script>\s*?<\/div>',
        "",
        html,
        flags=re.S,
    )

    # Fix plots in jupyter notebook
    html = re.sub(
        '(?<=<script type="text\/javascript">)\s*?require\(\["plotly"\], function\(Plotly\) {\s*?(?=window\.PLOTLYENV)',
        "",
        html,
    )
    html = re.sub("\).then\(function\(\){.*?(?=<\/script>)", ")}", html, flags=re.S)

    return html


def clean_search(config):
    with open(f"{config.data['site_dir']}/search/search_index.json", "r") as f:
        search = json.load(f)

    for elem in search["docs"]:
        # Remove plotly graphs
        elem["text"] = re.sub(
            "window\.PLOTLYENV.*?\)\s*?}\s*?", "", elem["text"], flags=re.S
        )

        # Remove mkdocs-jupyter css
        elem["text"] = re.sub(
            "\(function \(global, factory.*?(?=Example:)", "", elem["text"], flags=re.S
        )

    with open(f"{config.data['site_dir']}/search/search_index.json", "w") as f:
        json.dump(search, f)
