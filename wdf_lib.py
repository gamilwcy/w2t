import os
from renishawWiRE import WDFReader
from typing import Callable, Optional

class WDFConversionError(Exception):
    """自定义异常用于转换错误"""
    pass

def convert_wdf_to_txt(input_dir: str, 
                      output_dir: str,
                      progress_callback: Optional[Callable[[str, int, int], None]] = None,
                      error_callback: Optional[Callable[[str, str], None]] = None) -> None:
    """转换目录中所有WDF文件为TXT格式
    
    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
        progress_callback: 进度回调函数，参数为(当前文件名, 已处理数, 总数)
        error_callback: 错误回调函数，参数为(文件名, 错误信息)
    """
    # 获取所有WDF文件
    try:
        files = [f for f in os.listdir(input_dir) if f.endswith(".wdf")]
    except Exception as e:
        raise WDFConversionError(f"无法读取输入目录: {str(e)}")

    total = len(files)
    if total == 0:
        raise WDFConversionError("输入目录中没有找到WDF文件")

    # 创建输出目录
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        raise WDFConversionError(f"无法创建输出目录: {str(e)}")

    # 处理每个文件
    for i, filename in enumerate(files):
        try:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".wdf", ".txt"))
            
            # 调用单文件转换
            _convert_single_file(input_path, output_path)
            
            # 更新进度
            if progress_callback:
                progress_callback(filename, i+1, total)
                
        except Exception as e:
            if error_callback:
                error_callback(filename, str(e))
            else:
                raise

def _convert_single_file(input_path: str, output_path: str) -> None:
    """转换单个WDF文件"""
    try:
        reader = WDFReader(input_path)
        spectra = reader.spectra
        wavenumbers = reader.xdata
        
        if len(spectra) != len(wavenumbers):
            raise ValueError("光谱数据和波数数据长度不一致")
            
        with open(output_path, 'w') as f:
            f.write("Raman Shift (cm⁻¹)\tIntensity (a.u.)\n")
            for wvn, inten in zip(wavenumbers, spectra):
                f.write(f"{wvn}\t{inten}\n")
                
    except Exception as e:
        raise WDFConversionError(f"文件转换失败: {str(e)}")
