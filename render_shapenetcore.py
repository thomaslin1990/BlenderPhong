import sys
sys.path.append("/home/dongyun/Data/shrec17/code/BlenderPhong/")
import csv
import os
import argparse
from phong import *
# import ipdb

def args_set():
    args = argparse.ArgumentParser(description="the settings")
    args.add_argument("--output_dir", type=str, help="the output directory to save rendered view images")
    args.add_argument("--object_dir", type=str, help="the directory for the 3D mesh files (in .obj format)")
    args.add_argument("--csv_config_file", type=str, help="the csv file containing the class/subclass info for each object")
    args.add_argument("--render_type", type=str, help="the type of objects [normal, purturbed]", default="normal")
    return args

def do_model(path, image_dir, synsetID, id):
    name = load_model(path)
    center_model(name)
    normalize_model(name)
    # image_subdir = os.path.join(image_dir, name)
    for i, c in enumerate(cameras):
        # move_camera(c)
        move_camera_20(c)
        render()
        save(image_dir, str(synsetID) + "_" + str(id) + "_" + "{:03d}".format(i))

    delete_model(name)

if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index('--') + 1:]

    if len(argv) != 4:
        print('phong.py args: <output_dir> <object_dir> <csv_config_file> <render_type>')
        exit(-1)

    output_dir = argv[0]
    object_dir = argv[1]
    csv_config_file = argv[2]
    render_type = argv[3]

    ## Example to use subprocess to run blender
    # subprocess.run(["blender", "phong.blend", "--background", "--python", "your_script.py"])
    output_dir = os.path.join(output_dir, "shapenetcore55_20views_" + render_type)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    init_camera()
    fix_camera_to_origin()
    with open(csv_config_file, mode='r') as file:
        csv_reader = csv.reader(file)

        for i, row in enumerate(csv_reader):
            if i > 0:
                id, synsetId, subSynsetId, _, split = row

                output_model_dir = os.path.join(output_dir, synsetId)
                if not os.path.exists(output_model_dir):
                    os.makedirs(output_model_dir, exist_ok=True)

                output_split_dir = os.path.join(output_model_dir, split)
                if not os.path.exists(output_split_dir):
                    os.makedirs(output_split_dir, exist_ok=True)
                # check if the object hsa been rendered, if so, skip it
                rendered_file_list = os.listdir(output_split_dir)
                rendered_id_list = [item.split("_")[1] for item in rendered_file_list]
                if id in rendered_id_list:
                    count = rendered_id_list.count(id)
                    if count == 20:
                        print("Render view images for {} is finished!".format(id))
                        continue

                ori_model_folder = split + "_" + render_type
                ori_model_path = os.path.join(object_dir, ori_model_folder, (id+".obj"))

                do_model(ori_model_path, output_split_dir, synsetId, id)
            
            print("Render view images for {} is finished!".format(id))
    file.close()
    print("Rendering is done!")

                

    