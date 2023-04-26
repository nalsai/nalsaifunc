import vapoursynth as vs
from vapoursynth import core


def EdgeChromaFix(
    source: vs.VideoNode, right=14, size=4, kernel=core.resize.Spline36
) -> vs.VideoNode:
    # TODO:
    # - make sure the input is YUV
    # - handle chroma subsampling

    v = core.std.ShufflePlanes(source, 2, vs.GRAY)

    new_chroma_width = right + size
    old_chroma_width = v.width - new_chroma_width

    v1 = v.std.Crop(right=new_chroma_width)
    v2 = v.std.Crop(left=old_chroma_width, right=right).resize.Spline36(width=new_chroma_width)
    v_new = core.std.StackHorizontal([v1, v2])
    return core.std.ShufflePlanes([source, source, v_new], [0, 1, 0], vs.YUV)
