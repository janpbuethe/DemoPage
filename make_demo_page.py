import argparse
import os

import yaml

parser = argparse.ArgumentParser()
parser.add_argument("folder")
parser.add_argument("config")

def write_header(f, title, intro=None):
    f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        article {{
            align-items: flex-start;
            display: flex;
            flex-wrap: wrap;
            gap: 4em;
        }}
        html {{
            box-sizing: border-box;
            font-family: "Source Sans", "Verdana", "Calibri", sans-serif;
            padding: 2em;
        }}
        td {{
            padding: 3px 7px;
            text-align: center;
        }}
        td:first-child {{
            text-align: end;
        }}
        th {{
            background: #ff9900;
            color: #000;
            font-size: 1.2em;
            padding: 7px 7px;
        }}
        .section {{
            overflow-x: scroll;
        }}
        body {{
            margin: 0px auto;
            max-width: 60rem;
        }}
    </style>
</head>
<body>
<h1>{title}</h1>
<article>
            """)
    if intro is not None:
        f.write(f"""
<div>
    <p>
        {intro}
    </p>          
</div>
"""
                )

def write_footer(f):
    f.write("""
</article>
</body>
</html>
""")




def write_table_row(f, num_tabs, entries, header=False):
    sep="th" if header else "td"
    prefix=num_tabs * "\t"
    f.write(prefix + "<tr>\n")
    for e in entries:
        f.write(prefix + f"\t<{sep}>{e}</{sep}>\n")
    f.write(prefix + "</tr>\n")

def write_section(f, section):
    base = section['base']
    conditions = list(section['conditions'].keys())

    f.write("<div class=\"section\">\n")
    f.write(f"\t<h2>{section['title']}</h2>\n")
    f.write("\t<table>\n")

    write_table_row(f, 2, ["Item"] + list(section['conditions'].values()), header=True)
    for item, name in section['items'].items():
        write_table_row(
            f, 2, [name] + [f'<audio controls> <source src="{os.path.join(base, cond, item)}"> </audio>' for cond in conditions] 
        )

    f.write("\t</table>\n")
    f.write("</div>\n")


if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.config) as f:
        config = yaml.load(f, yaml.FullLoader)
    
    with open(os.path.join(args.folder, 'index.html'), "w") as f:
        write_header(f, config['title'], intro=config['description'])
        for section in config['sections']:
            write_section(f, section)
        write_footer(f)