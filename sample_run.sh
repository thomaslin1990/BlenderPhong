# mkdir -p tmp
# blender phong.blend --background --python phong.py -- /home/dongyun/Data/shrec17/data/public/train_normal/000080.obj ./tmp
# /home/dongyun/Data/blender-2.93.5-linux-x64/blender 
# blender phong.blend 
xvfb-run blender phong.blend --background --python render_shapenetcore.py -- \
/home/dongyun/Data/shrec17/data \
/home/dongyun/Data/shrec17/data/public \
/home/dongyun/Data/shrec17/code/all.csv \
normal

xvfb-run blender phong.blend --background --python render_shapenetcore.py -- \
/home/dongyun/Data/shrec17/data \
/home/dongyun/Data/shrec17/data/public \
/home/dongyun/Data/shrec17/code/all.csv \
perturbed