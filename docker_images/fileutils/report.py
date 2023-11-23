import uuid
import os, glob
import pandas as pd
from utils import parse_args
from bs4 import BeautifulSoup

def create_partial_report(args):
    html = """
            <html>
                <head>
                    <style>
                    .dataframe{ font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; width: 100%; border: 1px solid #ddd; padding: 8px; }
                    .dataframe th{ padding-top: 12px; padding-bottom: 12px; text-align: center; background-color: #04AA6D; color: white; }
                    .dataframe tr:nth-child(even){background-color: #f2f2f2;}
                    .dataframe td:nth-child(3), .dataframe td:nth-child(4), .dataframe td:nth-child(5), .dataframe td:nth-child(6),
                    .dataframe td:nth-child(8), .dataframe td:nth-child(9), .dataframe td:nth-child(10) {text-align:center;}
                    .dataframe tr:hover {background-color: #ddd;}

                    .collapsible { background-color: #777; color: white; cursor: pointer; padding: 18px; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; }
                    .active, .collapsible:hover { background-color: #555; }
                    .content { padding: 0 18px; max-height: 0; overflow: hidden; transition: max-height 0.2s ease-out; background-color: #f1f1f1; }
                    </style>

                </head>
                <body>
                    <h1> Report for Data Processing - Brain MRI
                </body>
            </html>
        """
    script_block = """
            <script>
                var coll = document.getElementsByClassName('collapsible');
                var i;

                for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener('click', function() {
                    this.classList.toggle('active');
                    console.log('clicked!!');
                    var content = this.nextElementSibling;
                    if (content.style.maxHeight){
                    content.style.maxHeight = null;
                    } else {
                    content.style.maxHeight = content.scrollHeight + 'px';
                    } 
                });
                }
            </script>
    """
 
    output_file =  uuid.uuid4().hex
    output_html = BeautifulSoup(html, 'html.parser')
    report_list = []
    report_columns = ["Filename", "Extension", "Size", "Has Mask", "Is Valid", "Full Path", "Mode", "Width", "Height", "Converted", "Resized"]

    for path, subdirs, files in os.walk(args.input_dir):
        for file in files:
            if file.lower().endswith(('.csv')):
                filename=f"{path}/{file}"
                split_path = path.split(os.sep)
                output_file = split_path[len(split_path)-2]
                print(f"--> Loading file: {filename}")                
                df = pd.read_csv(filename, index_col=None, header=0, names=report_columns)
                report_list.append(df)
    
    report_df = pd.concat(report_list, axis=0, ignore_index=True)
    report_table = report_df.to_html(header=True)
    snippet_begin = BeautifulSoup(f"<button class='collapsible'>View Report {output_file}</button>", "html.parser")
    output_html.body.extend(snippet_begin)
    snippet_end = BeautifulSoup(f"<div class='content'>{report_table}</div>", "html.parser")
    output_html.body.extend(snippet_end)

    output_html.body.extend(BeautifulSoup(script_block, "html.parser"))

    # Write final HTML file to disk
    print("Saving HTML report to output folder")
    with open(f"{args.output_dir}/{output_file}.html", "w") as file:
        file.write(str(output_html))

def create_full_report(args):
    html = """
            <html>
                <head>
                    <style>
                    .dataframe{ font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; width: 100%; border: 1px solid #ddd; padding: 8px; }
                    .dataframe th{ padding-top: 12px; padding-bottom: 12px; text-align: center; background-color: #04AA6D; color: white; }
                    .dataframe tr:nth-child(even){background-color: #f2f2f2;}
                    .dataframe td:nth-child(3), .dataframe td:nth-child(4), .dataframe td:nth-child(5), .dataframe td:nth-child(6),
                    .dataframe td:nth-child(8), .dataframe td:nth-child(9), .dataframe td:nth-child(10) {text-align:center;}
                    .dataframe tr:hover {background-color: #ddd;}

                    .collapsible { background-color: #777; color: white; cursor: pointer; padding: 18px; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; }
                    .active, .collapsible:hover { background-color: #555; }
                    .content { padding: 0 18px; max-height: 0; overflow: hidden; transition: max-height 0.2s ease-out; background-color: #f1f1f1; }
                    </style>

                </head>
                <body>
                    <h1> Final Report for Data Processing - Brain MRI
                </body>
            </html>
        """
    script_block = """
            <script>
                var coll = document.getElementsByClassName('collapsible');
                var i;

                for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener('click', function() {
                    this.classList.toggle('active');
                    console.log('clicked!!');
                    var content = this.nextElementSibling;
                    if (content.style.maxHeight){
                    content.style.maxHeight = null;
                    } else {
                    content.style.maxHeight = content.scrollHeight + 'px';
                    } 
                });
                }
            </script>
    """

    report_name = ""
    output_html = BeautifulSoup(html, 'html.parser')
    for path, subdirs, files in os.walk(args.input_dir):
        for file in files:
            if file.lower().endswith(('.html')):
                filename=f"{path}/{file}"
                print(f"--> Loading file: {filename}")                
                report_name, file_extension = os.path.splitext(file)
                html_file = open(filename)
                html_s = BeautifulSoup(html_file, 'html.parser')
                report_table = html_s.body.table
                
                snippet_begin = BeautifulSoup(f"<h2>Report {report_name}</h2><button class='collapsible'>View Report</button>", "html.parser")
                output_html.body.extend(snippet_begin)
                snippet_end = BeautifulSoup(f"<div class='content'>{report_table}</div>", "html.parser")
                output_html.body.extend(snippet_end)

    output_html.body.extend(BeautifulSoup(script_block, "html.parser"))

    # Write final HTML file to disk
    print("Saving HTML report to output folder")
    with open(f"{args.output_dir}/full_report.html", "w") as file:
        file.write(str(output_html))

if __name__ == "__main__":
    args = parse_args()
    if args.report_type == "partial":
        create_partial_report(args)
    else:
        create_full_report(args)