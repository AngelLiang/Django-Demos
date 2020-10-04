import xlwt


def get_borders():
    # color = 69
    color = xlwt.Borders.THIN
    # borders.left = xlwt.Borders.THIN
    # NO_LINE： 官方代码中NO_LINE所表示的值为0，没有边框
    # THIN： 官方代码中THIN所表示的值为1，边框为实线

    borders = xlwt.Borders()
    borders.left = color
    # borders.left = xlwt.Borders.THIN
    borders.right = color
    borders.top = color
    borders.bottom = color
    return borders


def get_pattern():
    # 设置背景颜色
    pattern = xlwt.Pattern()
    # 设置背景颜色的模式
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # 背景颜色
    pattern.pattern_fore_colour = 73
    return pattern


def get_noraml_style():
    style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    al = xlwt.Alignment()
    al.horz = 0x02      # 设置水平居中
    al.vert = 0x01      # 设置垂直居中
    style.alignment = al

    style.borders = get_borders()
    return style


def get_label_style():
    style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    al = xlwt.Alignment()
    al.horz = 0x02      # 设置水平居中
    al.vert = 0x01      # 设置垂直居中
    style.alignment = al

    # font = xlwt.Font()  # 为样式创建字体
    # font.bold = True   # 粗体
    # style.font = font

    # 设置背景颜色
    style.pattern = get_pattern()
    style.borders = get_borders()

    return style


def get_headers_style():
    style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    al = xlwt.Alignment()
    al.horz = 0x02      # 设置水平居中
    al.vert = 0x01      # 设置垂直居中
    style.alignment = al

    # font = xlwt.Font()  # 为样式创建字体
    # font.bold = True   # 粗体
    # style.font = font

    style.pattern = get_pattern()
    style.borders = get_borders()

    return style
