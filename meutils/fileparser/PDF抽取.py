import pdfplumber
from pandas import DataFrame
import tabulate

"""
表格
"""


def curves_to_edges(cs):
    edges = []
    for c in cs:
        edges += pdfplumber.utils.rect_to_edges(c)
    return edges


def clean_cell_text(text):
    """
    清除文本中的换行符和多余空格
    """
    if text is None:
        return ""
    text = text.replace("\n", "")
    # 去除字符串开头和结尾的空白字符
    text = text.strip()
    return text


def extract_tables_with_text(self, pdf) -> List[str]:
    """抽取表格并嵌入文本"""

    def check_bboxes(word, table_bbox):
        left = word['x0'], word['top'], word['x1'], word['bottom']
        r = table_bbox
        return left[0] > r[0] and left[1] > r[1] and left[2] < r[2] and left[3] < r[3]

    lines = []
    for page in pdf.pages:
        tables = page.find_tables(
            table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "explicit_vertical_lines": self.curves_to_edges(page.curves) + page.edges,
                "explicit_horizontal_lines": self.curves_to_edges(page.curves) + page.edges,
            }
        )
        bboxes = [table.bbox for table in tables]
        tables = [{'table': i.extract(), 'top': i.bbox[1]} for i in tables]
        non_table_words = [word for word in page.extract_words() if
                           not any([check_bboxes(word, table_bbox) for table_bbox in bboxes])]

        for cluster in pdfplumber.utils.cluster_objects(non_table_words + tables, 'top', tolerance=5):
            if 'text' in cluster[0]:
                lines.append(' '.join([i['text'] for i in cluster]))
            elif 'table' in cluster[0]:
                lines.append(tabulate.tabulate(DataFrame(cluster[0]['table']).applymap(self.clean_cell_text),
                                               tablefmt="github"))
    return lines
