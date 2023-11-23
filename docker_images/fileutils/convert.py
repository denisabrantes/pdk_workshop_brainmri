import os
import uuid
from PIL import Image
from utils import list_all_files, parse_args, create_report
from distutils.dir_util import copy_tree

def convert_image(input_img):
    filename, file_extension = os.path.splitext(input_img)
    output_img = filename + '.tif'    
    im = Image.open(input_img)
    im.save(output_img, 'TIFF')
    return output_img

def main():
    args = parse_args()
    report_list = []
    convert_list = []
    all_files, deleted_files = list_all_files(args.input_dir)
    # print(f"--> Total Files: {len(all_files)}: {all_files}")
    # print(f"--> Deleted Files: {len(deleted_files)}: {deleted_files}")
    print(f"--> Total Files: {len(all_files)}")
    print(f"--> Deleted Files: {len(deleted_files)}: {deleted_files}")    
    if len(all_files) > 0:
        for file in all_files:
            filename, file_extension = os.path.splitext(file)
            if file_extension not in ['.tif','.tiff']:
                tif_name = convert_image(file)
                convert_list.append(file)
                print(f"--> Converted File {file} to .tif")
                report_list.append([file, {'valid' : True},  {'has_mask': True},  {'converted': True}, {'resized': False}])
                
            else:
                report_list.append([file, {'valid' : True},  {'has_mask': True},  {'converted': False}, {'resized': False}])

        for deleted_file in deleted_files:
            report_list.append([deleted_file, {'valid' : False},  {'has_mask': False},  {'converted': False}, {'resized': False}])

        # Generate Report
        print("--> Generating CSV Report")
        create_report(report_list, f"{args.output_dir}/_report/{uuid.uuid4().hex}.csv")

        for file in convert_list:
            os.remove(file)

        # Copy files to output folder
        print("--> Copying files to output folder")
        copy_tree(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()