import os
import uuid
from PIL import Image
from utils import list_all_files, parse_args, create_report
from distutils.dir_util import copy_tree

def main():
    args = parse_args()
    report_list = []
    all_files, deleted_files = list_all_files(args.input_dir)
    # print(f"--> Total Files: {len(all_files)}: {all_files}")
    # print(f"--> Deleted Files: {len(deleted_files)}: {deleted_files}")
    print(f"--> Total Files: {len(all_files)}")
    print(f"--> Deleted Files: {len(deleted_files)}: {deleted_files}")    
    if len(all_files) > 0:    
        for file in all_files:
            im = Image.open(file)
            width, height = im.size
            if width != 256 or height != 256:
                report_list.append([file, {'valid' : True},  {'has_mask': True},  {'converted': False}, {'resized': True}])
                im = im.resize((256, 256))
                im.save(file, "TIFF")
                print(f"--> Resized file to 256x256: {file}")
            else:
                report_list.append([file, {'valid' : True},  {'has_mask': True},  {'converted': False}, {'resized': False}])

        for deleted_file in deleted_files:
            report_list.append([deleted_file, {'valid' : False},  {'has_mask': False},  {'converted': False}, {'resized': False}])

        # Generate Report
        print("--> Generating CSV Report")
        create_report(report_list, f"{args.output_dir}/_report/{uuid.uuid4().hex}.csv")

        # Copy files to output folder
        print("--> Copying files to output folder")
        copy_tree(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()

