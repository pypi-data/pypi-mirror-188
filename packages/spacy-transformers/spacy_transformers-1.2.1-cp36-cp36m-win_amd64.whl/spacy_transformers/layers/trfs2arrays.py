from typing import List, cast
from transformers.file_utils import ModelOutput
from transformers.modeling_outputs import BaseModelOutput
from thinc.api import Model
from thinc.types import Ragged, Floats2d
from ..data_classes import TransformerData
from ..align import apply_alignment


def trfs2arrays(
    pooling: Model[Ragged, Floats2d], grad_factor: float
) -> Model[List[TransformerData], List[Floats2d]]:
    """Pool transformer data into token-aligned tensors."""
    return Model(
        "trfs2arrays", forward, layers=[pooling], attrs={"grad_factor": grad_factor}
    )


def forward(model: Model, trf_datas: List[TransformerData], is_train: bool):
    pooling: Model[Ragged, Floats2d] = model.layers[0]
    grad_factor = model.attrs["grad_factor"]
    outputs = []
    backprops = []
    for trf_data in trf_datas:
        if "last_hidden_state" in trf_data.model_output:
            tensor_t_i = cast(BaseModelOutput, trf_data.model_output).last_hidden_state
            if tensor_t_i.size == 0:
                # account for empty trf_data in the batch
                outputs.append(model.ops.alloc2f(0, 0))
            else:
                src = model.ops.reshape2f(tensor_t_i, -1, trf_data.width)  # type: ignore
                dst, get_d_src = apply_alignment(model.ops, trf_data.align, src)
                output, get_d_dst = pooling(dst, is_train)
                outputs.append(output)
                backprops.append((get_d_dst, get_d_src))
        else:
            outputs.append(model.ops.alloc2f(0, 0))

    def backprop_trf_to_tensor(d_outputs: List[Floats2d]) -> List[TransformerData]:
        d_trf_datas = []
        zipped = zip(trf_datas, d_outputs, backprops)
        for trf_data, d_output, (get_d_dst, get_d_src) in zipped:
            d_model_output = ModelOutput(
                last_hidden_state=model.ops.alloc(
                    trf_data.model_output.last_hidden_state.shape,  # type: ignore
                    dtype=trf_data.model_output.last_hidden_state.dtype,  # type: ignore
                )
            )
            d_dst = get_d_dst(d_output)
            d_src = get_d_src(d_dst)
            d_src *= grad_factor
            d_model_output["last_hidden_state"] = d_src.reshape(
                cast(BaseModelOutput, trf_data.model_output).last_hidden_state.shape
            )
            d_trf_datas.append(
                TransformerData(
                    model_output=d_model_output,
                    wordpieces=trf_data.wordpieces,
                    align=trf_data.align,
                )
            )
        return d_trf_datas

    assert len(outputs) == len(trf_datas)
    return outputs, backprop_trf_to_tensor
