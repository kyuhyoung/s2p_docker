'''
import open3d as o3d
import glob
import os
from pathlib import Path

# 병합할 폴더 경로 지정
ply_folder = "/home/dabeeo/workspace/StraightMeshGeneration/src/s2p/tests/output/250527_nk_v1/pc"  # 여기에 분할된 PLY 파일들이 있다고 가정
output_file = "/home/dabeeo/workspace/StraightMeshGeneration/src/s2p/tests/output/250527_nk_v1/merged_pointcloud.ply"

# 모든 PLY 파일 찾기
#ply_files = sorted(glob.glob(os.path.join(ply_folder, "*.ply")))
ply_files = sorted(list(Path(ply_folder).rglob("*.ply")))

# 포인트 클라우드 리스트
merged_pcd = o3d.geometry.PointCloud()

print(f"총 {len(ply_files)}개의 파일을 병합합니다...")

# 각 파일을 읽어서 병합
for ply_file in ply_files:
    print(f"불러오는 중: {ply_file}")
        pcd = o3d.io.read_point_cloud(ply_file)
            merged_pcd += pcd  # 병합

            # 병합된 결과 저장
            o3d.io.write_point_cloud(output_file, merged_pcd)
            print(f"병합 완료! 저장된 파일: {output_file}")
'''


#!/usr/bin/env python3
import argparse
import glob
import os
from pathlib import Path
import numpy as np
from plyfile import PlyData, PlyElement


def merge_ply_files(ply_folder: str, output_file: str) -> None:
    """
    Merge all .ply files in `ply_folder` into a single PLY saved at `output_file`.
    """
    # 1) Find all PLYs
    #ply_files = sorted(glob.glob(os.path.join(ply_folder, "*.ply")))
    #ply_files = sorted(list(Path(ply_folder).rglob("*.ply")))
    ply_files = sorted(list(Path(ply_folder).rglob("cloud.ply")))
    if not ply_files:
        raise RuntimeError(f"No PLY files found in {ply_folder!r}")

    # 2) Read the first file to get the vertex dtype
    first_ply = PlyData.read(ply_files[0])
    vertex_dtype = first_ply['vertex'].data.dtype

    # 3) Load each PLY’s vertex array
    arrays = []
    for fn in ply_files:
        print(f"Reading {fn} …")
        ply = PlyData.read(fn)
        arr = ply['vertex'].data
        if arr.dtype != vertex_dtype:
            raise RuntimeError(f"Field mismatch: {fn} has dtype {arr.dtype}, expected {vertex_dtype}")
        arrays.append(arr)

    # 4) Concatenate into one big structured array
    merged_vertices = np.concatenate(arrays)

    # 5) Write out the merged PLY
    el = PlyElement.describe(merged_vertices, 'vertex')
    PlyData([el], text=True).write(output_file)
    print(f"Merged {len(arrays)} files → {output_file}")


def main():
    t_start = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        description="Merge a folder of PLY point-clouds into a single PLY file."
    )
    parser.add_argument(
        "--ply_folder",
        help="Path to folder containing .ply files to merge"
    )
    parser.add_argument(
        "--output_file",
        help="Path to where the merged PLY should be written"
    )
    args = parser.parse_args()
    merge_ply_files(args.ply_folder, args.output_file)

    t_end = datetime.datetime.now()
    print("Elapsed time for merging ply files :", t_end - t_start)

if __name__ == "__main__":
    main()


'''
from plyfile import PlyData, PlyElement
import numpy as np
import glob, os

ply_folder  = "/home/dabeeo/.../pc"
output_file = "/home/dabeeo/.../merged_pointcloud.ply"

# 1) Find all PLYs
ply_files = sorted(glob.glob(os.path.join(ply_folder, "*.ply")))
if not ply_files:
    raise RuntimeError("No PLY files found in " + ply_folder)

# 2) Read the first file to get the vertex dtype
first = PlyData.read(ply_files[0])
vertex_dtype = first['vertex'].data.dtype

# 3) Pre-allocate a list of arrays
arrays = []
for fn in ply_files:
    print(f"Reading {fn} …")
    ply = PlyData.read(fn)
    arr = ply['vertex'].data  # this is a numpy structured array
    if arr.dtype != vertex_dtype:
        raise RuntimeError(f"Field mismatch: {fn} has {arr.dtype}, expected {vertex_dtype}")
    arrays.append(arr)

# 4) Concatenate into one big array
merged_vertices = np.concatenate(arrays)

# 5) Wrap in a PlyElement and write
el = PlyElement.describe(merged_vertices, 'vertex')
PlyData([el], text=True).write(output_file)
print("Wrote merged PLY to", output_file)
'''
