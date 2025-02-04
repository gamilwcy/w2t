import os
from renishawWiRE import WDFReader

def convert_wdf_to_txt(input_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)s

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".wdf"):
            # 构造完整的文件路径
            wdf_path = os.path.join(input_dir, filename)
            txt_filename = filename.replace(".wdf", ".txt")
            txt_path = os.path.join(output_dir, txt_filename)

            # 读取 .wdf 文件
            reader = WDFReader(wdf_path)
            spectra = reader.spectra
            wavenumbers = reader.xdata

            # 将数据保存为 .txt 文件
            with open(txt_path, 'w') as f:
                # 写入表头
                f.write("Raman Shift (cm⁻¹)\tIntensity (a.u.)\n")
                # 写入数据
                for wavenumber, intensity in zip(wavenumbers, spectra):
                    f.write(f"{wavenumber}\t{intensity}\n")

            print(f"转换完成: {filename} -> {txt_filename}")

# 手动输入路径
input_directory = input("请输入 .wdf 文件所在的目录路径: ").strip()
output_directory = input("请输入保存 .txt 文件的目录路径: ").strip()

# 调用函数进行转换
convert_wdf_to_txt(input_directory, output_directory)
