import os
from utils import list_files, parse_args, create_report
from distutils.dir_util import copy_tree

def main():
    args = parse_args()
    all_files, deleted_files = list_files(args.input_dir, False)
    all_masks, _ = list_files(args.input_dir, True)
    print(f"--> Total Files: {len(all_files)}")
    print(f"--> Total Masks: {len(all_masks)}")    
    print(f"--> Deleted Files: {len(deleted_files)}")
    matches = 0
    no_match = 0
    no_match_list = []
    report_list = []
    for file in all_files:
        filename, _ = os.path.splitext(file)
        match = 0
        hasMask = False
        for mask in all_masks:
              if filename in mask:
                match = 1
                matches = matches + 1
                hasMask = True
                break
        if match == 0:
            no_match = no_match + 1
            no_match_list.append(file)
        report_list.append([file, {'valid' : True},  {'has_mask': hasMask},  {'converted': False}, {'resized': False}])
    for deleted_file in deleted_files:
        report_list.append([deleted_file, {'valid' : False},  {'has_mask': False},  {'converted': False}, {'resized': False}])
    if len(no_match_list) > 0:
         for filename in no_match_list:
              print(f"--> File has no mask: {filename}")
              # do not delete html files (reports)
              if not "html" in filename:
                  report_list.append([filename, {'valid' : True},  {'has_mask': False},  {'converted': False}, {'resized': False}])
                  os.remove(filename)

    # Generate Report
    print("--> Generating CSV Report")
    create_report(report_list, f"{args.output_dir}/_report/report.csv")

    # Copy files to output folder
    print("--> Copying files to output folder")
    copy_tree(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()

