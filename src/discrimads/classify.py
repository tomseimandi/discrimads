import os
from inaFaceAnalyzer.inaFaceAnalyzer import ImageAnalyzer
from pathlib import Path


def predict_gender(frames_dir: Path) -> int:
    inaFaceAnalyzer = ImageAnalyzer()
    paths = os.listdir(frames_dir)
    frame_list = filter(lambda x: x.endswith(".jpg"), paths)
    frame_list = list(map(lambda x: frames_dir / x, frame_list))

    # classify frames
    df = inaFaceAnalyzer([str(p) for p in frame_list])
    df_2 = df.groupby("frame")['sex_label'].apply(list)
    ret = []
    for row in df_2:
        if len(row) > 1:
            if len(set(row)) > 1:
                ret.append(3)
            else:
                if row[0] == 'f':
                    ret.append(1)
                else:
                    ret.append(0)
        else:
            if row[0] == 'f':
                ret.append(1)
            else:
                ret.append(0)
    for frame_name in frame_list:
        if frame_name not in df['frame'].tolist():
            ret.append(2)

    del inaFaceAnalyzer
    return ret
