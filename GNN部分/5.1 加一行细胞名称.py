def get_header_from_file(source_file, encoding='utf-8'):
    """ 安全读取指定文件的第一行 """
    try:
        with open(source_file, 'r', encoding=encoding) as f:
            header = next(f)  # 获取首行
            return header.rstrip('\n') + '\n'  # 标准化换行符
    except StopIteration:
        raise ValueError(f"文件 {source_file} 是空文件")
    except FileNotFoundError:
        raise FileNotFoundError(f"头文件 {source_file} 未找到")

def add_dynamic_header(input_file, output_file, header_source, buffer_size=8192):
    """ 动态添加文件头（支持超大文件）
    
    :param input_file: 要处理的输入文件
    :param output_file: 生成的新文件
    :param header_source: 提供头部的源文件路径
    :param buffer_size: 缓冲区大小（字节）
    """
    # 获取动态头部
    header = get_header_from_file(header_source)
    
    # 流式处理文件
    with (
        open(input_file, 'r', encoding='utf-8') as f_in,
        open(output_file, 'w', encoding='utf-8', buffering=buffer_size) as f_out
    ):
        # 写入头部
        f_out.write(header)
        
        # 复制内容（缓冲区优化）
        while True:
            chunk = f_in.read(buffer_size)
            if not chunk:
                break
            f_out.write(chunk)

# 使用示例
add_dynamic_header(
    input_file = 'GNN部分\\4.1_data.csv',
    output_file = 'GNN部分\\5.1_data.csv',
    header_source = 'GNN部分\data\8w行样本名称.txt.T.csv'
)
# GNN部分\data\8w行样本名称.txt.T.csv