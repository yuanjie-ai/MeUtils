#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : hydra_demo
# @Time         : 2021/1/26 1:28 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://github.com/facebookresearch/hydra/tree/1.0_branch/examples/tutorials/basic/your_first_hydra_app


from omegaconf import DictConfig, OmegaConf
import hydra


@hydra.main(config_name='conf')
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    logger.info("Info level message")


if __name__ == "__main__":
    my_app()
