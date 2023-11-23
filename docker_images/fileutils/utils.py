import os
import argparse
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser(description="Validate Files")
    parser.add_argument(
        "--input_dir",
        type=str,
        help="Name of the folder containing input data",
        default="/pfs/input",
        required=False
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Name of the folder where output baseline will be stored",
        default="/pfs/out",
        required=False
    )
    parser.add_argument(
        "--report_type",
        type=str,
        help="Used by the report pipelien",
        default="partial",
        required=False
    )    
    parser.add_argument(
        "--input_dir_val",
        type=str,
        help="Used by the report pipelien",
        default="/pfs/validate_images",
        required=False
    )
    parser.add_argument(
        "--input_dir_cnv",
        type=str,
        help="Used by the report pipelien",
        default="/pfs/convert_images",
        required=False
    )
    parser.add_argument(
        "--input_dir_res",
        type=str,
        help="Used by the report pipelien",
        default="/pfs/resize_images",
        required=False
    )         
    return parser.parse_args()

def get_file_info(filepath, hasMask=False, isValid=False, isConverted=False, isResized=False):
    im_info = []
    # basic file info
    if not isValid:
            im_info = {
                        "filename": filepath,
                        "extension": "DELETED", 
                        "size": "DELETED", 
                        "has_mask": "DELETED", 
                        "is_valid": "False",
                        "full_path": "DELETED", 
                        "mode": "DELETED", 
                        "width": "DELETED",  
                        "height": "DELETED",
                        "converted": isConverted,
                        "resized": isResized
                    }        
    else:
        _, extension = os.path.splitext(filepath)
        filename = os.path.basename(filepath)
        file_stats = os.stat(filepath)
        file_size = f"{round(file_stats.st_size / 1024)}k"
        try:         
            im = Image.open(filepath)
            im_info = {
                        "filename": filename,
                        "extension": extension, 
                        "size": file_size, 
                        "has_mask": hasMask, 
                        "is_valid": isValid,
                        "full_path": filepath, 
                        "mode": im.mode, 
                        "width": im.width,  
                        "height": im.height,
                        "converted": isConverted,
                        "resized": isResized
                    }
        except Exception as ex:
            # If it's not an image file
            im_info = {
                        "filename": filename,
                        "extension": extension, 
                        "size": file_size, 
                        "has_mask": hasMask, 
                        "is_valid": isValid,
                        "full_path": filepath, 
                        "mode": "N/A", 
                        "width": "N/A",  
                        "height": "N/A",
                        "converted": "N/A",
                        "resized": "N/A"
                    }
    #print("---> RETURNING: ", im_info)
    return im_info

def create_report(input_data, output_file):
    info_list = []
    for item in input_data:
        #print("===-> Item:", item)
        file = item[0]
        isValid = item[1]['valid']
        hasMask = item[2]['has_mask']
        isConverted = item[3]['converted']
        isResized = item[4]['resized']
        file_info = get_file_info(file, hasMask, isValid, isConverted, isResized)
        info_list.append(file_info)
    
    save_report(info_list, output_file)

def save_report(input_data, output_file):
    report_folder = os.path.split(output_file)[0]
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)    

    df_input = pd.DataFrame(input_data)
    df_input.to_csv(output_file)

def merge_reports(file_list, report_title, output_file):
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

    output_html = BeautifulSoup(html, 'html.parser')
    for input_file in file_list:
        if input_file.lower().endswith('.html'):
            with open(os.path.join(input_file), 'r') as html_file:
                report_body = BeautifulSoup(html_file.read(), 'html.parser').body
                snippet_begin = BeautifulSoup(f"<button class='collapsible'>View Report: {report_title}</button>", "html.parser")
                output_html.body.extend(snippet_begin)
                snippet_end = BeautifulSoup(f"<div class='content'>{report_body}</div>", "html.parser")
                output_html.body.extend(snippet_end)
    
    output_html.body.extend(BeautifulSoup(script_block, "html.parser"))

    # Write final HTML file to disk
    print("Saving Merged HTML report to output folder")
    report_folder = os.path.split(output_file)[0]
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    with open(output_file, "w") as file:
        file.write(str(output_html))

    return None

def list_files(directory, is_mask):
    file_list = []
    deleted_list = []
    for path, subdirs, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif')):
                filename=f"{path}/{file}"
                # do not delete html files (reports)
                if not "html" in file:
                  deleted_list.append(filename)
                  os.remove(filename)
            else:
                if is_mask and "_mask" in file:
                        filename = f"{path}/{file}"
                        file_list.append(filename)
                elif not is_mask and "_mask" not in file:
                        filename = f"{path}/{file}"
                        file_list.append(filename)
    return file_list, deleted_list


def list_all_files(directory):
    file_list = []
    deleted_list = []
    for path, subdirs, files in os.walk(directory):
        for file in files:
            filename=f"{path}/{file}"
            if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif')):
                # do not delete html files (reports)
                if not "html" in file:
                  deleted_list.append(filename)
                  os.remove(filename)
            else:
                file_list.append(filename)
    return file_list, deleted_list