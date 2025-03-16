"""
通用的工具类
commit: 适配LSTM时间序列数据重构
@since 2025年3月11日 20:44:03
"""

import numpy as np
import pandas as pd


def create_sequences(feature_data, target_data, timesteps):
    """创建时间序列样本"""
    X, y = [], []
    # 调整数据形状以适应LSTM输入 (samples, timesteps, features)
    for i in range(timesteps, len(feature_data)):   # discard the last "timestep" days
        X.append(feature_data[i - timesteps:i])     # rolling_timestep * features
        y.append(target_data[i])                    # days * (no rolling_timestep) * features
    return np.array(X), np.array(y)


def prepare_dataset(df, selected_features, target_column, timesteps, x_scaler, y_scaler=None, fit=False):
    """数据集预处理统一方法"""
    # 特征处理
    # 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
    features = df[selected_features].copy().values
    if fit:
        features = x_scaler.fit_transform(features)
    else:
        features = x_scaler.transform(features)

    # 目标值处理
    targets = df[target_column].values.reshape(-1, 1)
    if y_scaler:
        if fit:
            targets = y_scaler.fit_transform(targets)
        else:
            targets = y_scaler.transform(targets)

    # 创建时间序列
    X, y = create_sequences(features, targets, timesteps)
    return X, y




