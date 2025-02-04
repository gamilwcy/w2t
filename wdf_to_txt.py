from wdf_lib import convert_wdf_to_txt, WDFConversionError

def cli_progress(filename: str, current: int, total: int):
    print(f"正在处理 {filename} ({current}/{total})")

def cli_error(filename: str, error: str):
    print(f"错误: {filename} - {error}")

if __name__ == "__main__":
    input_dir = input("请输入.wdf文件所在的目录路径: ").strip()
    output_dir = input("请输入保存.txt文件的目录路径: ").strip()

    try:
        convert_wdf_to_txt(
            input_dir=input_dir,
            output_dir=output_dir,
            progress_callback=cli_progress,
            error_callback=cli_error
        )
    except WDFConversionError as e:
        print(f"转换失败: {str(e)}")
